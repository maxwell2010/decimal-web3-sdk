# Decimal Java SDK

Target package: `ru.mintcandy.decimal`.

Use cases:

- Android apps.
- JVM backend services.
- Desktop tools.

The Java SDK should mirror Python and Web JS DTO names where possible. For Android, keep crypto/signing local and push heavy read-only history queries through the REST API.

Implemented now without external dependencies:

- `NetworkConfig` with Web3/REST/WS/API endpoints.
- `TransactionPolicy` for 5-second transaction budgeting.
- `DecimalClient` using Java `HttpClient`.
- Read-only calls: `health`, `latestBlock`, `blockNumber`, `gasPrice`, `balanceWei`, `transactionCount`.
- Transaction draft DTOs and DEL fee preflight.
- Raw transaction broadcast entrypoint for externally/local signed transactions.

Compile check:

```bash
javac -d build/classes $(find src/main/java -name "*.java")
```

PowerShell:

```powershell
javac -d build\classes (Get-ChildItem -Recurse -Filter *.java src\main\java | ForEach-Object { $_.FullName })
```
