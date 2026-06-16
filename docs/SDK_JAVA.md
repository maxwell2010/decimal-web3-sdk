# Java / Android SDK

Package:

```text
ru.mintcandy.decimal
```

Path:

```text
packages/java
```

## Назначение

Java SDK является JVM/Android-слоем для Decimal:

- Android native apps;
- JVM backend services;
- desktop utilities;
- future integration with CandyWallet native modules if needed.

Текущий Java SDK специально сделан без внешних зависимостей, на стандартном `java.net.http.HttpClient`.

## Требования

- Java 21 или совместимый JDK.
- Для Android-приложений: Android Studio / Android SDK.

## Компиляция

PowerShell:

```powershell
cd packages\java
javac -d build\classes (Get-ChildItem -Recurse -Filter *.java src\main\java | ForEach-Object { $_.FullName })
```

Bash:

```bash
cd packages/java
javac -d build/classes $(find src/main/java -name "*.java")
```

## Базовое использование

```java
import ru.mintcandy.decimal.DecimalClient;

public class Main {
    public static void main(String[] args) throws Exception {
        DecimalClient client = new DecimalClient();

        System.out.println(client.health());
        System.out.println(client.blockNumber());
        System.out.println(client.gasPrice());
        System.out.println(client.balanceWei("0x..."));
    }
}
```

## Network config

```java
NetworkConfig config = NetworkConfig.mainnet();
DecimalClient client = new DecimalClient(config);
```

Default Web3 endpoint:

- `https://node.decimalchain.com/web3/`

REST/API/WS endpoint-ы для production передаются явно через config.

## Read-only методы

```java
client.health();
client.latestBlock();
client.blockNumber();
client.gasPrice();
client.balanceWei("0xAddress");
client.transactionCount("0xAddress");
```

## Transaction draft и preflight

```java
import java.math.BigInteger;
import ru.mintcandy.decimal.TransactionDraft;
import ru.mintcandy.decimal.TransactionResult;

TransactionDraft draft = client.buildNativeTransfer(
    "0xFrom",
    "0xTo",
    new BigInteger("1000000000000000000")
);

TransactionResult dryRun = client.dryRun(draft);

if (!dryRun.success()) {
    System.out.println(dryRun.error());
}
```

## Broadcast raw transaction

Подпись пока предполагается внешней или локальным Android crypto layer:

```java
String txHash = client.sendRawTransaction("0xSignedRawTransaction");
```

## TransactionPolicy

```java
TransactionPolicy policy = TransactionPolicy.fast();
policy.validate();
```

Цель: держать build + estimate + broadcast + первый status/receipt poll в бюджете до 5 секунд, если позволяют сеть и ноды.

## Текущий статус

Готово:

- `NetworkConfig`.
- `TransactionPolicy`.
- `DecimalClient`.
- JSON-RPC calls.
- REST health/latest block.
- `TransactionDraft`.
- `FeePreflight`.
- `TransactionResult`.
- raw transaction broadcast.

Осталось:

- Android secure signing/key storage;
- ERC20 ABI encoding;
- Token Center workflows;
- NFT workflows;
- Gradle/Maven packaging;
- tests на JVM;
- Kotlin-friendly API.
