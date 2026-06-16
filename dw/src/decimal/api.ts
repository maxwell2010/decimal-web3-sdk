import { decimalConfig } from "./config";
import type { Asset } from "@/types";

export type ValidatorSummary = {
  id: string;
  name: string;
  commission: string;
  stakeDel: string;
  active: boolean;
};

export type SwapCoin = {
  id: string;
  symbol: string;
  name: string;
  reserveDel: string;
  priceDel: string | null;
  available: boolean;
  address?: string;
};

export type TxHistoryItem = {
  hash: string;
  type: string;
  status: string;
  amount: string;
  timestamp: string;
};

export type DelegationItem = {
  validator: string;
  moniker: string;
  amountDel: string;
  symbol: string;
  rewardDel: string;
};

export async function getValidators(limit = 100): Promise<ValidatorSummary[]> {
  const priorityRows = await Promise.allSettled([
    getValidatorDetails("0x7a3585a25792e01f0e623881c96f8c1b36a75fbf"),
  ]);
  const rows: any[] = priorityRows
    .filter((row): row is PromiseFulfilledResult<any> => row.status === "fulfilled" && row.value)
    .map((row) => row.value);

  try {
    const payload = await getJson(`${decimalConfig.apiBaseUrl}/validators?limit=${limit}`, 5000);
    const list = Array.isArray(payload?.validators) ? payload.validators : [];
    for (const item of list) rows.push(item);
  } catch {
    // Keep priority validators visible even if the full list is slow.
  }
  const merged = new Map<string, any>();
  for (const item of rows) {
    const id = String(item.drc20_address || item.address || item.evmAddress || item.operator_address || "").toLowerCase();
    if (id && !merged.has(id)) merged.set(id, item);
  }
  return [...merged.values()].map((item: any) => ({
    id: String(item.drc20_address || item.address || item.evmAddress || item.operator_address || ""),
    name: String(item.moniker || item.name || item.description?.moniker || "Валидатор"),
    commission: `${Math.round(Number(item.commission || 0) * 100)}%`,
    stakeDel: formatDel(item.stake),
    active: item.online === true && item.jailed !== true,
  }))
    .filter((item: ValidatorSummary) => item.id)
    .sort((a: ValidatorSummary, b: ValidatorSummary) => prioritySort(a.name, b.name, ["MINTCANDY", "FREEDOM"]));
}

export async function getSwapCoins(limit = 1000): Promise<SwapCoin[]> {
  const [rows, priorityRows] = await Promise.all([
    getCoinPages(limit).catch(() => []),
    Promise.allSettled(["mintcandy", "byacademy", "fbworld"].map((symbol) => getCoinDetails(symbol))),
  ]);
  const merged = new Map<string, SwapCoin>();
  for (const item of rows) {
    const coin = swapCoinFromApi(item);
    if (coin) merged.set(coin.id.toLowerCase(), coin);
  }
  for (const row of priorityRows) {
    if (row.status !== "fulfilled") continue;
    const coin = swapCoinFromApi(row.value);
    if (coin) merged.set(coin.id.toLowerCase(), coin);
  }
  return [...merged.values()]
    .sort((a: SwapCoin, b: SwapCoin) => a.symbol.localeCompare(b.symbol, "ru"));
}

export async function getAddressAssets(address: string): Promise<Asset[]> {
  const indexed = await getIndexedBalances(address).catch(() => null);
  const assets = new Map<string, Asset>();
  for (const item of indexed?.balances || []) {
    const asset = assetFromIndexedBalance(item);
    if (asset) assets.set(asset.id.toLowerCase(), asset);
  }

  if (assets.size === 0) {
    const nativeRows = await getAddressBalanceRows(address).catch(() => []);
    const nativeDel = nativeAssetFromRows(nativeRows);
    if (nativeDel) assets.set("del", nativeDel);
  }

  return sortAssets([...assets.values()]);
}

export async function getTxHistory(address: string, limit = 100): Promise<TxHistoryItem[]> {
  const safeLimit = Math.min(Math.max(limit, 1), 100);
  const payload = await getJson(`${decimalConfig.apiBaseUrl}/addresses/${address}/txs?limit=${safeLimit}`);
  const rows = Array.isArray(payload?.data) ? payload.data : Array.isArray(payload?.txs) ? payload.txs : [];
  return rows.slice(0, safeLimit).map((item: any) => ({
    hash: String(item.hash || item.tx_hash || item.txhash || ""),
    type: String(item.type || item.message_type || item.tx_type || "Транзакция"),
    status: normalizeTxStatus(item.raw_data?.transaction_status || item.transaction_status || item.status || item.code),
    amount: String(item.amount || item.value || ""),
    timestamp: String(item.timestamp || item.created_at || item.time || ""),
  })).filter((item: TxHistoryItem) => item.hash);
}

export async function getDelegations(address: string, validators: ValidatorSummary[]): Promise<DelegationItem[]> {
  try {
    const payload = await getJson(`${decimalConfig.centralApiUrl}/v1/wallets/${address.toLowerCase()}/staking`, 18000);
    const parsed = delegationItemsFromPayload(payload);
    if (parsed.length > 0) return parsed;
  } catch {
    // Fall back to direct node API below.
  }
  try {
    const payload = await getJson(`${decimalConfig.apiBaseUrl}/validators/wallet/${address}/stakes/coins`, 15000);
    const parsed = delegationItemsFromPayload(payload);
    if (parsed.length > 0) return parsed;
  } catch {
    // Fall back to scanning visible validators.
  }
  return getDelegationsByValidatorScan(address, validators);
}

function delegationItemsFromPayload(payload: any): DelegationItem[] {
  const root = payload?.Result || payload?.result || payload;
  const rows = Array.isArray(root?.items) ? root.items : [];
  return rows.flatMap((row: any) => {
    const validator = row.validator || {};
    const items = Array.isArray(row.items) ? row.items : [];
    return items.map((item: any) => ({
      validator: String(validator.drc20_address || validator.address || validator.operator_address || ""),
      moniker: String(validator.moniker || validator.name || validator.description?.moniker || "Валидатор"),
      amountDel: trimDecimal(String(item.delegatedBaseCoinsFormatted || item.delegatedCoinsFormatted || item.stake?.amount_formatted || "0")),
      symbol: String(item.symbol || item.coin_symbol || item.stake?.symbol || "DEL").toUpperCase(),
      rewardDel: formatDel(validator.rewards || "0"),
    }));
  }).filter((item: DelegationItem) => Number(item.amountDel) > 0);
}

async function getDelegationsByValidatorScan(address: string, validators: ValidatorSummary[]): Promise<DelegationItem[]> {
  const delegator = evmToBech32(address);
  const rows = await Promise.allSettled(validators.slice(0, 20).map(async (validator) => {
    const payload = await getJson(`${decimalConfig.apiBaseUrl}/validators/${validator.id}/delegations`, 8000);
    const delegations = Array.isArray(payload?.delegations) ? payload.delegations : Array.isArray(payload?.data) ? payload.data : [];
    const matched = delegations.find((item: any) => String(item.delegator || item.delegator_address || "").toLowerCase() === delegator);
    if (!matched) return null;
    return {
      validator: validator.id,
      moniker: validator.name,
      amountDel: formatDel(matched.stake || matched.amount || matched.value || "0"),
      symbol: String(matched.symbol || matched.denom || "DEL").toUpperCase(),
      rewardDel: formatDel(matched.reward || matched.rewards || "0"),
    };
  }));
  return rows
    .filter((item): item is PromiseFulfilledResult<DelegationItem | null> => item.status === "fulfilled")
    .map((item) => item.value)
    .filter((item): item is DelegationItem => item !== null && Number(item.amountDel) > 0);
}

async function getIndexedBalances(address: string): Promise<{ balances: any[] } | null> {
  const query = "limit=300&offset=0&include_bank=1&prefer_bank=1";
  for (const baseUrl of apiBaseUrls()) {
    try {
      const payload = await getJson(`${baseUrl}/erc20/balances/${address.toLowerCase()}?${query}`, 7000);
      const root = unwrapApiResult(payload);
      const balances = Array.isArray(root?.balances) ? root.balances : [];
      if (balances.length > 0) return { balances };
    } catch {
      // Try the next node API source.
    }
  }
  return null;
}

async function getCoinDetails(symbol: string): Promise<any> {
  const payload = await getJson(`${decimalConfig.apiBaseUrl}/coins/${encodeURIComponent(symbol)}`);
  const root = unwrapApiResult(payload);
  return root?.coin || root;
}

async function getCoinPages(limit: number): Promise<any[]> {
  const pageLimit = 50;
  const maxItems = Math.max(pageLimit, limit);
  const rows: any[] = [];
  let nextKey = "";
  while (rows.length < maxItems) {
    const params = [
      `pagination.limit=${pageLimit}`,
      "with_price=0",
    ];
    if (nextKey) params.push(`pagination.key=${encodeURIComponent(nextKey)}`);
    const payload = await getJson(`${decimalConfig.apiBaseUrl}/coins?${params.join("&")}`, 15000);
    const page = Array.isArray(payload?.coins) ? payload.coins : [];
    rows.push(...page);
    nextKey = String(payload?.pagination?.next_key || "");
    if (!nextKey || page.length === 0) break;
  }
  return rows.slice(0, maxItems);
}

async function getValidatorDetails(address: string): Promise<any> {
  const payload = await getJson(`${decimalConfig.apiBaseUrl}/validators/${address}`, 12000);
  return unwrapApiResult(payload);
}

async function getAddressBalanceRows(address: string): Promise<any[]> {
  for (const baseUrl of apiBaseUrls()) {
    try {
      const payload = await getJson(`${baseUrl}/addresses/${address.toLowerCase()}/balances`, 7000);
      const root = unwrapApiResult(payload);
      const rows = Array.isArray(root?.balances) ? root.balances : [];
      if (rows.length > 0) return rows;
    } catch {
      // Try the next Decimal API source.
    }
  }
  return [];
}

function nativeAssetFromRows(rows: any[]): Asset | null {
  const del = rows.find((item: any) => String(item?.denom || "").toLowerCase() === "del");
  if (!del) return null;
  const balance = amountToDecimal(del.amount || del.balance_raw || del.balance);
  if (Number(balance) <= 0) return null;
  return {
    id: "del",
    type: "coin",
    symbol: "DEL",
    name: "Decimal",
    balance,
    decimals: 18,
  };
}

function assetFromIndexedBalance(item: any): Asset | null {
  const denom = String(item?.denom || item?.symbol || "").trim();
  if (!denom) return null;
  const isDel = denom.toLowerCase() === "del" || item?.native === true;
  const contract = String(item?.contract_address || item?.drc20_address || "").trim();
  if (!isDel && !contract.toLowerCase().startsWith("0x")) return null;
  const balance = amountToDecimal(item?.balance_raw || item?.amount || item?.balance);
  if (Number(balance) <= 0) return null;
  if (isDel) {
    return {
      id: "del",
      type: "coin",
      symbol: "DEL",
      name: "Decimal",
      balance,
      decimals: 18,
    };
  }
  return {
    id: contract,
    type: "erc20",
    address: contract,
    symbol: denom.toUpperCase(),
    name: String(item?.name || item?.title || denom).trim(),
    balance,
    decimals: Number(item?.decimals || 18),
  };
}

function swapCoinFromApi(item: any): SwapCoin | null {
  const address = String(item?.drc20_address || item?.contract_address || item?.address || "").trim();
  const symbol = String(item?.denom || item?.symbol || "").trim().toUpperCase();
  if (!symbol || !address.toLowerCase().startsWith("0x")) return null;
  const reserveDel = formatDel(item?.reserve);
  const priceDel = typeof item?.current_price_del === "string" ? trimDecimal(item.current_price_del, 18) : calculateCoinPriceDel(item);
  return {
    id: address,
    symbol,
    name: String(item?.title || item?.name || symbol).trim(),
    reserveDel,
    priceDel,
    available: Number(reserveDel) > 0 && priceDel !== null,
    address,
  };
}

function calculateCoinPriceDel(item: any): string | null {
  const reserve = Number(formatDel(item?.reserve));
  const volume = Number(formatDel(item?.volume));
  const crr = Number(item?.crr || 0);
  if (!Number.isFinite(reserve) || !Number.isFinite(volume) || !Number.isFinite(crr) || reserve <= 0 || volume <= 0 || crr <= 0) {
    return null;
  }
  return trimDecimal(String(reserve / (volume * (crr / 100))), 18);
}

function normalizeTxStatus(raw: unknown): string {
  if (raw === 0 || raw === "0") return "Удачно";
  const value = String(raw || "").trim().toLowerCase();
  if (["success", "successful", "ok", "confirmed", "completed", "done", "true", "удачно", "успешно"].includes(value)) return "Удачно";
  if (["failed", "fail", "error", "rejected", "reverted", "false", "не удачно", "неудачно"].includes(value)) return "Не удачно";
  if (/^\d+$/.test(value) && Number(value) > 0) return "Не удачно";
  return "В обработке";
}

async function getJson(url: string, timeoutMs = 40000): Promise<any> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, { signal: controller.signal });
    if (!response.ok) throw new Error(`Request failed ${response.status}`);
    return response.json();
  } finally {
    clearTimeout(timer);
  }
}

function unwrapApiResult(payload: any): any {
  if (!payload || typeof payload !== "object") return payload;
  if (payload.Ok === true || payload.ok === true) return payload.Result || payload.result || {};
  return payload.Result || payload.result || payload;
}

function formatDel(raw: unknown): string {
  const value = typeof raw === "string" ? raw : String(raw || "0");
  if (!/^\d+$/.test(value)) return "0";
  return trimDecimal(`${value.slice(0, -18) || "0"}.${value.slice(-18).padStart(18, "0")}`);
}

function amountToDecimal(raw: unknown): string {
  const value = typeof raw === "string" ? raw : String(raw || "0");
  if (value.includes(".")) return trimDecimal(value);
  return formatDel(value);
}

function trimDecimal(value: string, precision = 4): string {
  const [whole, fraction = ""] = value.split(".");
  let effectivePrecision = precision;
  if (/^-?0$/.test(whole) && fraction) {
    const firstNonZero = fraction.search(/[1-9]/);
    if (firstNonZero >= precision) effectivePrecision = Math.min(fraction.length, firstNonZero + 4);
  }
  const cut = fraction.slice(0, effectivePrecision).replace(/0+$/, "");
  return cut ? `${whole}.${cut}` : whole;
}

function apiBaseUrls(): string[] {
  return [
    decimalConfig.apiBaseUrl,
    ...Array.from(decimalConfig.apiFallbackBaseUrls || []),
  ].filter((url, index, all) => Boolean(url) && all.indexOf(url) === index);
}

function sortAssets(assets: Asset[]): Asset[] {
  return [...assets].sort((a, b) => {
    if (a.symbol === "DEL") return -1;
    if (b.symbol === "DEL") return 1;
    return prioritySort(a.symbol, b.symbol, ["MINTCANDY"]);
  });
}

function prioritySort(a: string, b: string, priority: string[]): number {
  const au = a.toUpperCase();
  const bu = b.toUpperCase();
  const ai = priority.indexOf(au);
  const bi = priority.indexOf(bu);
  if (ai !== -1 || bi !== -1) {
    if (ai === -1) return 1;
    if (bi === -1) return -1;
    return ai - bi;
  }
  return au.localeCompare(bu, "ru");
}

function evmToBech32(address: string, prefix = "d0"): string {
  const hex = address.toLowerCase().replace(/^0x/, "");
  const bytes = hex.match(/.{1,2}/g)?.map((item) => parseInt(item, 16)) || [];
  return bech32Encode(prefix, convertBits(bytes, 8, 5, true));
}

function bech32Encode(prefix: string, words: number[]): string {
  const alphabet = "qpzry9x8gf2tvdw0s3jn54khce6mua7l";
  const checksum = bech32CreateChecksum(prefix, words);
  return `${prefix}1${[...words, ...checksum].map((word) => alphabet[word]).join("")}`;
}

function bech32CreateChecksum(prefix: string, words: number[]): number[] {
  const values = [...bech32HrpExpand(prefix), ...words, 0, 0, 0, 0, 0, 0];
  const mod = bech32Polymod(values) ^ 1;
  return [0, 1, 2, 3, 4, 5].map((index) => (mod >> (5 * (5 - index))) & 31);
}

function bech32HrpExpand(prefix: string): number[] {
  return [...prefix].map((char) => char.charCodeAt(0) >> 5).concat(0, [...prefix].map((char) => char.charCodeAt(0) & 31));
}

function bech32Polymod(values: number[]): number {
  const generators = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3];
  let chk = 1;
  for (const value of values) {
    const top = chk >> 25;
    chk = ((chk & 0x1ffffff) << 5) ^ value;
    for (let i = 0; i < 5; i += 1) {
      if ((top >> i) & 1) chk ^= generators[i];
    }
  }
  return chk;
}

function convertBits(data: number[], from: number, to: number, pad: boolean): number[] {
  let acc = 0;
  let bits = 0;
  const ret: number[] = [];
  const maxv = (1 << to) - 1;
  for (const value of data) {
    acc = (acc << from) | value;
    bits += from;
    while (bits >= to) {
      bits -= to;
      ret.push((acc >> bits) & maxv);
    }
  }
  if (pad && bits > 0) ret.push((acc << (to - bits)) & maxv);
  return ret;
}
