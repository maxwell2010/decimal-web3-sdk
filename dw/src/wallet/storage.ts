import * as SecureStore from "expo-secure-store";
import { generateMnemonic } from "@scure/bip39";
import { wordlist } from "@scure/bip39/wordlists/english";
import { mnemonicToAccount } from "viem/accounts";
import type { WalletAccount } from "@/types";

const WALLET_KEY = "decimal.wallet.v1";
const PIN_KEY = "decimal.pin.v1";

export async function importWallet(mnemonic: string): Promise<WalletAccount> {
  const account = mnemonicToAccount(mnemonic.trim());
  const wallet = { address: account.address, mnemonic: mnemonic.trim() };
  await SecureStore.setItemAsync(WALLET_KEY, JSON.stringify(wallet));
  return wallet;
}

export async function generateWallet(): Promise<WalletAccount> {
  const mnemonic = generateMnemonic(wordlist, 128);
  return importWallet(mnemonic);
}

export async function loadWallet(): Promise<WalletAccount | null> {
  const raw = await SecureStore.getItemAsync(WALLET_KEY);
  return raw ? (JSON.parse(raw) as WalletAccount) : null;
}

export async function clearWallet(): Promise<void> {
  await SecureStore.deleteItemAsync(WALLET_KEY);
  await SecureStore.deleteItemAsync(PIN_KEY);
}

export async function savePin(pin: string): Promise<void> {
  await SecureStore.setItemAsync(PIN_KEY, pin);
}

export async function loadPin(): Promise<string | null> {
  return SecureStore.getItemAsync(PIN_KEY);
}
