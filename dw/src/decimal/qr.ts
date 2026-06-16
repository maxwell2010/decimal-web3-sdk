import type { Asset, PaymentRequest } from "@/types";

const PREFIX = "decimal:";

export function buildPaymentRequest(input: {
  address: string;
  asset: Asset;
  amount?: string;
  memo?: string;
}): string {
  const params = new URLSearchParams();
  params.set("token", input.asset.symbol);
  if (input.asset.address) params.set("tokenAddress", input.asset.address);
  if (input.amount) params.set("amount", input.amount);
  if (input.memo) params.set("memo", input.memo);
  return `${PREFIX}${input.address}?${params.toString()}`;
}

export function parsePaymentRequest(value: string): PaymentRequest | null {
  if (!value.startsWith(PREFIX)) return null;
  const body = value.slice(PREFIX.length);
  const [address, query = ""] = body.split("?");
  if (!address || !address.startsWith("0x")) return null;
  const params = new URLSearchParams(query);
  const token = params.get("token") || "DEL";
  return {
    network: "decimal",
    address,
    token,
    tokenAddress: params.get("tokenAddress") || undefined,
    amount: params.get("amount") || undefined,
    memo: params.get("memo") || undefined,
  };
}
