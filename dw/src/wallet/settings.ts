import AsyncStorage from "@react-native-async-storage/async-storage";

const SETTINGS_KEY = "decimal.wallet.settings.v1";

export type WalletSettings = {
  biometrics: boolean;
  lightTheme: boolean;
  language: "ru" | "en";
};

export const defaultSettings: WalletSettings = {
  biometrics: true,
  lightTheme: false,
  language: "ru",
};

export async function loadSettings(): Promise<WalletSettings> {
  const raw = await AsyncStorage.getItem(SETTINGS_KEY);
  if (!raw) return defaultSettings;
  return { ...defaultSettings, ...JSON.parse(raw) };
}

export async function saveSettings(settings: WalletSettings): Promise<void> {
  await AsyncStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
}
