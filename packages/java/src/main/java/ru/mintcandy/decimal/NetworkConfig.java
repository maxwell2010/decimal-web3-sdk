package ru.mintcandy.decimal;

import java.util.List;

public record NetworkConfig(
    int chainId,
    List<String> web3Urls,
    List<String> restUrls,
    List<String> wsUrls,
    String apiRootUrl,
    String apiBaseUrl
) {
    public static NetworkConfig mainnet() {
        return new NetworkConfig(
            75,
            List.of("https://node1.mintcandy.ru/web3", "https://node2.mintcandy.ru/web3"),
            List.of("https://node1.mintcandy.ru/api/", "https://node2.mintcandy.ru/api/"),
            List.of("wss://node1.mintcandy.ru/ws/", "wss://node2.mintcandy.ru/ws/"),
            "https://node1.mintcandy.ru/txs",
            "https://node1.mintcandy.ru/txs/api/v1"
        );
    }
}
