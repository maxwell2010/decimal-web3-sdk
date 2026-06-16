import { decimalConfig } from "@/decimal/config";
import AsyncStorage from "@react-native-async-storage/async-storage";

export type DelFiatRates = {
  usd: number | null;
  rub: number | null;
  change24: number | null;
  updatedAt: number;
};

let cachedRates: DelFiatRates | null = null;
let cachedAt = 0;
const cacheTtlMs = 30_000;
const storageKey = "decimal.market.del_fiat_rates.v1";

export async function getDelFiatRates(): Promise<DelFiatRates | null> {
  const now = Date.now();
  cachedRates = cachedRates || await loadStoredRates();
  if (cachedRates && now - cachedAt < cacheTtlMs) return cachedRates;

  const apiRates = await fetchOwnApiRates();
  if (apiRates) {
    cachedRates = apiRates;
    cachedAt = now;
    await AsyncStorage.setItem(storageKey, JSON.stringify(apiRates));
    return apiRates;
  }

  try {
    const response = await withTimeout(fetch(`${decimalConfig.bitteamApiUrl}/pairs`), 4500);
    if (!response.ok) return cachedRates;
    const payload = await response.json();
    const pairs = Array.isArray(payload?.result?.pairs) ? payload.result.pairs : [];
    const delUsdt = pairs.find((pair: unknown) => isPair(pair, "del_usdt"));
    const delRub = pairs.find((pair: unknown) => isPair(pair, "del_rub"));
    const rates: DelFiatRates = {
      usd: readNumber(delUsdt?.lastPrice),
      rub: readNumber(delRub?.lastPrice),
      change24: readNumber(delUsdt?.change24 ?? delUsdt?.change24h),
      updatedAt: now,
    };
    cachedRates = rates.usd || rates.rub ? rates : cachedRates;
    cachedAt = now;
    if (cachedRates === rates) {
      await AsyncStorage.setItem(storageKey, JSON.stringify(rates));
    }
    return cachedRates;
  } catch {
    return cachedRates;
  }
}

async function fetchOwnApiRates(): Promise<DelFiatRates | null> {
  try {
    const response = await withTimeout(fetch(decimalConfig.marketRatesUrl), 4500);
    if (!response.ok) return null;
    const payload = await response.json();
    const result = payload?.Result || payload?.result;
    const rates: DelFiatRates = {
      usd: readNumber(result?.usd),
      rub: readNumber(result?.rub),
      change24: typeof result?.change24 === "number" ? result.change24 : null,
      updatedAt: typeof result?.fetched_at_unix === "number" ? Math.round(result.fetched_at_unix * 1000) : Date.now(),
    };
    return rates.usd || rates.rub ? rates : null;
  } catch {
    return null;
  }
}

async function loadStoredRates(): Promise<DelFiatRates | null> {
  try {
    const raw = await AsyncStorage.getItem(storageKey);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as Partial<DelFiatRates>;
    const rates: DelFiatRates = {
      usd: readNumber(parsed.usd),
      rub: readNumber(parsed.rub),
      change24: typeof parsed.change24 === "number" ? parsed.change24 : null,
      updatedAt: typeof parsed.updatedAt === "number" ? parsed.updatedAt : 0,
    };
    cachedAt = rates.updatedAt;
    return rates.usd || rates.rub ? rates : null;
  } catch {
    return null;
  }
}

function isPair(pair: unknown, name: string): pair is { name?: string; lastPrice?: unknown; change24?: unknown; change24h?: unknown } {
  return typeof pair === "object" && pair !== null && (pair as { name?: string }).name === name;
}

function readNumber(value: unknown): number | null {
  const numberValue = Number(value);
  return Number.isFinite(numberValue) && numberValue > 0 ? numberValue : null;
}

async function withTimeout<T>(promise: Promise<T>, timeoutMs: number): Promise<T> {
  return Promise.race([
    promise,
    new Promise<T>((_, reject) => {
      setTimeout(() => reject(new Error("BitTeam request timeout")), timeoutMs);
    }),
  ]);
}
