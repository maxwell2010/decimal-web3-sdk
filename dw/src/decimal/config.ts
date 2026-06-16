export const decimalConfig = {
  chainId: 75,
  web3Urls: ["https://node1.mintcandy.ru/web3", "https://node2.mintcandy.ru/web3"],
  centralApiUrl: "https://api.mintcandy.ru",
  apiRootUrl: "https://node2.mintcandy.ru/mc-api",
  apiBaseUrl: "https://node2.mintcandy.ru/mc-api/v1",
  apiFallbackBaseUrls: ["https://node1.mintcandy.ru/mc-api/v1"],
  marketRatesUrl: "https://api.mintcandy.ru/v1/market/del",
  bitteamApiUrl: "https://bit.team/trade/api",
  wsUrls: ["wss://node1.mintcandy.ru/ws/", "wss://node2.mintcandy.ru/ws/"],
  contracts: {
    delToken: "0x16049a46126d69211de7c042465122badefa360c",
    tokenCenter: "0x9113ba675aa8f2ef0c068cee2cdabab95b6437fb",
    delegation: "0xa16c34ed1c0601c0e749e17ebef19752a15faa01",
  },
  trackedErc20Tokens: [] as string[],
} as const;
