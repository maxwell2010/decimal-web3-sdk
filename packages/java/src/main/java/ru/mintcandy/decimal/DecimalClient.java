package ru.mintcandy.decimal;

import java.io.IOException;
import java.math.BigInteger;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class DecimalClient {
    private static final Pattern JSON_RESULT_PATTERN = Pattern.compile("\"result\"\\s*:\\s*\"?([^\",}]+)\"?");
    private static final Pattern JSON_ERROR_PATTERN = Pattern.compile("\"error\"\\s*:");

    private final NetworkConfig config;
    private final HttpClient http;
    private final AtomicLong rpcId = new AtomicLong(1);

    public DecimalClient() {
        this(NetworkConfig.mainnet());
    }

    public DecimalClient(NetworkConfig config) {
        this.config = config;
        this.http = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(5))
            .build();
    }

    public NetworkConfig config() {
        return config;
    }

    public String health() throws IOException, InterruptedException {
        return get(config.apiRootUrl(), "/health", Map.of());
    }

    public String latestBlock() throws IOException, InterruptedException {
        return get(config.apiBaseUrl(), "/blocks/latest", Map.of());
    }

    public BigInteger blockNumber() throws IOException, InterruptedException {
        return rpcQuantity("eth_blockNumber");
    }

    public BigInteger gasPrice() throws IOException, InterruptedException {
        return rpcQuantity("eth_gasPrice");
    }

    public BigInteger balanceWei(String address) throws IOException, InterruptedException {
        return rpcQuantity("eth_getBalance", quote(address), quote("latest"));
    }

    public BigInteger transactionCount(String address) throws IOException, InterruptedException {
        return rpcQuantity("eth_getTransactionCount", quote(address), quote("pending"));
    }

    public BigInteger estimateGas(TransactionDraft draft) throws IOException, InterruptedException {
        String tx = "{"
            + "\"from\":" + quote(draft.from()) + ","
            + "\"to\":" + quote(draft.to()) + ","
            + "\"value\":" + quote(toQuantity(draft.valueWei())) + ","
            + "\"data\":" + quote(draft.data() == null ? "0x" : draft.data())
            + "}";
        return rpcQuantity("eth_estimateGas", tx);
    }

    public FeePreflight preflightFee(TransactionDraft draft) throws IOException, InterruptedException {
        if (draft.feeWei() == null) {
            throw new IllegalArgumentException("Estimate transaction before fee preflight");
        }
        return FeePreflight.of(draft.from(), balanceWei(draft.from()), draft.valueWei(), draft.feeWei());
    }

    public String sendRawTransaction(String rawTransactionHex) throws IOException, InterruptedException {
        return rpcString("eth_sendRawTransaction", quote(rawTransactionHex));
    }

    public TransactionDraft buildNativeTransfer(String from, String to, BigInteger valueWei) throws IOException, InterruptedException {
        return new TransactionDraft(
            from,
            to,
            valueWei,
            "0x",
            transactionCount(from),
            gasPrice(),
            null,
            null
        );
    }

    public TransactionResult dryRun(TransactionDraft draft) {
        try {
            TransactionDraft estimated = draft.gas() == null ? draft.withEstimate(estimateGas(draft)) : draft;
            FeePreflight preflight = preflightFee(estimated);
            if (!preflight.ok()) {
                return new TransactionResult(
                    false,
                    null,
                    estimated.gas(),
                    estimated.feeWei(),
                    preflight,
                    "Insufficient DEL for transaction value and fee: missing_wei=" + preflight.missingWei()
                );
            }
            return new TransactionResult(true, null, estimated.gas(), estimated.feeWei(), preflight, null);
        } catch (Exception exc) {
            return TransactionResult.failed(exc.getMessage());
        }
    }

    private BigInteger rpcQuantity(String method, String... params) throws IOException, InterruptedException {
        return parseQuantity(rpcString(method, params));
    }

    private String rpcString(String method, String... params) throws IOException, InterruptedException {
        String body = "{\"jsonrpc\":\"2.0\",\"id\":" + rpcId.getAndIncrement()
            + ",\"method\":\"" + method + "\",\"params\":[" + String.join(",", params) + "]}";
        HttpRequest request = HttpRequest.newBuilder(URI.create(config.web3Urls().get(0)))
            .timeout(Duration.ofSeconds(20))
            .header("content-type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(body))
            .build();
        String response = send(request);
        if (JSON_ERROR_PATTERN.matcher(response).find()) {
            throw new IOException("RPC error: " + response);
        }
        Matcher matcher = JSON_RESULT_PATTERN.matcher(response);
        if (!matcher.find()) {
            throw new IOException("RPC result not found: " + response);
        }
        return matcher.group(1);
    }

    private String get(String baseUrl, String path, Map<String, ?> params) throws IOException, InterruptedException {
        URI uri = URI.create(joinUrl(baseUrl, path) + query(params));
        HttpRequest request = HttpRequest.newBuilder(uri)
            .timeout(Duration.ofSeconds(20))
            .GET()
            .build();
        return send(request);
    }

    private String send(HttpRequest request) throws IOException, InterruptedException {
        HttpResponse<String> response = http.send(request, HttpResponse.BodyHandlers.ofString());
        if (response.statusCode() < 200 || response.statusCode() >= 300) {
            throw new IOException("HTTP " + response.statusCode() + ": " + response.body());
        }
        return response.body();
    }

    private static String joinUrl(String base, String path) {
        return base.replaceAll("/+$", "") + "/" + path.replaceAll("^/+", "");
    }

    private static String query(Map<String, ?> params) {
        if (params.isEmpty()) {
            return "";
        }
        StringBuilder builder = new StringBuilder("?");
        boolean first = true;
        for (Map.Entry<String, ?> entry : params.entrySet()) {
            if (!first) {
                builder.append('&');
            }
            first = false;
            builder.append(URLEncoder.encode(entry.getKey(), StandardCharsets.UTF_8));
            builder.append('=');
            builder.append(URLEncoder.encode(String.valueOf(entry.getValue()), StandardCharsets.UTF_8));
        }
        return builder.toString();
    }

    private static BigInteger parseQuantity(String value) {
        if (value.startsWith("0x")) {
            return new BigInteger(value.substring(2), 16);
        }
        return new BigInteger(value);
    }

    private static String toQuantity(BigInteger value) {
        if (value == null || value.signum() == 0) {
            return "0x0";
        }
        return "0x" + value.toString(16);
    }

    private static String quote(String value) {
        return "\"" + value.replace("\\", "\\\\").replace("\"", "\\\"") + "\"";
    }
}
