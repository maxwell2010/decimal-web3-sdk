import { StatusBar } from "expo-status-bar";
import * as Clipboard from "expo-clipboard";
import * as LocalAuthentication from "expo-local-authentication";
import { LinearGradient } from "expo-linear-gradient";
import { CameraView, useCameraPermissions } from "expo-camera";
import QRCode from "react-native-qrcode-svg";
import {
  Alert,
  ActivityIndicator,
  Animated,
  Easing,
  Image,
  KeyboardAvoidingView,
  Modal,
  Platform,
  Pressable,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Switch,
  Text,
  TextInput,
  View,
  Linking,
} from "react-native";
import { useEffect, useMemo, useRef, useState } from "react";
import { ArrowLeft, ChevronDown, ChevronRight, Copy, Maximize, QrCode, Repeat2, ScanLine, Search, Share2, Trash2, UserPlus, X } from "lucide-react-native";
import { AssetIcon } from "@/components/AssetIcon";
import { GradientButton } from "@/components/GradientButton";
import { Logo } from "@/components/Logo";
import { TabBar } from "@/components/TabBar";
import { buildPaymentRequest, parsePaymentRequest } from "@/decimal/qr";
import { DecimalMobileClient } from "@/decimal/client";
import { getAddressAssets, getDelegations, getSwapCoins, getTxHistory, getValidators } from "@/decimal/api";
import { getDelFiatRates } from "@/market/bitteam";
import { loadSettings, saveSettings } from "@/wallet/settings";
import { clearWallet, generateWallet, importWallet, loadPin, loadWallet, savePin } from "@/wallet/storage";
import { loadCachedAssets, loadCachedHistory, loadCachedStake, loadContacts, saveCachedAssets, saveCachedHistory, saveCachedStake, saveContacts } from "@/wallet/cache";
import { colors, gradients, radii, setThemeMode, spacing } from "@/theme";
import type { Asset, ContactItem, PaymentRequest, Screen, WalletAccount } from "@/types";
import type { DelegationItem, SwapCoin, TxHistoryItem, ValidatorSummary } from "@/decimal/api";
import type { DelFiatRates } from "@/market/bitteam";

const client = new DecimalMobileClient();

export default function App() {
  const [screen, setScreen] = useState<Screen>("welcome");
  const [wallet, setWallet] = useState<WalletAccount | null>(null);
  const [pinMode, setPinMode] = useState<"create" | "unlock">("create");
  const [assets, setAssets] = useState<Asset[]>(fallbackAssets);
  const [assetLoading, setAssetLoading] = useState(false);
  const [assetError, setAssetError] = useState<string | null>(null);
  const [delRates, setDelRates] = useState<DelFiatRates | null>(null);
  const [ratesLoading, setRatesLoading] = useState(false);
  const [selectedAssetId, setSelectedAssetId] = useState("del");
  const [assetPickerReturn, setAssetPickerReturn] = useState<"swap" | "transfer">("transfer");
  const [selectedSwapCoinId, setSelectedSwapCoinId] = useState("");
  const [dataOverlay, setDataOverlay] = useState<{ visible: boolean; text: string }>({ visible: false, text: "" });
  const [dataOverlayTimedOut, setDataOverlayTimedOut] = useState(false);
  const [dataNotice, setDataNotice] = useState("");
  const [receiveAmount, setReceiveAmount] = useState("");
  const [sendTo, setSendTo] = useState("");
  const [sendAmount, setSendAmount] = useState("");
  const [paymentRequest, setPaymentRequest] = useState<PaymentRequest | null>(null);
  const [transferTab, setTransferTab] = useState<"send" | "receive">("send");
  const [scannerOpen, setScannerOpen] = useState(false);
  const [cameraPermission, requestCameraPermission] = useCameraPermissions();
  const [lightTheme, setLightTheme] = useState(false);
  const [biometrics, setBiometrics] = useState(true);
  const [language, setLanguage] = useState<"ru" | "en">("ru");
  const [validators, setValidators] = useState<ValidatorSummary[]>([]);
  const [delegations, setDelegations] = useState<DelegationItem[]>([]);
  const [swapCoins, setSwapCoins] = useState<SwapCoin[]>([]);
  const [history, setHistory] = useState<TxHistoryItem[]>([]);
  const [contacts, setContacts] = useState<ContactItem[]>([]);
  const [sending, setSending] = useState(false);
  const [staking, setStaking] = useState(false);
  const [swapping, setSwapping] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [swapLoading, setSwapLoading] = useState(false);
  const [stakeLoading, setStakeLoading] = useState(false);
  const [txOverlay, setTxOverlay] = useState<{ visible: boolean; loading: boolean; title: string; message: string; kind: "info" | "success" | "error" }>({ visible: false, loading: false, title: "", message: "", kind: "info" });
  const [changePinStep, setChangePinStep] = useState<"old" | "new">("old");

  setThemeMode(lightTheme);
  styles = createStyles();
  const selectedAsset = assets.find((item) => item.id === selectedAssetId) || assets[0];
  const dataLoading = dataOverlay.visible || assetLoading || historyLoading || stakeLoading;

  useEffect(() => {
    if (!dataLoading) {
      setDataOverlayTimedOut(false);
      return undefined;
    }
    setDataNotice("");
    setDataOverlayTimedOut(false);
    const timer = setTimeout(() => {
      setAssetLoading(false);
      setHistoryLoading(false);
      setSwapLoading(false);
      setStakeLoading(false);
      setDataOverlay({ visible: false, text: "" });
      setDataOverlayTimedOut(true);
      setDataNotice("Не смог получить данные");
    }, 45000);
    return () => clearTimeout(timer);
  }, [dataLoading]);

  useEffect(() => {
    loadSettings().then((settings) => {
      setLightTheme(settings.lightTheme);
      setBiometrics(settings.biometrics);
      setLanguage(settings.language);
    });
    loadWallet().then(async (stored) => {
      if (!stored) return;
      setWallet(stored);
      const [cachedAssets, cachedHistory, cachedStake, cachedContacts] = await Promise.all([
        loadCachedAssets(stored.address),
        loadCachedHistory(stored.address),
        loadCachedStake(stored.address),
        loadContacts(stored.address),
      ]);
      if (cachedAssets) {
        const cleanedAssets = normalizeAssets(cachedAssets);
        if (hasUsableAssets(cleanedAssets)) {
          setAssets(cleanedAssets);
        }
      }
      if (cachedHistory) setHistory(cachedHistory);
      if (cachedStake) {
        setValidators(cachedStake.validators);
        setDelegations(cachedStake.delegations);
      }
      setContacts(cachedContacts);
      const storedPin = await loadPin();
      setPinMode(storedPin ? "unlock" : "create");
      setScreen("pin");
    });
  }, []);

  useEffect(() => {
    if (!wallet) return;
    setAssetLoading(true);
    setDataOverlay({ visible: true, text: "Обновление данных" });
    setAssetError(null);
    getAddressAssets(wallet.address)
      .then((next) => {
        const cleanedAssets = normalizeAssets(next);
        if (cleanedAssets.length > 0) {
          setAssets(cleanedAssets);
          saveCachedAssets(wallet.address, cleanedAssets);
        }
      })
      .catch(() => {
        setAssetError("Не удалось обновить баланс. Проверьте интернет и попробуйте позже.");
      })
      .finally(() => {
        setAssetLoading(false);
        setDataOverlay({ visible: false, text: "" });
      });
  }, [wallet]);

  useEffect(() => {
    if (!wallet) return;
    setRatesLoading(true);
    getDelFiatRates()
      .then(setDelRates)
      .finally(() => setRatesLoading(false));
  }, [wallet]);

  useEffect(() => {
    saveSettings({ biometrics, lightTheme, language }).catch(() => undefined);
  }, [biometrics, lightTheme, language]);

  useEffect(() => {
    if (!wallet) return;
    setStakeLoading(true);
    setSwapLoading(true);
    setHistoryLoading(true);
    getValidators().then((nextValidators) => {
      if (nextValidators.length > 0) setValidators(nextValidators);
    }).catch(() => undefined).finally(() => setStakeLoading(false));
    getSwapCoins().then((coins) => {
      setSwapCoins(coins);
      if (!selectedSwapCoinId || !coins.some((coin) => coin.id === selectedSwapCoinId)) {
        setSelectedSwapCoinId(coins.find((coin) => coin.symbol.toUpperCase() === "MINTCANDY")?.id || coins[0]?.id || "");
      }
    }).catch(() => undefined).finally(() => setSwapLoading(false));
    getTxHistory(wallet.address, 100).then((next) => {
      setHistory(next);
      saveCachedHistory(wallet.address, next);
    }).catch(() => undefined).finally(() => setHistoryLoading(false));
  }, [wallet]);

  useEffect(() => {
    if (!wallet || validators.length === 0) return;
    setStakeLoading(true);
    getDelegations(wallet.address, validators).then((next) => {
      setDelegations(next);
      saveCachedStake(wallet.address, validators, next);
    }).catch(() => undefined).finally(() => setStakeLoading(false));
  }, [wallet, validators]);

  useEffect(() => {
    if (!wallet || screen !== "stake") return;
    let active = true;
    setDataOverlay({ visible: true, text: "Обновление данных" });
    setStakeLoading(true);
    getValidators()
      .then(async (nextValidators) => {
        if (!active) return;
        setValidators(nextValidators);
        const nextDelegations = await getDelegations(wallet.address, nextValidators);
        if (!active) return;
        setDelegations(nextDelegations);
        saveCachedStake(wallet.address, nextValidators, nextDelegations);
      })
      .catch(() => {
        if (!active) return;
        setDataNotice("Не смог получить данные");
      })
      .finally(() => {
        if (!active) return;
        setStakeLoading(false);
        setDataOverlay({ visible: false, text: "" });
      });
    return () => {
      active = false;
    };
  }, [screen, wallet]);

  useEffect(() => {
    if (!wallet || screen !== "transfer") return;
    setDataOverlay({ visible: true, text: "Обновление данных" });
    setHistoryLoading(true);
    getTxHistory(wallet.address, 100).then((next) => {
      setHistory(next);
      saveCachedHistory(wallet.address, next);
    }).catch(() => undefined).finally(() => {
      setHistoryLoading(false);
      setDataOverlay({ visible: false, text: "" });
    });
  }, [screen, wallet]);

  useEffect(() => {
    if (!wallet || screen !== "swap") return;
    setSwapLoading(true);
    getSwapCoins().then((coins) => {
      setSwapCoins(coins);
      setSelectedSwapCoinId((current) => coins.some((coin) => coin.id === current) ? current : coins.find((coin) => coin.symbol.toUpperCase() === "MINTCANDY")?.id || coins[0]?.id || "");
    }).catch(() => undefined).finally(() => {
      setSwapLoading(false);
    });
  }, [screen, wallet]);

  async function refreshWalletData() {
    if (!wallet) return;
    const [nextAssets, nextHistory] = await Promise.all([
      getAddressAssets(wallet.address).catch(() => []),
      getTxHistory(wallet.address, 100).catch(() => []),
    ]);
    const cleanedAssets = normalizeAssets(nextAssets);
    if (cleanedAssets.length > 0) {
      setAssets(cleanedAssets);
      saveCachedAssets(wallet.address, cleanedAssets);
    }
    setHistory(nextHistory);
    saveCachedHistory(wallet.address, nextHistory);
  }

  const requestQr = useMemo(() => {
    if (!wallet) return "";
    return buildPaymentRequest({
      address: wallet.address,
      asset: selectedAsset,
      amount: receiveAmount.trim() || undefined,
    });
  }, [wallet, selectedAsset, receiveAmount]);

  async function handleGenerate() {
    const created = await generateWallet();
    setWallet(created);
    setPinMode("create");
    setScreen("pin");
  }

  async function handleImport(mnemonic: string) {
    try {
      const imported = await importWallet(mnemonic);
      setWallet(imported);
      setPinMode("create");
      setScreen("pin");
    } catch {
      Alert.alert("Не удалось импортировать", "Проверьте сид-фразу и попробуйте снова.");
    }
  }

  async function handleUnlockPin(pin: string) {
    const stored = await loadPin();
    if (pinMode === "create") {
      await savePin(pin);
      setScreen("assets");
      return;
    }
    if (stored === pin) {
      setScreen("assets");
      return;
    }
    Alert.alert("Неверный PIN", "Попробуйте еще раз.");
  }

  async function handleBiometric() {
    if (!biometrics) return;
    const result = await LocalAuthentication.authenticateAsync({ promptMessage: "Вход в CandyWallet" });
    if (result.success) setScreen("assets");
  }

  async function scanQr() {
    const permission = cameraPermission?.granted ? cameraPermission : await requestCameraPermission();
    if (!permission.granted) {
      Alert.alert("Камера недоступна", "Разрешите доступ к камере для сканирования QR.");
      return;
    }
    setScannerOpen(true);
  }

  function onQrScanned(value: string) {
    const parsed = parsePaymentRequest(value);
    if (!parsed) {
      Alert.alert("QR не распознан", "Этот QR-код не похож на запрос оплаты.");
      return;
    }
    setPaymentRequest(parsed);
    setSendTo(parsed.address);
    setSendAmount(sanitizeDecimalInput(parsed.amount || ""));
    const found = assets.find((asset) => asset.symbol === parsed.token || asset.address === parsed.tokenAddress);
    if (found) setSelectedAssetId(found.id);
    setScannerOpen(false);
    setTransferTab("send");
    setScreen("transfer");
  }

  if (screen === "welcome") {
    return <WelcomeScreen onGenerate={handleGenerate} onImport={handleImport} />;
  }

  if (screen === "pin") {
    return <PinScreen mode={pinMode} onComplete={handleUnlockPin} onBiometric={pinMode === "unlock" ? handleBiometric : undefined} />;
  }

  const content = (() => {
    if (screen === "assets") {
      return <AssetsScreen assets={assets} wallet={wallet} loading={assetLoading} ratesLoading={ratesLoading} delRates={delRates} error={assetError} onSelectAsset={setSelectedAssetId} />;
    }
    if (screen === "swap") {
      return (
        <SwapScreen
          assets={assets}
          coins={swapCoins}
          selectedCoinId={selectedSwapCoinId}
          setSelectedCoinId={setSelectedSwapCoinId}
          swapping={swapping}
          loading={swapLoading}
          onPickAsset={() => {
            setAssetPickerReturn("swap");
            setScreen("assetPicker");
          }}
          onPickCoin={() => setScreen("coinPicker")}
          onSwap={async (coin, amount, direction) => {
            if (!wallet?.mnemonic || !coin.address) {
              Alert.alert("Обмен недоступен", "Выберите монету с доступным резервом.");
              return;
            }
            try {
              setSwapping(true);
              setTxOverlay({ visible: true, loading: true, kind: "info", title: "Отправляем обмен", message: "Считаем комиссию и отправляем транзакцию в сеть." });
              const result = direction === "buy"
                ? await client.buyTokenWithDel({ mnemonic: wallet.mnemonic, token: coin.address, amountDel: amount })
                : await client.sellTokenForDel({ mnemonic: wallet.mnemonic, token: coin.address, amount, decimals: 18 });
              setTxOverlay({ visible: true, loading: false, kind: "success", title: result.confirmed ? "Обмен выполнен" : "Обмен отправлен", message: `Комиссия: ${result.feeDel} DEL` });
              await refreshWalletData();
            } catch (error) {
              setTxOverlay({ visible: true, loading: false, kind: "error", title: "Обмен не выполнен", message: error instanceof Error ? error.message : "Проверьте сумму и попробуйте снова." });
            } finally {
              setSwapping(false);
            }
          }}
        />
      );
    }
    if (screen === "transfer") {
      return (
        <TransferScreen
          wallet={wallet}
          asset={selectedAsset}
          assets={assets}
          tab={transferTab}
          setTab={setTransferTab}
          sendTo={sendTo}
          setSendTo={setSendTo}
          sendAmount={sendAmount}
          setSendAmount={(value) => setSendAmount(sanitizeDecimalInput(value))}
          receiveAmount={receiveAmount}
          setReceiveAmount={(value) => setReceiveAmount(sanitizeDecimalInput(value))}
          requestQr={requestQr}
          onPickAsset={() => {
            setAssetPickerReturn("transfer");
            setScreen("assetPicker");
          }}
          onScan={scanQr}
          contacts={contacts}
          onSaveContact={async (address) => {
            if (!wallet || !address.startsWith("0x")) return;
            const exists = contacts.some((item) => item.address.toLowerCase() === address.toLowerCase());
            if (exists) {
              Alert.alert("Контакт уже есть", "Этот адрес уже сохранен.");
              return;
            }
            const next = [{ id: `${Date.now()}`, name: `Кошелек ${shortHash(address)}`, address }, ...contacts];
            setContacts(next);
            await saveContacts(wallet.address, next);
            Alert.alert("Контакт сохранен", "Адрес добавлен в записную книжку.");
          }}
          onPickContact={() => setScreen("contactPicker")}
          history={history}
          historyLoading={historyLoading}
          onSend={async () => {
            if (!wallet?.mnemonic) {
              Alert.alert("Кошелек недоступен", "Не удалось получить ключ для подписи.");
              return;
            }
            try {
              setSending(true);
              setTxOverlay({ visible: true, loading: true, kind: "info", title: "Отправляем транзакцию", message: "Считаем комиссию, проверяем баланс и ждем ответ сети." });
              const result = selectedAsset.type === "coin"
                ? await client.sendDel({ mnemonic: wallet.mnemonic, to: sendTo, amount: sendAmount })
                : await client.sendErc20({ mnemonic: wallet.mnemonic, token: selectedAsset.address || selectedAsset.id, to: sendTo, amount: sendAmount, decimals: selectedAsset.decimals });
              setTxOverlay({ visible: true, loading: false, kind: "success", title: result.confirmed ? "Транзакция выполнена" : "Транзакция отправлена", message: `Комиссия: ${result.feeDel} DEL` });
              setSendAmount("");
              await refreshWalletData();
            } catch (error) {
              setTxOverlay({ visible: true, loading: false, kind: "error", title: "Не удалось отправить", message: error instanceof Error ? error.message : "Проверьте данные и попробуйте снова." });
            } finally {
              setSending(false);
            }
          }}
          sending={sending}
          onOpenTx={(hash) => Linking.openURL(`https://explorer.decimalchain.com/transactions/${hash}`)}
        />
      );
    }
    if (screen === "stake") {
      return (
        <StakeScreen
          validators={validators}
          delegations={delegations}
          staking={staking}
          loading={stakeLoading}
          onStake={async (action, validator, amount) => {
            if (!wallet?.mnemonic) {
              Alert.alert("Кошелек недоступен", "Не удалось получить ключ для подписи.");
              return;
            }
            try {
              setStaking(true);
              setTxOverlay({ visible: true, loading: true, kind: "info", title: "Отправляем операцию", message: "Считаем комиссию и отправляем стейкинг-транзакцию." });
              if (action === "move") {
                throw new Error("Перемещение появится после подключения transfer stake метода в SDK.");
              }
              const result = action === "delegate"
                ? await client.delegateDel({ mnemonic: wallet.mnemonic, validator, amount })
                : await client.withdrawDel({ mnemonic: wallet.mnemonic, validator, amount });
              setTxOverlay({ visible: true, loading: false, kind: "success", title: result.confirmed ? "Операция выполнена" : "Операция отправлена", message: `Комиссия: ${result.feeDel} DEL` });
              await refreshWalletData();
              getDelegations(wallet.address, validators).then(setDelegations).catch(() => setDelegations([]));
            } catch (error) {
              setTxOverlay({ visible: true, loading: false, kind: "error", title: "Операция не выполнена", message: error instanceof Error ? error.message : "Проверьте сумму и попробуйте снова." });
            } finally {
              setStaking(false);
            }
          }}
        />
      );
    }
    if (screen === "settings") {
      return (
        <SettingsScreen
          lightTheme={lightTheme}
          setLightTheme={setLightTheme}
          biometrics={biometrics}
          setBiometrics={setBiometrics}
          language={language}
          setLanguage={setLanguage}
          onChangePin={() => {
            setChangePinStep("old");
            setScreen("changePin");
          }}
          onContacts={() => setScreen("contacts")}
          onAbout={() => setScreen("about")}
          onClear={async () => {
            await clearWallet();
            setWallet(null);
            setScreen("welcome");
          }}
        />
      );
    }
    if (screen === "transit") return <TransitScreen onBack={() => setScreen("stake")} />;
    if (screen === "contacts") return <ContactsScreen contacts={contacts} onBack={() => setScreen("settings")} onSelect={() => undefined} />;
    if (screen === "contactPicker") return <ContactsScreen contacts={contacts} onBack={() => setScreen("transfer")} onSelect={(contact) => { setSendTo(contact.address); setScreen("transfer"); }} />;
    if (screen === "about") return <SimpleScreen title="О приложении" onBack={() => setScreen("settings")} text="CandyWallet 0.1.4. Кошелек для сети Decimal от MintCandy." />;
    if (screen === "changePin") {
      return (
        <PinScreen
          mode={changePinStep === "old" ? "verify" : "create"}
          onComplete={async (pin) => {
            if (changePinStep === "old") {
              const stored = await loadPin();
              if (stored !== pin) {
                Alert.alert("Неверный PIN", "Введите текущий PIN еще раз.");
                return;
              }
              setChangePinStep("new");
              return;
            }
            await savePin(pin);
            Alert.alert("PIN обновлен", "Новый PIN-код сохранен.");
            setScreen("settings");
          }}
        />
      );
    }
    if (screen === "assetPicker") {
      return <AssetPicker assets={assets} selected={selectedAssetId} onSelect={(id) => { setSelectedAssetId(id); setScreen(assetPickerReturn); }} onBack={() => setScreen(assetPickerReturn)} />;
    }
    if (screen === "coinPicker") {
      return <CoinPicker coins={swapCoins} assets={assets} selected={selectedSwapCoinId} onSelect={(id) => { setSelectedSwapCoinId(id); setScreen("swap"); }} onBack={() => setScreen("swap")} />;
    }
    return null;
  })();

  return (
    <SafeAreaView style={styles.app}>
      <StatusBar style={lightTheme ? "dark" : "light"} />
      {scannerOpen ? <Scanner onClose={() => setScannerOpen(false)} onScanned={onQrScanned} /> : content}
      <TxOverlay state={txOverlay} onClose={() => setTxOverlay((current) => ({ ...current, visible: false }))} />
      <BlockingOverlay visible={dataLoading && !dataOverlayTimedOut} text="Обновление данных" />
      {dataNotice ? <NoticeBanner text={dataNotice} onClose={() => setDataNotice("")} /> : null}
      {!["assetPicker", "coinPicker", "transit", "changePin", "contacts", "contactPicker", "about"].includes(screen) && <TabBar current={screen} onChange={setScreen} />}
    </SafeAreaView>
  );
}

function WelcomeScreen({ onGenerate, onImport }: { onGenerate: () => void; onImport: (mnemonic: string) => void }) {
  const [mnemonic, setMnemonic] = useState("");
  return (
    <SafeAreaView style={styles.app}>
      <StatusBar style="light" />
      <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : undefined} style={styles.welcome}>
        <View style={styles.welcomeBrand}>
          <Logo size={96} />
          <View style={styles.brandTextBlock}>
            <Text style={styles.brandEyebrow}>from DecimalChain</Text>
            <Text style={styles.brandName}>CandyWallet</Text>
          </View>
        </View>
        <Text style={styles.hero}>Ваш Decimal-кошелек</Text>
        <Text style={styles.heroSub}>Импортируйте сид-фразу или создайте новый адрес для локального тестирования.</Text>
        <TextInput
          value={mnemonic}
          onChangeText={setMnemonic}
          placeholder="Сид-фраза"
          placeholderTextColor={colors.dim}
          autoCapitalize="none"
          multiline
          style={styles.seedInput}
        />
        <GradientButton title="Импортировать" disabled={mnemonic.trim().split(/\s+/).length < 12} onPress={() => onImport(mnemonic)} />
        <View style={styles.welcomeActions}>
          <Text style={styles.or}>или</Text>
          <GradientButton title="Создать кошелек" onPress={onGenerate} />
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

function PinScreen({ mode, onComplete, onBiometric }: { mode: "create" | "unlock" | "verify"; onComplete: (pin: string) => void; onBiometric?: () => void }) {
  const [pin, setPin] = useState("");
  function press(value: string) {
    const next = `${pin}${value}`.slice(0, 4);
    setPin(next);
    if (next.length === 4) {
      setTimeout(() => {
        onComplete(next);
        setPin("");
      }, 100);
    }
  }
  return (
    <SafeAreaView style={styles.app}>
      <StatusBar style="light" />
      <View style={styles.pinScreen}>
        <Text style={styles.pinTitle}>{mode === "create" ? "Создать ПИН-код" : "Введите ПИН-код"}</Text>
        <Text style={styles.pinSub}>{mode === "create" ? "Введите новый PIN" : mode === "verify" ? "Подтвердите текущий PIN" : "Разблокируйте кошелек"}</Text>
        <View style={styles.dots}>{[0, 1, 2, 3].map((dot) => <View key={dot} style={[styles.dot, dot < pin.length && styles.dotActive]} />)}</View>
        <View style={styles.keypad}>
          {"123456789".split("").map((number) => <PinKey key={number} label={number} onPress={() => press(number)} />)}
          <View />
          <PinKey label="0" onPress={() => press("0")} />
          <PinKey label="⌫" muted onPress={() => setPin(pin.slice(0, -1))} />
        </View>
        {onBiometric && <Pressable onPress={onBiometric}><Text style={styles.biometric}>Войти по отпечатку</Text></Pressable>}
      </View>
    </SafeAreaView>
  );
}

function PinKey({ label, muted, onPress }: { label: string; muted?: boolean; onPress: () => void }) {
  return (
    <Pressable onPress={onPress} style={styles.key}>
      <Text style={[styles.keyText, muted && { color: colors.dim }]}>{label}</Text>
    </Pressable>
  );
}

function AssetsScreen({
  assets,
  wallet,
  loading,
  error,
  delRates,
  ratesLoading,
  onSelectAsset,
}: {
  assets: Asset[];
  wallet: WalletAccount | null;
  loading: boolean;
  ratesLoading: boolean;
  delRates: DelFiatRates | null;
  error: string | null;
  onSelectAsset: (id: string) => void;
}) {
  const del = assets.find((asset) => asset.symbol.toUpperCase() === "DEL" || asset.id === "del") || fallbackAssets[0];
  const delBalance = Number(del.balance);
  const visibleTokens = assets.filter((asset) => asset.id !== "del" && asset.symbol.toUpperCase() !== "DEL" && asset.type !== "coin" && asset.balance !== "0");
  const fiatLine = formatDelFiat(delBalance, delRates, ratesLoading);
  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.scrollContent}>
      <View style={styles.pageTop}>
        <View>
          <Text style={[styles.title, styles.titleInline]}>Активы</Text>
        </View>
        <Logo size={38} />
      </View>
      <View style={styles.walletPanel}>
        <Text style={styles.balanceLabelDark}>{loading ? "Обновление данных" : "Основной баланс"}</Text>
        <Text style={styles.balanceDark}>{del.balance} DEL</Text>
        {fiatLine && <Text style={styles.fiatLine}>{fiatLine}</Text>}
      </View>
      {error && <Text style={styles.warningText}>{error}</Text>}
      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>Токены</Text>
        <Text style={styles.sectionMeta}>{visibleTokens.length}</Text>
      </View>
      {visibleTokens.length > 0 ? (
        visibleTokens.map((asset) => <AssetRow key={asset.id} asset={asset} onPress={() => onSelectAsset(asset.id)} />)
      ) : (
        <EmptyState
          title="Других токенов пока нет"
          text="Когда токены появятся на балансе, они будут показаны здесь."
        />
      )}
    </ScrollView>
  );
}

function SwapScreen({
  assets,
  coins,
  selectedCoinId,
  setSelectedCoinId,
  swapping,
  loading,
  onPickAsset,
  onPickCoin,
  onSwap,
}: {
  assets: Asset[];
  coins: SwapCoin[];
  selectedCoinId: string;
  setSelectedCoinId: (id: string) => void;
  swapping: boolean;
  loading: boolean;
  onPickAsset: () => void;
  onPickCoin: () => void;
  onSwap: (coin: SwapCoin, amount: string, direction: "buy" | "sell") => void;
}) {
  const [amount, setAmount] = useState("");
  const [fromDel, setFromDel] = useState(true);
  const selectedCoin = coins.find((coin) => coin.id === selectedCoinId) || coins.find((coin) => coin.symbol.toUpperCase() === "MINTCANDY") || coins[0];
  const tokenAsset = selectedCoin ? assets.find((asset) => asset.address?.toLowerCase() === selectedCoin.address?.toLowerCase() || asset.symbol === selectedCoin.symbol) : undefined;
  const estimate = selectedCoin?.priceDel ? (fromDel ? Number(amount || 0) / Number(selectedCoin.priceDel) : Number(amount || 0) * Number(selectedCoin.priceDel)) : 0;
  const canSwap = Boolean(selectedCoin?.address && selectedCoin.available && Number(amount) > 0 && !swapping);
  const delAsset = assets.find((asset) => asset.symbol === "DEL") || fallbackAssets[0];
  const estimatedAmount = Number(amount) > 0 ? formatSwapEstimate(estimate) : "0";
  const canInvert = Boolean(selectedCoin);
  useEffect(() => {
    if (!selectedCoin && !fromDel) setFromDel(true);
  }, [selectedCoin, fromDel]);
  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.scrollContent}>
      <Text style={styles.title}>Конвертация</Text>
      {fromDel ? (
        <SwapInputCard asset={delAsset} amount={amount} setAmount={setAmount} onPick={onPickAsset} onMax={() => setAmount(sanitizeDecimalInput(delAsset.balance))} />
      ) : selectedCoin ? (
        <SwapInputCoinCard coin={selectedCoin} amount={amount} balance={tokenAsset?.balance || "0"} setAmount={setAmount} onPick={onPickCoin} onMax={() => setAmount(sanitizeDecimalInput(tokenAsset?.balance || "0"))} />
      ) : null}
      <Pressable disabled={!canInvert} onPress={() => setFromDel((value) => !value)} style={[styles.swapCircle, !canInvert && { opacity: 0.45 }]}>
        <LinearGradient colors={gradients.primary} style={styles.swapCircleGradient}>
          <Repeat2 color={colors.white} size={24} />
        </LinearGradient>
      </Pressable>
      {fromDel
        ? selectedCoin && <SwapOutputCoinCard coin={selectedCoin} amount={estimatedAmount} balance={tokenAsset?.balance || "0"} onPick={onPickCoin} />
        : <SwapOutputAssetCard asset={delAsset} amount={estimatedAmount} onPick={onPickAsset} />}
      <GradientButton title={swapping ? "Отправляем" : "Продолжить"} disabled={!canSwap} onPress={() => selectedCoin && onSwap(selectedCoin, amount, fromDel ? "buy" : "sell")} style={{ marginTop: spacing.lg }} />
      {!loading && coins.length === 0 && <EmptyState title="Монеты не загружены" text="Откройте выбор монеты после обновления данных." />}
      {selectedCoin && !selectedCoin.available && <Text style={styles.warningText}>Для {selectedCoin.symbol} пока нет цены или резерва для обмена.</Text>}
    </ScrollView>
  );
}

function TransferScreen(props: {
  wallet: WalletAccount | null;
  asset: Asset;
  assets: Asset[];
  tab: "send" | "receive";
  setTab: (tab: "send" | "receive") => void;
  sendTo: string;
  setSendTo: (value: string) => void;
  sendAmount: string;
  setSendAmount: (value: string) => void;
  receiveAmount: string;
  setReceiveAmount: (value: string) => void;
  requestQr: string;
  onPickAsset: () => void;
  onScan: () => void;
  contacts: ContactItem[];
  onSaveContact: (address: string) => void;
  onPickContact: () => void;
  onSend: () => void;
  sending: boolean;
  history: TxHistoryItem[];
  historyLoading: boolean;
  onOpenTx: (hash: string) => void;
}) {
  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.scrollContent}>
      <Text style={styles.title}>Трансфер</Text>
      <View style={styles.segment}>
        <Pressable onPress={() => props.setTab("send")} style={[styles.segmentItem, props.tab === "send" && styles.segmentActive]}><Text style={styles.segmentText}>Отправить</Text></Pressable>
        <Pressable onPress={() => props.setTab("receive")} style={[styles.segmentItem, props.tab === "receive" && styles.segmentActive]}><Text style={styles.segmentText}>Получить</Text></Pressable>
      </View>
      {props.tab === "send" ? <SendPanel {...props} /> : <ReceivePanel {...props} />}
      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>История</Text>
        <Text style={styles.sectionMeta}>{props.historyLoading ? "..." : props.history.length}</Text>
      </View>
      {props.historyLoading ? <LoadingBlock text="Обновление данных" /> : props.history.length > 0 ? props.history.slice(0, 100).map((tx) => (
        <Pressable key={tx.hash} onPress={() => props.onOpenTx(tx.hash)} style={styles.txRow}>
          <View style={{ flex: 1 }}>
            <Text style={styles.assetSymbol}>{tx.type}</Text>
            <Text style={styles.muted}>{shortHash(tx.hash)} {tx.timestamp ? `· ${formatDate(tx.timestamp)}` : ""}</Text>
          </View>
          <Text style={styles.link}>{tx.status}</Text>
        </Pressable>
      )) : (
        <EmptyState title="История пуста" text="Последние операции появятся здесь после обновления." />
      )}
    </ScrollView>
  );
}

function SendPanel(props: Parameters<typeof TransferScreen>[0]) {
  const canSend = props.sendTo.startsWith("0x") && Number(props.sendAmount) > 0;
  return (
    <View style={styles.form}>
      <AssetCard asset={props.asset} onPress={props.onPickAsset} />
      {props.requestQr && props.sendTo && <Text style={styles.detected}>Запрос оплаты: {props.asset.symbol}</Text>}
      <View style={styles.inputLine}>
        <TextInput value={props.sendTo} onChangeText={props.setSendTo} placeholder="Кому" placeholderTextColor={colors.dim} style={styles.lineInput} />
        <Pressable onPress={props.onScan}><ScanLine color={colors.blue} size={28} /></Pressable>
      </View>
      <View style={styles.inputLine}>
        <TextInput value={props.sendAmount} onChangeText={props.setSendAmount} placeholder="Сумма" keyboardType="decimal-pad" placeholderTextColor={colors.dim} style={styles.lineInput} />
        <Pressable onPress={() => props.setSendAmount(sanitizeDecimalInput(props.asset.balance))}><Text style={styles.link}>MAX</Text></Pressable>
      </View>
      <View style={styles.sendRow}>
        <Pressable
          onPress={() => props.sendTo.startsWith("0x") ? props.onSaveContact(props.sendTo) : props.onPickContact()}
          style={styles.contactButton}
        >
          <UserPlus color={colors.blue} size={26} />
        </Pressable>
        <GradientButton title={props.sending ? "Отправляем" : "Отправить"} disabled={!canSend || props.sending} onPress={props.onSend} style={{ flex: 1 }} />
      </View>
    </View>
  );
}

function ReceivePanel(props: Parameters<typeof TransferScreen>[0]) {
  return (
    <ScrollView contentContainerStyle={styles.receive}>
      <AssetCard asset={props.asset} onPress={props.onPickAsset} compact />
      <TextInput value={props.receiveAmount} onChangeText={props.setReceiveAmount} placeholder="Сумма для QR (необязательно)" keyboardType="decimal-pad" placeholderTextColor={colors.dim} style={styles.amountInput} />
      <View style={styles.qrBox}><QRCode value={props.requestQr || "decimal:"} size={210} backgroundColor={colors.white} color="#000000" /></View>
      <Text style={styles.receiveTitle}>Ваш адрес</Text>
      <Pressable onPress={() => props.wallet?.address && Clipboard.setStringAsync(props.wallet.address)}>
        <Text style={styles.addressText}>{shortAddressFull(props.wallet?.address || "")}</Text>
      </Pressable>
      <Text style={styles.hint}>QR содержит адрес, токен {props.asset.symbol}{props.receiveAmount ? ` и сумму ${props.receiveAmount}` : ""}</Text>
      <Pressable style={styles.shareButton}><Share2 color={colors.white} size={24} /><Text style={styles.shareText}>Поделиться</Text></Pressable>
    </ScrollView>
  );
}

function StakeScreen({
  validators,
  delegations,
  staking,
  loading,
  onStake,
}: {
  validators: ValidatorSummary[];
  delegations: DelegationItem[];
  staking: boolean;
  loading: boolean;
  onStake: (action: "delegate" | "withdraw" | "move", validator: string, amount: string) => void;
}) {
  const [selectedValidator, setSelectedValidator] = useState("");
  const [amount, setAmount] = useState("");
  const [action, setAction] = useState<"delegate" | "withdraw" | "move">("delegate");
  const activeValidators = validators.filter((validator) => validator.active).slice(0, 6);
  const pickedValidator = activeValidators.find((validator) => validator.id === selectedValidator) || activeValidators[0];
  const delegated = delegations.reduce((sum, item) => sum + Number(item.amountDel || 0), 0);
  const canStake = Boolean(pickedValidator?.id && Number(amount) > 0 && !staking);
  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.scrollContent}>
      <View style={styles.pageTop}>
        <View>
          <Text style={[styles.title, styles.titleInline]}>Стейкинг</Text>
        </View>
        <Text style={styles.plus}>+</Text>
      </View>
      <View style={styles.walletPanel}>
        <Text style={styles.balanceLabelDark}>Делегировано</Text>
        <Text style={styles.balanceDark}>{trimDisplay(delegated)} DEL</Text>
        <Text style={styles.walletAddress}>Сумма ваших активных делегаций.</Text>
      </View>
      <Pressable style={styles.transitCard}>
        <View><Text style={styles.muted}>Транзитный баланс</Text><Text style={styles.tokenAmount}>0 DEL</Text></View>
        <ChevronRight color={colors.muted} />
      </Pressable>
      <View style={styles.walletPanel}>
        <View style={styles.bottomSegment}>
          <Pressable onPress={() => setAction("delegate")} style={[styles.bottomSegmentItem, action === "delegate" && styles.bottomSegmentActive]}><Text style={styles.segmentText}>Делегировать</Text></Pressable>
          <Pressable onPress={() => setAction("withdraw")} style={[styles.bottomSegmentItem, action === "withdraw" && styles.bottomSegmentActive]}><Text style={styles.segmentText}>Отозвать</Text></Pressable>
          <Pressable onPress={() => setAction("move")} style={[styles.bottomSegmentItem, action === "move" && styles.bottomSegmentActive]}><Text style={styles.segmentText}>Переместить</Text></Pressable>
        </View>
        <TextInput value={amount} onChangeText={(value) => setAmount(sanitizeDecimalInput(value))} placeholder="Сумма DEL" keyboardType="decimal-pad" placeholderTextColor={colors.dim} style={styles.amountInput} />
        {pickedValidator && <Text style={styles.walletAddress}>Валидатор: {pickedValidator.name}</Text>}
        <GradientButton title={staking ? "Отправляем" : action === "delegate" ? "Делегировать" : action === "withdraw" ? "Отозвать" : "Переместить"} disabled={!canStake} onPress={() => pickedValidator && onStake(action, pickedValidator.id, amount)} style={{ marginTop: spacing.md }} />
      </View>
      {loading ? <LoadingBlock text="Обновление данных" /> : delegations.length > 0 ? delegations.map((item) => (
        <View key={item.validator} style={styles.validatorCard}>
          <View style={styles.rowBetween}>
            <Text style={styles.validatorTitle}>{item.moniker}</Text>
            <Text style={styles.assetBalance}>{item.amountDel} {item.symbol}</Text>
          </View>
          <Text style={styles.muted}>Награда {item.rewardDel} DEL</Text>
        </View>
      )) : (
        <EmptyState title="Активных делегаций нет" text="Когда вы начнете делегировать монеты, список появится здесь." />
      )}
      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>Валидаторы</Text>
        <Text style={styles.sectionMeta}>{activeValidators.length}</Text>
      </View>
      {loading ? <LoadingBlock text="Обновление данных" /> : activeValidators.length > 0 ? activeValidators.map((validator) => (
        <Pressable key={validator.id} onPress={() => setSelectedValidator(validator.id)} style={[styles.validatorCard, pickedValidator?.id === validator.id && { borderColor: colors.blue }]}>
          <View style={styles.rowBetween}>
            <Text style={styles.validatorTitle}>{validator.name}</Text>
            <Text style={styles.link}>{validator.commission}</Text>
          </View>
          <Text style={styles.muted}>Стейк {validator.stakeDel} DEL</Text>
        </Pressable>
      )) : (
        <EmptyState title="Валидаторы загружаются" text="Список появится после обновления данных." />
      )}
    </ScrollView>
  );
}

function SettingsScreen(props: { lightTheme: boolean; setLightTheme: (value: boolean) => void; biometrics: boolean; setBiometrics: (value: boolean) => void; language: "ru" | "en"; setLanguage: (value: "ru" | "en") => void; onChangePin: () => void; onContacts: () => void; onAbout: () => void; onClear: () => void }) {
  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.scrollContent}>
      <Text style={styles.title}>Настройки</Text>
      <View style={styles.settingsGroup}>
        <SettingRow label="Язык" value={props.language === "ru" ? "Русский" : "English"} onPress={() => props.setLanguage(props.language === "ru" ? "en" : "ru")} />
        <SettingToggle label="Светлая тема" value={props.lightTheme} onChange={props.setLightTheme} />
      </View>
      <View style={styles.settingsGroup}>
        <SettingRow label="Вход по ПИН-коду" value="включен" />
        <SettingRow label="Изменить ПИН-код" onPress={props.onChangePin} />
        <SettingToggle label="Отпечаток пальца" value={props.biometrics} onChange={props.setBiometrics} />
      </View>
      <View style={styles.settingsGroup}>
        <SettingRow label="Список контактов" onPress={props.onContacts} />
        <SettingRow label="О приложении" value="0.1.4" onPress={props.onAbout} />
      </View>
      <Pressable onPress={props.onClear} style={styles.dangerButton}>
        <Trash2 color={colors.white} size={18} />
        <Text style={styles.dangerButtonText}>Удалить локальные данные</Text>
      </Pressable>
    </ScrollView>
  );
}

function SimpleScreen({ title, text, onBack }: { title: string; text: string; onBack: () => void }) {
  return (
    <View style={styles.screen}>
      <View style={styles.header}><Pressable onPress={onBack}><ArrowLeft color={colors.text} size={32} /></Pressable><Text style={styles.headerTitle}>{title}</Text><View style={{ width: 32 }} /></View>
      <EmptyState title={title} text={text} />
    </View>
  );
}

function ContactsScreen({ contacts, onBack, onSelect }: { contacts: ContactItem[]; onBack: () => void; onSelect: (contact: ContactItem) => void }) {
  return (
    <View style={styles.screen}>
      <View style={styles.header}><Pressable onPress={onBack}><ArrowLeft color={colors.text} size={32} /></Pressable><Text style={styles.headerTitle}>Контакты</Text><View style={{ width: 32 }} /></View>
      <ScrollView style={{ flex: 1 }}>
        {contacts.map((contact) => (
          <Pressable key={contact.id} onPress={() => onSelect(contact)} style={styles.assetRow}>
            <UserPlus color={colors.blue} size={26} />
            <View style={{ flex: 1 }}>
              <Text style={styles.assetSymbol}>{contact.name}</Text>
              <Text style={styles.muted}>{shortHash(contact.address)}</Text>
            </View>
          </Pressable>
        ))}
        {contacts.length === 0 && <EmptyState title="Контактов пока нет" text="На вкладке Транзакция введите адрес и нажмите кнопку контакта, чтобы сохранить кошелек." />}
      </ScrollView>
    </View>
  );
}

function AssetPicker({ assets, selected, onSelect, onBack }: { assets: Asset[]; selected: string; onSelect: (id: string) => void; onBack: () => void }) {
  const [tab, setTab] = useState<"coins" | "nft">("coins");
  const visible = assets.filter((asset) => tab === "coins" ? asset.type !== "nft" : asset.type === "nft");
  return (
    <View style={styles.screen}>
      <View style={styles.header}><Pressable onPress={onBack}><ArrowLeft color={colors.text} size={32} /></Pressable><Text style={styles.headerTitle}>Выберите актив</Text><View style={{ width: 32 }} /></View>
      <ScrollView style={{ flex: 1 }}>{visible.map((asset) => <AssetRow key={asset.id} asset={asset} selected={asset.id === selected} onPress={() => onSelect(asset.id)} />)}</ScrollView>
      <View style={styles.bottomSegment}>
        <Pressable onPress={() => setTab("coins")} style={[styles.bottomSegmentItem, tab === "coins" && styles.bottomSegmentActive]}><Text style={styles.segmentText}>Монеты</Text></Pressable>
        <Pressable onPress={() => setTab("nft")} style={[styles.bottomSegmentItem, tab === "nft" && styles.bottomSegmentActive]}><Text style={styles.segmentText}>NFT</Text></Pressable>
      </View>
    </View>
  );
}

function CoinPicker({ coins, assets, selected, onSelect, onBack }: { coins: SwapCoin[]; assets: Asset[]; selected: string; onSelect: (id: string) => void; onBack: () => void }) {
  const [query, setQuery] = useState("");
  const normalized = query.trim().toLowerCase();
  const visible = coins
    .filter((coin) => normalized.length === 0 || coin.symbol.toLowerCase().includes(normalized) || coin.name.toLowerCase().includes(normalized))
    .slice(0, 200);
  return (
    <View style={styles.screen}>
      <View style={styles.header}><Pressable onPress={onBack}><ArrowLeft color={colors.text} size={32} /></Pressable><Text style={styles.headerTitle}>Выберите монету</Text><View style={{ width: 32 }} /></View>
      <View style={styles.searchBox}>
        <Search color={colors.blue} size={20} />
        <TextInput value={query} onChangeText={setQuery} placeholder="Поиск" placeholderTextColor={colors.dim} autoCapitalize="characters" style={styles.searchInput} />
      </View>
      <ScrollView style={{ flex: 1 }}>
        {visible.map((coin) => {
          const walletAsset = assets.find((asset) => asset.address?.toLowerCase() === coin.address?.toLowerCase() || asset.symbol.toUpperCase() === coin.symbol.toUpperCase());
          const walletBalance = walletAsset?.balance || "0";
          return (
            <Pressable key={coin.id} onPress={() => onSelect(coin.id)} style={[styles.assetRow, selected === coin.id && { borderColor: colors.blue }]}>
              <AssetIcon symbol={coin.symbol} />
              <View style={{ flex: 1 }}>
                <Text style={styles.assetSymbol}>{coin.symbol}</Text>
                <Text style={styles.muted}>Цена {coin.priceDel || "0"} DEL · Резерв {coin.reserveDel}</Text>
              </View>
              <Text style={styles.assetBalance}>{walletBalance}</Text>
            </Pressable>
          );
        })}
        {visible.length === 0 && <EmptyState title="Монеты не найдены" text="Проверьте запрос или обновите список монет позже." />}
      </ScrollView>
    </View>
  );
}

function TransitScreen({ onBack }: { onBack: () => void }) {
  return (
    <View style={styles.screen}>
      <View style={styles.header}><Pressable onPress={onBack}><ArrowLeft color={colors.text} size={32} /></Pressable><Text style={styles.headerTitle}>Транзитный баланс</Text><View style={{ width: 32 }} /></View>
      <View style={{ flex: 1 }} />
      <View style={styles.bottomSegment}>
        <View style={[styles.bottomSegmentItem, styles.bottomSegmentActive]}><Text style={styles.segmentText}>Возврат</Text></View>
        <View style={styles.bottomSegmentItem}><Text style={styles.segmentText}>Перенос</Text></View>
      </View>
    </View>
  );
}

function Scanner({ onClose, onScanned }: { onClose: () => void; onScanned: (value: string) => void }) {
  const [locked, setLocked] = useState(false);
  return (
    <View style={styles.scanner}>
      <CameraView
        style={StyleSheet.absoluteFill}
        barcodeScannerSettings={{ barcodeTypes: ["qr"] }}
        onBarcodeScanned={({ data }) => {
          if (locked) return;
          setLocked(true);
          onScanned(data);
        }}
      />
      <Pressable onPress={onClose} style={styles.close}><X color={colors.white} size={28} /></Pressable>
      <View style={styles.scanFrame}><QrCode color={colors.white} size={220} /></View>
    </View>
  );
}

function AssetRow({ asset, selected, onPress }: { asset: Asset; selected?: boolean; onPress: () => void }) {
  return (
    <Pressable onPress={onPress} style={[styles.assetRow, selected && { borderColor: colors.blue }]}>
      <AssetIcon symbol={asset.symbol} />
      <Text style={styles.assetSymbol}>{asset.symbol}</Text>
      <Text style={styles.assetBalance}>{asset.balance}</Text>
    </Pressable>
  );
}

function AssetCard({ asset, onPress, compact }: { asset: Asset; onPress: () => void; compact?: boolean }) {
  return (
    <Pressable onPress={onPress} style={[styles.assetCard, compact && { height: 78 }]}>
      <AssetIcon symbol={asset.symbol} />
      <Text style={styles.assetSymbol}>{asset.symbol}</Text>
      <Text style={styles.assetBalance}>{asset.balance}</Text>
    </Pressable>
  );
}

function SwapInputCard({ asset, amount, setAmount, onPick, onMax }: { asset: Asset; amount: string; setAmount: (value: string) => void; onPick: () => void; onMax: () => void }) {
  return (
    <View style={styles.swapCard}>
      <View style={styles.rowBetween}>
        <View style={styles.row}><AssetIcon symbol={asset.symbol} /><Text style={styles.assetSymbol}>{asset.symbol}</Text></View>
        <Pressable onPress={onPick} style={styles.row}><Text style={styles.link}>Изменить</Text><ChevronRight color={colors.blue} /></Pressable>
      </View>
      <View style={styles.swapLineInput}>
        <TextInput value={amount} onChangeText={(value) => setAmount(sanitizeDecimalInput(value))} placeholder="0" keyboardType="decimal-pad" placeholderTextColor={colors.dim} style={styles.swapAmountInput} />
        <Pressable onPress={onMax}><Text style={styles.link}>MAX</Text></Pressable>
      </View>
      <Text style={styles.muted}>Баланс {asset.balance} {asset.symbol}</Text>
    </View>
  );
}

function SwapInputCoinCard({ coin, amount, balance, setAmount, onPick, onMax }: { coin: SwapCoin; amount: string; balance: string; setAmount: (value: string) => void; onPick: () => void; onMax: () => void }) {
  return (
    <View style={styles.swapCard}>
      <View style={styles.rowBetween}>
        <View style={styles.row}><AssetIcon symbol={coin.symbol} /><Text style={styles.assetSymbol}>{coin.symbol}</Text></View>
        <Pressable onPress={onPick} style={styles.row}><Text style={styles.link}>Изменить</Text><ChevronRight color={colors.blue} /></Pressable>
      </View>
      <View style={styles.swapLineInput}>
        <TextInput value={amount} onChangeText={(value) => setAmount(sanitizeDecimalInput(value))} placeholder="0" keyboardType="decimal-pad" placeholderTextColor={colors.dim} style={styles.swapAmountInput} />
        <Pressable onPress={onMax}><Text style={styles.link}>MAX</Text></Pressable>
      </View>
      <Text style={styles.muted}>Баланс {balance} {coin.symbol}</Text>
    </View>
  );
}

function SwapOutputAssetCard({ asset, amount, onPick }: { asset: Asset; amount: string; onPick: () => void }) {
  return (
    <View style={styles.swapCard}>
      <View style={styles.rowBetween}>
        <View style={styles.row}><AssetIcon symbol={asset.symbol} /><Text style={styles.assetSymbol}>{asset.symbol}</Text></View>
        <Pressable onPress={onPick} style={styles.row}><Text style={styles.link}>Изменить</Text><ChevronRight color={colors.blue} /></Pressable>
      </View>
      <Text style={styles.swapOutputText}>{amount}</Text>
      <Text style={styles.muted}>Баланс {asset.balance} {asset.symbol}</Text>
    </View>
  );
}

function SwapOutputCoinCard({ coin, amount, balance, onPick }: { coin: SwapCoin; amount: string; balance: string; onPick: () => void }) {
  return (
    <View style={styles.swapCard}>
      <View style={styles.rowBetween}>
        <View style={styles.row}><AssetIcon symbol={coin.symbol} /><Text style={styles.assetSymbol}>{coin.symbol}</Text></View>
        <Pressable onPress={onPick} style={styles.row}><Text style={styles.link}>Изменить</Text><ChevronRight color={colors.blue} /></Pressable>
      </View>
      <Text style={styles.swapOutputText}>{amount}</Text>
      <Text style={styles.muted}>Баланс {balance} {coin.symbol}</Text>
    </View>
  );
}

function SwapCard({ asset, onPick, max }: { asset: Asset; onPick: () => void; max?: boolean }) {
  return (
    <View style={styles.swapCard}>
      <View style={styles.rowBetween}>
        <View style={styles.row}><AssetIcon symbol={asset.symbol} /><Text style={styles.assetSymbol}>{asset.symbol}</Text></View>
        <Pressable onPress={onPick} style={styles.row}><Text style={styles.link}>Изменить</Text><ChevronRight color={colors.blue} /></Pressable>
      </View>
      <View style={styles.swapLine}>{max && <Text style={styles.link}>MAX</Text>}</View>
    </View>
  );
}

function SwapCoinCard({ coin, onPick }: { coin: SwapCoin; onPick: () => void }) {
  return (
    <View style={styles.swapCard}>
      <View style={styles.rowBetween}>
        <View style={styles.row}><AssetIcon symbol={coin.symbol} /><Text style={styles.assetSymbol}>{coin.symbol}</Text></View>
        <Pressable onPress={onPick} style={styles.row}><Text style={styles.link}>Изменить</Text><ChevronRight color={colors.blue} /></Pressable>
      </View>
      <View style={styles.swapLine}>
        <Text style={styles.muted}>Цена {coin.priceDel || "0"} DEL</Text>
      </View>
    </View>
  );
}

function SettingRow({ label, value, onPress }: { label: string; value?: string; onPress?: () => void }) {
  const content = <><Text style={styles.settingLabel}>{label}</Text><View style={styles.row}>{value && <Text style={styles.settingValue}>{value}</Text>}<ChevronRight color={colors.dim} /></View></>;
  if (onPress) return <Pressable onPress={onPress} style={styles.settingRow}>{content}</Pressable>;
  return <View style={styles.settingRow}>{content}</View>;
}

function SettingToggle({ label, value, onChange }: { label: string; value: boolean; onChange: (value: boolean) => void }) {
  return <View style={styles.settingRow}><Text style={styles.settingLabel}>{label}</Text><Switch value={value} onValueChange={onChange} trackColor={{ false: colors.dim, true: colors.blue }} thumbColor={colors.muted} /></View>;
}

function EmptyState({ title, text }: { title: string; text: string }) {
  return (
    <View style={styles.emptyState}>
      <Text style={styles.emptyTitle}>{title}</Text>
      <Text style={styles.emptyText}>{text}</Text>
    </View>
  );
}

function LoadingBlock({ text }: { text: string }) {
  return (
    <View style={styles.loadingBlock}>
      <ActivityIndicator color={colors.blue} />
      <Text style={styles.emptyText}>{text}</Text>
    </View>
  );
}

function TxOverlay({ state, onClose }: { state: { visible: boolean; loading: boolean; title: string; message: string; kind: "info" | "success" | "error" }; onClose: () => void }) {
  return (
    <Modal transparent visible={state.visible} animationType="fade" onRequestClose={state.loading ? undefined : onClose}>
      <View style={styles.modalBackdrop}>
        <View style={styles.txModal}>
          <View style={[styles.txStatusIcon, state.kind === "error" && styles.txStatusError, state.kind === "success" && styles.txStatusSuccess]}>
            {state.loading ? <ActivityIndicator color={colors.white} /> : <Text style={styles.txStatusMark}>{state.kind === "error" ? "!" : "✓"}</Text>}
          </View>
          <Text style={styles.txModalTitle}>{state.title}</Text>
          <Text style={styles.txModalText}>{state.message}</Text>
          {!state.loading && <GradientButton title="Готово" onPress={onClose} style={{ alignSelf: "stretch", marginTop: spacing.md }} />}
        </View>
      </View>
    </Modal>
  );
}

function BlockingOverlay({ visible, text }: { visible: boolean; text: string }) {
  const rotate = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    if (!visible) {
      rotate.stopAnimation();
      rotate.setValue(0);
      return undefined;
    }
    const animation = Animated.loop(
      Animated.timing(rotate, {
        toValue: 1,
        duration: 2200,
        easing: Easing.linear,
        useNativeDriver: true,
      }),
    );
    animation.start();
    return () => animation.stop();
  }, [rotate, visible]);

  const spin = rotate.interpolate({ inputRange: [0, 1], outputRange: ["0deg", "360deg"] });

  return (
    <Modal transparent visible={visible} animationType="fade">
      <View style={styles.blockingBackdrop}>
        <View style={styles.blockingBox} pointerEvents="none">
          <View style={styles.candyLoader}>
            <Animated.View style={[styles.candyLoaderOrbit, { transform: [{ rotate: spin }] }]}>
              {Array.from({ length: 12 }).map((_, index) => {
                const angle = `${index * 30}deg`;
                return (
                  <View
                    key={index}
                    style={[
                      styles.candyLoaderDot,
                      {
                        opacity: 0.35 + index * 0.045,
                        transform: [{ rotate: angle }, { translateX: 46 }, { rotate: `-${angle}` }],
                      },
                    ]}
                  />
                );
              })}
            </Animated.View>
            <LinearGradient colors={gradients.primary} style={styles.candyLoaderRing}>
              <View style={styles.candyLoaderLogo}>
                <Image source={require("./assets/preloader-avatar.png")} resizeMode="cover" style={styles.candyLoaderAvatar} />
              </View>
            </LinearGradient>
          </View>
          <WaveText text={text} />
        </View>
      </View>
    </Modal>
  );
}

function WaveText({ text }: { text: string }) {
  const letters = useMemo(() => Array.from(text), [text]);
  const values = useRef<Animated.Value[]>([]);
  if (values.current.length !== letters.length) {
    values.current = letters.map((_, index) => values.current[index] || new Animated.Value(0));
  }

  useEffect(() => {
    const animations = letters.map((_, index) => {
      const value = values.current[index];
      return Animated.loop(
        Animated.sequence([
          Animated.delay(index * 70),
          Animated.timing(value, { toValue: 1, duration: 420, easing: Easing.inOut(Easing.quad), useNativeDriver: false }),
          Animated.timing(value, { toValue: 0, duration: 420, easing: Easing.inOut(Easing.quad), useNativeDriver: false }),
          Animated.delay(Math.max(0, (letters.length - index) * 70)),
        ]),
      );
    });
    animations.forEach((animation) => animation.start());
    return () => animations.forEach((animation) => animation.stop());
  }, [letters]);

  return (
    <View style={styles.waveTextRow}>
      {letters.map((letter, index) => {
        const value = values.current[index] || new Animated.Value(0);
        const color = value.interpolate({ inputRange: [0, 1], outputRange: [colors.success, colors.blue] });
        const translateY = value.interpolate({ inputRange: [0, 1], outputRange: [0, -7] });
        return (
          <Animated.Text key={`${letter}-${index}`} style={[styles.blockingText, { color, transform: [{ translateY }] }]}>
            {letter === " " ? "\u00A0" : letter}
          </Animated.Text>
        );
      })}
    </View>
  );
}

function NoticeBanner({ text, onClose }: { text: string; onClose: () => void }) {
  useEffect(() => {
    const timer = setTimeout(onClose, 4500);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <View style={styles.noticeBanner}>
      <Text style={styles.noticeText}>{text}</Text>
      <Pressable onPress={onClose} hitSlop={12}>
        <X color={colors.white} size={18} />
      </Pressable>
    </View>
  );
}

function shortAddressFull(address: string): string {
  if (address.length < 20) return address;
  return `${address.slice(0, 18)}\n${address.slice(18)}`;
}

function formatDelFiat(balance: number, rates: DelFiatRates | null, loading: boolean): string | null {
  if (loading && !rates) return "Обновление данных";
  if (!rates?.usd && !rates?.rub) return null;
  const parts: string[] = [];
  if (rates.usd) parts.push(`$${formatFiat(balance * rates.usd, "usd")}`);
  if (rates.rub) parts.push(`${formatFiat(balance * rates.rub, "rub")} ₽`);
  const change = rates.change24 === null ? "" : ` · 24ч ${rates.change24 > 0 ? "+" : ""}${rates.change24.toFixed(2)}%`;
  return `${parts.join(" / ")}${change}`;
}

function formatFiat(value: number, currency: "usd" | "rub"): string {
  if (!Number.isFinite(value)) return "0";
  const digits = currency === "usd" ? 4 : 2;
  return value.toLocaleString("ru-RU", {
    maximumFractionDigits: digits,
    minimumFractionDigits: value > 0 && value < 1 ? digits : 2,
  });
}

function shortHash(hash: string): string {
  if (hash.length < 16) return hash;
  return `${hash.slice(0, 8)}...${hash.slice(-6)}`;
}

function formatDate(value: string): string {
  const numeric = Number(value);
  const date = Number.isFinite(numeric)
    ? new Date(numeric < 1000000000000 ? numeric * 1000 : numeric)
    : new Date(value);
  if (Number.isNaN(date.getTime())) return "";
  return date.toLocaleDateString("ru-RU", { day: "2-digit", month: "2-digit", year: "2-digit" });
}

function trimDisplay(value: number): string {
  if (!Number.isFinite(value)) return "0";
  return value.toLocaleString("ru-RU", { maximumFractionDigits: 4 });
}

function formatSwapEstimate(value: number): string {
  if (!Number.isFinite(value) || value <= 0) return "0";
  const precision = value < 1 ? 8 : 4;
  return value.toFixed(precision).replace(/0+$/, "").replace(/\.$/, "");
}

function sanitizeDecimalInput(value: string): string {
  const normalized = value.replace(",", ".").replace(/[^0-9.]/g, "");
  const [whole, ...rest] = normalized.split(".");
  const fraction = rest.join("");
  if (normalized.startsWith(".")) return fraction ? `0.${fraction}` : "0.";
  return rest.length > 0 ? `${whole || "0"}.${fraction}` : whole;
}

function filterSupportedAssets(items: Asset[]): Asset[] {
  return items.filter((asset) => {
    if (asset.symbol.toUpperCase() === "DEL" || asset.id === "del") return true;
    return asset.type === "erc20" && Boolean(asset.address?.toLowerCase().startsWith("0x"));
  });
}

function normalizeAssets(items: Asset[]): Asset[] {
  return filterSupportedAssets(items).sort((a, b) => {
    const aDel = a.symbol.toUpperCase() === "DEL" || a.id === "del";
    const bDel = b.symbol.toUpperCase() === "DEL" || b.id === "del";
    if (aDel && !bDel) return -1;
    if (!aDel && bDel) return 1;
    const priority = ["MINTCANDY"];
    const ai = priority.indexOf(a.symbol.toUpperCase());
    const bi = priority.indexOf(b.symbol.toUpperCase());
    if (ai !== -1 || bi !== -1) {
      if (ai === -1) return 1;
      if (bi === -1) return -1;
      return ai - bi;
    }
    return a.symbol.localeCompare(b.symbol, "ru");
  });
}

function hasUsableAssets(items: Asset[]): boolean {
  return items.some((asset) => Number(asset.balance) > 0);
}

const fallbackAssets: Asset[] = [
  { id: "del", type: "coin", symbol: "DEL", name: "Decimal", balance: "0", decimals: 18 },
];

let styles = createStyles();

function createStyles() {
  return StyleSheet.create({
  addressText: { color: colors.text, fontSize: 18, lineHeight: 28, textAlign: "center" },
  amountInput: { borderBottomColor: colors.line, borderBottomWidth: 1, color: colors.text, fontSize: 18, height: 54, minWidth: "100%", textAlign: "center" },
  app: { backgroundColor: colors.bg, flex: 1 },
  assetBalance: { color: colors.text, fontSize: 20, fontWeight: "700", marginLeft: "auto" },
  assetCard: { alignItems: "center", backgroundColor: colors.panel, borderRadius: radii.md, flexDirection: "row", gap: 14, height: 92, paddingHorizontal: 22 },
  assetRow: { alignItems: "center", backgroundColor: colors.panel, borderColor: colors.line, borderRadius: radii.md, borderWidth: 1, flexDirection: "row", gap: 14, height: 92, marginBottom: 14, paddingHorizontal: 22 },
  assetSymbol: { color: colors.text, fontSize: 20, fontWeight: "800" },
  balance: { color: colors.white, fontSize: 30, fontWeight: "900", marginTop: 10 },
  balanceDark: { color: colors.text, fontSize: 34, fontWeight: "900", marginTop: 10 },
  balanceCard: { borderRadius: radii.md, height: 118, justifyContent: "center", marginBottom: 28, paddingHorizontal: 28 },
  balanceLabel: { color: colors.white, fontSize: 16, fontWeight: "700" },
  balanceLabelDark: { color: colors.muted, fontSize: 14, fontWeight: "800", textTransform: "uppercase" },
  biometric: { color: colors.blue, fontSize: 16, fontWeight: "700", marginTop: 20, textAlign: "center" },
  blockingBackdrop: { alignItems: "center", backgroundColor: "rgba(0,0,0,0.46)", flex: 1, justifyContent: "center" },
  blockingBox: { alignItems: "center", gap: 18, justifyContent: "center", minWidth: 220, paddingHorizontal: 24, paddingVertical: 22 },
  blockingText: { color: colors.text, fontSize: 17, fontWeight: "800", textAlign: "center" },
  bottomSegment: { backgroundColor: colors.tab, borderRadius: radii.sm, flexDirection: "row", gap: 4, marginBottom: 20, padding: 4 },
  bottomSegmentActive: { backgroundColor: colors.blue },
  bottomSegmentItem: { alignItems: "center", borderRadius: radii.sm, flex: 1, height: 48, justifyContent: "center" },
  close: { position: "absolute", right: 20, top: 52, zIndex: 2 },
  coinRow: { alignItems: "center", backgroundColor: colors.panel, borderColor: colors.line, borderRadius: radii.md, borderWidth: 1, flexDirection: "row", justifyContent: "space-between", marginBottom: 12, padding: 18 },
  contactButton: { alignItems: "center", backgroundColor: colors.panel, borderRadius: radii.md, height: 64, justifyContent: "center", width: 70 },
  candyLoader: { alignItems: "center", height: 118, justifyContent: "center", width: 118 },
  candyLoaderDot: { backgroundColor: colors.cyan, borderRadius: 6, height: 12, left: 53, position: "absolute", top: 53, width: 12 },
  candyLoaderAvatar: { height: 84, width: 84 },
  candyLoaderLogo: { alignItems: "center", backgroundColor: colors.white, borderRadius: 42, height: 84, justifyContent: "center", overflow: "hidden", width: 84 },
  candyLoaderOrbit: { height: 118, left: 0, position: "absolute", top: 0, width: 118 },
  candyLoaderRing: { alignItems: "center", borderRadius: 47, height: 94, justifyContent: "center", padding: 4, width: 94 },
  dangerButton: { alignItems: "center", backgroundColor: colors.danger, borderRadius: radii.md, flexDirection: "row", gap: 10, height: 56, justifyContent: "center", marginTop: 8 },
  dangerButtonText: { color: colors.white, fontSize: 16, fontWeight: "900" },
  dangerRow: { alignItems: "center", flexDirection: "row", gap: 8, marginTop: 18 },
  dangerText: { color: colors.danger, fontSize: 17, marginTop: 18 },
  detected: { color: colors.success, fontSize: 13, fontWeight: "700" },
  dim: { color: colors.dim },
  dot: { backgroundColor: colors.dim, borderRadius: 10, height: 20, width: 20 },
  dotActive: { backgroundColor: colors.blue },
  dots: { flexDirection: "row", gap: 22, justifyContent: "center", marginBottom: 58, marginTop: 72 },
  emptyState: { backgroundColor: colors.panel, borderColor: colors.line, borderRadius: radii.md, borderWidth: 1, gap: 10, padding: 22 },
  emptyText: { color: colors.muted, fontSize: 15, lineHeight: 22 },
  emptyTitle: { color: colors.text, fontSize: 18, fontWeight: "900" },
  form: { gap: 28, marginTop: 28 },
  fiatLine: { color: colors.cyan, fontSize: 15, fontWeight: "800", marginTop: 8 },
  header: { alignItems: "center", flexDirection: "row", justifyContent: "space-between", marginBottom: 34 },
  headerTitle: { color: colors.text, fontSize: 22, fontWeight: "800" },
  hero: { color: colors.text, fontSize: 34, fontWeight: "900", lineHeight: 42, marginTop: 34 },
  heroSub: { color: colors.muted, fontSize: 16, lineHeight: 24, marginTop: 12 },
  hint: { color: colors.muted, fontSize: 15, marginTop: 20, textAlign: "center" },
  inputLine: { alignItems: "center", borderBottomColor: colors.line, borderBottomWidth: 1, flexDirection: "row", height: 70 },
  key: { alignItems: "center", flexBasis: "33.333%", height: 102, justifyContent: "center" },
  keyText: { color: colors.text, fontSize: 44, fontWeight: "800" },
  keypad: { alignSelf: "stretch", flexDirection: "row", flexWrap: "wrap", justifyContent: "center", rowGap: 12, width: "100%" },
  lineInput: { color: colors.text, flex: 1, fontSize: 20 },
  link: { color: colors.blue, fontSize: 17, fontWeight: "800" },
  loadingBlock: { alignItems: "center", backgroundColor: colors.panel, borderColor: colors.line, borderRadius: radii.md, borderWidth: 1, gap: 12, padding: 22 },
  brandEyebrow: { color: colors.cyan, fontSize: 12, fontWeight: "900", letterSpacing: 0, textTransform: "uppercase" },
  brandName: { color: colors.text, fontSize: 28, fontWeight: "900", marginTop: 4 },
  brandTextBlock: { flex: 1, justifyContent: "center" },
  kicker: { color: colors.cyan, fontSize: 12, fontWeight: "900", letterSpacing: 0, marginBottom: 8, textTransform: "uppercase" },
  muted: { color: colors.muted, fontSize: 14 },
  noticeBanner: { alignItems: "center", alignSelf: "center", backgroundColor: colors.danger, borderRadius: radii.md, bottom: 88, flexDirection: "row", gap: 12, justifyContent: "space-between", left: 18, paddingHorizontal: 16, paddingVertical: 13, position: "absolute", right: 18, zIndex: 20 },
  noticeText: { color: colors.white, flex: 1, fontSize: 15, fontWeight: "800" },
  modalBackdrop: { alignItems: "center", backgroundColor: "rgba(0,0,0,0.62)", flex: 1, justifyContent: "center", padding: 24 },
  or: { color: colors.dim, fontSize: 18, fontWeight: "800", marginVertical: 26, textAlign: "center", textTransform: "uppercase" },
  pinScreen: { flex: 1, paddingHorizontal: 22, paddingTop: 28 },
  pinSub: { color: colors.text, fontSize: 18, marginTop: 20, textAlign: "center" },
  pinTitle: { color: colors.text, fontSize: 36, fontWeight: "900", textAlign: "center" },
  plus: { color: colors.blue, fontSize: 42, fontWeight: "300" },
  qrBox: { alignItems: "center", backgroundColor: colors.white, borderRadius: radii.sm, marginTop: 26, padding: 10 },
  receive: { alignItems: "center", gap: 10, paddingTop: 26 },
  receiveTitle: { color: colors.text, fontSize: 20, fontWeight: "800", marginTop: 20 },
  row: { alignItems: "center", flexDirection: "row", gap: 12 },
  rowBetween: { alignItems: "center", flexDirection: "row", justifyContent: "space-between" },
  scanFrame: { alignItems: "center", flex: 1, justifyContent: "center" },
  scanner: { backgroundColor: colors.black, flex: 1 },
  searchBox: { alignItems: "center", backgroundColor: colors.panel, borderColor: colors.line, borderRadius: radii.md, borderWidth: 1, flexDirection: "row", gap: 12, height: 60, marginBottom: 26, paddingHorizontal: 18 },
  searchInput: { color: colors.text, flex: 1, fontSize: 18 },
  screen: { backgroundColor: colors.bg, flex: 1, paddingHorizontal: 24, paddingTop: 42 },
  scrollContent: { paddingBottom: 28 },
  sectionHeader: { alignItems: "center", flexDirection: "row", justifyContent: "space-between", marginBottom: 14, marginTop: 26 },
  sectionMeta: { color: colors.muted, fontSize: 16, fontWeight: "800" },
  sectionTitle: { color: colors.text, fontSize: 22, fontWeight: "700" },
  seedInput: { borderBottomColor: colors.line, borderBottomWidth: 1, color: colors.text, fontSize: 18, minHeight: 74, marginBottom: 38, marginTop: 48 },
  segment: { borderBottomColor: colors.line, borderBottomWidth: 1, flexDirection: "row", marginHorizontal: -24 },
  segmentActive: { borderBottomColor: colors.blue, borderBottomWidth: 2 },
  segmentItem: { alignItems: "center", flex: 1, height: 44, justifyContent: "center" },
  segmentText: { color: colors.text, fontSize: 18, fontWeight: "800" },
  sendRow: { flexDirection: "row", gap: 18 },
  settingLabel: { color: colors.text, fontSize: 17 },
  settingRow: { alignItems: "center", flexDirection: "row", height: 58, justifyContent: "space-between" },
  settingValue: { color: colors.dim, fontSize: 17 },
  settingsGroup: { backgroundColor: colors.panel, borderColor: colors.line, borderRadius: radii.md, borderWidth: 1, marginBottom: 16, paddingHorizontal: 18 },
  shareButton: { alignItems: "center", backgroundColor: "#676c75", borderRadius: radii.sm, flexDirection: "row", gap: 12, height: 52, justifyContent: "center", marginTop: 12, paddingHorizontal: 18 },
  shareText: { color: colors.white, fontSize: 20, fontWeight: "800" },
  stakeTop: { borderRadius: radii.md, height: 108, justifyContent: "center", paddingHorizontal: 22 },
  swapCard: { backgroundColor: colors.panel, borderRadius: radii.md, height: 170, justifyContent: "space-between", padding: 22 },
  swapCircle: { alignItems: "center", alignSelf: "center", backgroundColor: colors.bg, borderColor: colors.line, borderRadius: 34, borderWidth: 1, height: 68, justifyContent: "center", marginVertical: -22, padding: 5, width: 68, zIndex: 2 },
  swapCircleGradient: { alignItems: "center", borderRadius: 28, height: 56, justifyContent: "center", width: 56 },
  swapIcon: { color: colors.dim, fontSize: 34, fontWeight: "800" },
  swapAmountInput: { color: colors.text, flex: 1, fontSize: 22, fontWeight: "700", minHeight: 48 },
  swapLine: { alignItems: "flex-end", borderTopColor: colors.line, borderTopWidth: 1, height: 44, justifyContent: "center" },
  swapLineInput: { alignItems: "center", borderBottomColor: colors.line, borderBottomWidth: 1, flexDirection: "row", minHeight: 56 },
  swapOutputText: { borderBottomColor: colors.line, borderBottomWidth: 1, color: colors.text, fontSize: 22, fontWeight: "800", minHeight: 56, paddingTop: 14 },
  title: { color: colors.text, fontSize: 40, fontWeight: "900", marginBottom: 28 },
  titleInline: { marginBottom: 0 },
  tokenAmount: { color: colors.text, fontSize: 17, fontWeight: "700" },
  transitCard: { alignItems: "center", backgroundColor: colors.panel, borderColor: colors.line, borderRadius: radii.md, borderWidth: 1, flexDirection: "row", justifyContent: "space-between", marginBottom: 30, padding: 20 },
  txRow: { alignItems: "center", backgroundColor: colors.panel, borderColor: colors.line, borderRadius: radii.md, borderWidth: 1, flexDirection: "row", gap: 12, marginBottom: 12, padding: 16 },
  txModal: { alignItems: "center", backgroundColor: colors.panel, borderColor: colors.line, borderRadius: radii.lg, borderWidth: 1, gap: 12, padding: 24, width: "100%" },
  txModalText: { color: colors.muted, fontSize: 16, lineHeight: 22, textAlign: "center" },
  txModalTitle: { color: colors.text, fontSize: 24, fontWeight: "900", textAlign: "center" },
  txStatusError: { backgroundColor: colors.danger },
  txStatusIcon: { alignItems: "center", backgroundColor: colors.blue, borderRadius: 28, height: 56, justifyContent: "center", width: 56 },
  txStatusMark: { color: colors.white, fontSize: 30, fontWeight: "900" },
  txStatusSuccess: { backgroundColor: colors.success },
  validatorCard: { backgroundColor: colors.panel, borderColor: colors.line, borderRadius: radii.md, borderWidth: 1, gap: 16, padding: 22 },
  validatorCoin: { color: colors.muted, fontSize: 17, letterSpacing: 0 },
  validatorIcon: { backgroundColor: colors.blue, borderBottomColor: "#ef2f41", borderLeftColor: "#ffc400", borderRadius: 25, borderRightColor: colors.purple, borderTopColor: "#0db8d7", borderWidth: 12, height: 50, width: 50 },
  validatorTitle: { color: colors.text, fontSize: 22, fontWeight: "800" },
  warningText: { color: colors.danger, fontSize: 14, fontWeight: "700", lineHeight: 20, marginTop: 12 },
  walletAddress: { color: colors.muted, fontSize: 15, fontWeight: "700", marginTop: 14 },
  walletPanel: { backgroundColor: colors.panel, borderColor: colors.line, borderRadius: radii.lg, borderWidth: 1, padding: 22 },
  waveTextRow: { alignItems: "center", flexDirection: "row", justifyContent: "center", minHeight: 30 },
  welcome: { flex: 1, justifyContent: "center", paddingHorizontal: 22 },
  welcomeActions: { gap: 0 },
  welcomeBrand: { alignItems: "center", flexDirection: "row", gap: 16 },
  walletTitle: { alignItems: "center", flexDirection: "row", gap: 6, marginBottom: 28 },
  pageTop: { alignItems: "center", flexDirection: "row", justifyContent: "space-between", marginBottom: 22 },
  });
}
