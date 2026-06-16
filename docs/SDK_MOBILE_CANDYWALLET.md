# CandyWallet Android App

Path:

```text
dw
```

App name:

```text
CandyWallet
```

Android package:

```text
ru.mintcandy.decimalwallet
```

## Назначение

CandyWallet это первый Android-first кошелек поверх нашего Decimal SDK/API.

Цели:

- красивый темный UI на базе референсов Decimal Wallet;
- бренд MintCandy/CandyWallet;
- импорт и генерация кошелька;
- PIN и биометрия;
- активы DEL/ERC20/NFT;
- перевод и получение;
- QR не только для адреса, но и для payment request: адрес + токен + сумма + memo;
- конвертация;
- стейкинг;
- настройки.

## Технологии

- Expo 53.
- React Native 0.79.
- React 19.
- TypeScript.
- `viem` для Decimal RPC.
- `expo-secure-store` для локального хранения.
- `expo-local-authentication` для биометрии.
- `expo-camera` для QR scanner.
- `react-native-qrcode-svg` для QR генерации.

## Установка

```powershell
cd dw
npm install
```

## Проверка

```powershell
npm run typecheck
npx expo config --type public
```

## Запуск dev server

```powershell
cd dw
npm run start
```

Текущий Metro URL:

```text
http://localhost:8081
```

## Android запуск

Через Expo/Dev Client:

```powershell
npm run android
```

Для локальной APK-сборки:

```powershell
$env:ANDROID_HOME="$env:LOCALAPPDATA\Android\Sdk"
$env:ANDROID_SDK_ROOT="$env:LOCALAPPDATA\Android\Sdk"
npx expo prebuild --platform android
cd android
.\gradlew.bat assembleRelease
```

Ожидаемый APK:

```text
dw/android/app/build/outputs/apk/release/app-release.apk
```

Текущая собранная копия релиза:

```text
dw/releases/CandyWallet-0.1.0-release.apk
```

Debug APK:

```text
dw/releases/CandyWallet-0.1.0-debug.apk
```

Debug APK:

```powershell
cd android
.\gradlew.bat assembleDebug
```

Ожидаемый файл:

```text
dw/android/app/build/outputs/apk/debug/app-debug.apk
```

## QR формат

CandyWallet использует payment request URI:

```text
decimal:0xAddress?token=DEL&amount=1.25&memo=optional
```

Для ERC20:

```text
decimal:0xAddress?token=BYACADEMY&tokenAddress=0xToken&amount=2.25
```

Это позволяет:

- выбрать токен на экране получения;
- указать сумму;
- показать QR;
- отсканировать QR на другом устройстве;
- автоматически заполнить адрес, токен и сумму на отправке.

## Логотип

Основной логотип:

```text
dw/assets/candywallet-logo.png
```

Источник:

```text
C:\Users\Maximus\Downloads\1774601725.png
```

Splash:

```text
dw/assets/splash.png
```

Источник:

```text
C:\Users\Maximus\Downloads\1774602074b275.png
```

## Текущий статус

Готово:

- Expo проект.
- CandyWallet branding.
- icon/splash assets.
- welcome screen.
- seed import/generate.
- PIN screen.
- secure storage skeleton.
- biometrics hook.
- assets screen.
- swap screen.
- transfer send/receive.
- QR генерация с token/amount.
- QR scanner hook.
- staking screen mock.
- settings screen.
- Decimal mobile API layer.
- TypeScript check.
- Native Android project через Expo prebuild.
- Debug APK.
- Release APK для тестирования.

Сборка APK выполнена с локальным JDK 17:

```text
dw/.jdk17/jdk-17.0.19+10
```

Проверка APK:

```text
apksigner verify: passed
package: ru.mintcandy.decimalwallet
versionName: 0.1.0
versionCode: 1
minSdkVersion: 24
targetSdkVersion: 35
```

Осталось:

- production-grade key derivation/backup flow;
- реальная отправка транзакций из мобильного UI;
- подключить full token list из API;
- NFT gallery;
- validator list из API;
- transaction history;
- UX для fee preview перед отправкой;
- release signing keystore;
- Play Store metadata.

Важно: текущий `app-release.apk` подписан debug signing config из prebuild. Для публикации в Play Store нужно создать production keystore и пересобрать release/AAB.
