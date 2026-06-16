import AsyncStorage from "@react-native-async-storage/async-storage";
import type { Asset } from "@/types";
import type { ContactItem } from "@/types";
import type { DelegationItem, TxHistoryItem, ValidatorSummary } from "@/decimal/api";

const key = (address: string, name: string) => `candywallet:${address.toLowerCase()}:${name}`;

export async function loadCachedAssets(address: string): Promise<Asset[] | null> {
  return loadJson<Asset[]>(key(address, "assets"));
}

export async function saveCachedAssets(address: string, assets: Asset[]): Promise<void> {
  await saveJson(key(address, "assets"), assets);
}

export async function loadCachedHistory(address: string): Promise<TxHistoryItem[] | null> {
  return loadJson<TxHistoryItem[]>(key(address, "history"));
}

export async function saveCachedHistory(address: string, history: TxHistoryItem[]): Promise<void> {
  await saveJson(key(address, "history"), history.slice(0, 100));
}

export async function loadCachedStake(address: string): Promise<{ validators: ValidatorSummary[]; delegations: DelegationItem[] } | null> {
  return loadJson<{ validators: ValidatorSummary[]; delegations: DelegationItem[] }>(key(address, "stake"));
}

export async function saveCachedStake(address: string, validators: ValidatorSummary[], delegations: DelegationItem[]): Promise<void> {
  await saveJson(key(address, "stake"), { validators, delegations });
}

export async function loadContacts(address: string): Promise<ContactItem[]> {
  return loadJson<ContactItem[]>(key(address, "contacts")).then((items) => items || []);
}

export async function saveContacts(address: string, contacts: ContactItem[]): Promise<void> {
  await saveJson(key(address, "contacts"), contacts);
}

async function loadJson<T>(storageKey: string): Promise<T | null> {
  try {
    const raw = await AsyncStorage.getItem(storageKey);
    return raw ? JSON.parse(raw) as T : null;
  } catch {
    return null;
  }
}

async function saveJson(storageKey: string, value: unknown): Promise<void> {
  try {
    await AsyncStorage.setItem(storageKey, JSON.stringify(value));
  } catch {
    // Cache writes are best-effort; wallet operations must not depend on them.
  }
}
