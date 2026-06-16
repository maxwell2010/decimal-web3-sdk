export type AssetType = "coin" | "erc20" | "nft";

export type Asset = {
  id: string;
  type: AssetType;
  symbol: string;
  name: string;
  address?: string;
  tokenId?: string;
  balance: string;
  decimals: number;
  icon?: string;
};

export type WalletAccount = {
  address: string;
  mnemonic?: string;
  privateKey?: string;
};

export type SendDraft = {
  to: string;
  asset: Asset;
  amount: string;
  memo?: string;
};

export type PaymentRequest = {
  network: "decimal";
  address: string;
  token: string;
  tokenAddress?: string;
  amount?: string;
  memo?: string;
};

export type ContactItem = {
  id: string;
  name: string;
  address: string;
};

export type Screen =
  | "welcome"
  | "pin"
  | "assets"
  | "swap"
  | "transfer"
  | "stake"
  | "settings"
  | "changePin"
  | "contacts"
  | "contactPicker"
  | "about"
  | "assetPicker"
  | "coinPicker"
  | "transit";
