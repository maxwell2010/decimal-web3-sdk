import {
  createPublicClient,
  encodeFunctionData,
  formatEther,
  getAddress,
  http,
  parseEther,
  type Address,
  type Hex,
  type PublicClient,
} from "viem";
import { privateKeyToAccount } from "viem/accounts";

export type NetworkConfig = {
  chainId: number;
  web3Urls: string[];
  restUrls: string[];
  wsUrls: string[];
  apiRootUrl: string;
  apiBaseUrl: string;
  contracts: SystemContracts;
};

export type SystemContracts = {
  contractCenter: Address;
  delegation: Address;
  delegationNft: Address;
  masterValidator: Address;
  nftCenter: Address;
  tokenCenter: Address;
  wdel: Address;
  multicall: Address;
  delToken: Address;
};

export type TransactionPolicy = {
  targetTotalSeconds: number;
  buildTimeoutSeconds: number;
  estimateTimeoutSeconds: number;
  broadcastTimeoutSeconds: number;
  receiptPollSeconds: number;
  maxRpcAttempts: number;
};

export type TransactionDraft = {
  from: Address;
  to: Address;
  value: bigint;
  data: Hex;
  nonce: number;
  gasPrice: bigint;
  gas?: bigint;
  feeWei?: bigint;
};

export type FeePreflight = {
  ok: boolean;
  from: Address;
  nativeBalanceWei: bigint;
  valueWei: bigint;
  feeWei: bigint;
  requiredWei: bigint;
  missingWei: bigint;
};

export type TransactionResult = {
  success: boolean;
  txHash?: Hex;
  rawTx?: Hex;
  gas?: bigint;
  feeWei?: bigint;
  feeDel?: string;
  preflight?: FeePreflight;
  error?: string;
};

export type Erc20Info = {
  address: Address;
  name?: string;
  symbol?: string;
  decimals: number;
};

export type AgentResult = {
  name: string;
  success: boolean;
  payload?: Record<string, unknown>;
  error?: string;
};

export interface DecimalAgent {
  name: string;
  run(context: AgentContext): Promise<AgentResult>;
}

export type AgentContext = {
  client?: DecimalWeb3Client;
  data: Record<string, unknown>;
  policy: TransactionPolicy;
};

const decimalChain = {
  id: 75,
  name: "Decimal",
  nativeCurrency: { decimals: 18, name: "Decimal", symbol: "DEL" },
  rpcUrls: {
    default: { http: ["https://node1.mintcandy.ru/web3"] },
  },
} as const;

const erc20Abi = [
  {
    type: "function",
    name: "name",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "string" }],
  },
  {
    type: "function",
    name: "symbol",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "string" }],
  },
  {
    type: "function",
    name: "decimals",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "uint8" }],
  },
  {
    type: "function",
    name: "balanceOf",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ type: "uint256" }],
  },
  {
    type: "function",
    name: "allowance",
    stateMutability: "view",
    inputs: [
      { name: "owner", type: "address" },
      { name: "spender", type: "address" },
    ],
    outputs: [{ type: "uint256" }],
  },
  {
    type: "function",
    name: "transfer",
    stateMutability: "nonpayable",
    inputs: [
      { name: "to", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [{ type: "bool" }],
  },
  {
    type: "function",
    name: "approve",
    stateMutability: "nonpayable",
    inputs: [
      { name: "spender", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [{ type: "bool" }],
  },
] as const;

export const mainnetConfig = (): NetworkConfig => ({
  chainId: 75,
  web3Urls: ["https://node1.mintcandy.ru/web3", "https://node2.mintcandy.ru/web3"],
  restUrls: ["https://node1.mintcandy.ru/api/", "https://node2.mintcandy.ru/api/"],
  wsUrls: ["wss://node1.mintcandy.ru/ws/", "wss://node2.mintcandy.ru/ws/"],
  apiRootUrl: "https://node1.mintcandy.ru/txs",
  apiBaseUrl: "https://node1.mintcandy.ru/txs/api/v1",
  contracts: {
    contractCenter: "0xc108715a06f76caa96fa2c943ebf05159c29a87d",
    delegation: "0xa16c34ed1c0601c0e749e17ebef19752a15faa01",
    delegationNft: "0x5a6533e337f4b7f815aefb0609200acfbe1ba231",
    masterValidator: "0x8ff2f220fb80b3f26cd96652aecbf3129983c115",
    nftCenter: "0x9113ba675aa8f2ef0c068cee2cdabab95b6437fb",
    tokenCenter: "0x9113ba675aa8f2ef0c068cee2cdabab95b6437fb",
    wdel: "0x1c5d8992da64c8d56ea413dd6f723061c29a7c0b",
    multicall: "0x7b23eb47587ca6482fc16cb3d9d426ec64d4b5fc",
    delToken: "0x16049a46126d69211de7c042465122badefa360c",
  },
});

export const fastTransactionPolicy = (): TransactionPolicy => ({
  targetTotalSeconds: 5,
  buildTimeoutSeconds: 1,
  estimateTimeoutSeconds: 1.5,
  broadcastTimeoutSeconds: 1.5,
  receiptPollSeconds: 1,
  maxRpcAttempts: 2,
});

export class DecimalWeb3Client {
  readonly publicClient: PublicClient;

  constructor(readonly config: NetworkConfig = mainnetConfig()) {
    this.publicClient = createPublicClient({
      chain: { ...decimalChain, id: config.chainId, rpcUrls: { default: { http: config.web3Urls } } },
      transport: http(config.web3Urls[0]),
    });
  }

  async blockNumber(): Promise<bigint> {
    return this.publicClient.getBlockNumber();
  }

  async balanceWei(address: Address): Promise<bigint> {
    return this.publicClient.getBalance({ address: getAddress(address) });
  }

  async balanceDel(address: Address): Promise<string> {
    return formatEther(await this.balanceWei(address));
  }

  async gasPrice(): Promise<bigint> {
    return this.publicClient.getGasPrice();
  }

  async transactionCount(address: Address): Promise<number> {
    return this.publicClient.getTransactionCount({ address: getAddress(address) });
  }

  async restGet<T = unknown>(path: string, params?: Record<string, string | number | boolean>): Promise<T> {
    return fetchJson<T>(joinUrl(this.config.apiBaseUrl, path), params);
  }

  async restRootGet<T = unknown>(path: string, params?: Record<string, string | number | boolean>): Promise<T> {
    return fetchJson<T>(joinUrl(this.config.apiRootUrl, path), params);
  }

  async health(): Promise<unknown> {
    return this.restRootGet("/health");
  }

  async latestBlock(): Promise<unknown> {
    return this.restGet("/blocks/latest");
  }

  async erc20Info(token: Address): Promise<Erc20Info> {
    const address = getAddress(token);
    const [name, symbol, decimals] = await Promise.all([
      this.tryReadContract<string>(address, "name"),
      this.tryReadContract<string>(address, "symbol"),
      this.publicClient.readContract({ address, abi: erc20Abi, functionName: "decimals" }),
    ]);
    return { address, name, symbol, decimals: Number(decimals) };
  }

  async erc20Balance(token: Address, owner: Address): Promise<bigint> {
    return this.publicClient.readContract({
      address: getAddress(token),
      abi: erc20Abi,
      functionName: "balanceOf",
      args: [getAddress(owner)],
    });
  }

  async erc20Allowance(token: Address, owner: Address, spender: Address): Promise<bigint> {
    return this.publicClient.readContract({
      address: getAddress(token),
      abi: erc20Abi,
      functionName: "allowance",
      args: [getAddress(owner), getAddress(spender)],
    });
  }

  buildErc20TransferData(to: Address, amountRaw: bigint): Hex {
    return encodeFunctionData({ abi: erc20Abi, functionName: "transfer", args: [getAddress(to), amountRaw] });
  }

  buildErc20ApproveData(spender: Address, amountRaw: bigint): Hex {
    return encodeFunctionData({ abi: erc20Abi, functionName: "approve", args: [getAddress(spender), amountRaw] });
  }

  async buildNativeTransfer(input: {
    privateKey: Hex;
    to: Address;
    amountDel: string;
    data?: Hex;
  }): Promise<TransactionDraft> {
    const account = privateKeyToAccount(input.privateKey);
    return this.buildContractCall({
      privateKey: input.privateKey,
      to: input.to,
      valueWei: parseEther(input.amountDel),
      data: input.data ?? "0x",
      from: account.address,
    });
  }

  async buildErc20Transfer(input: {
    privateKey: Hex;
    token: Address;
    to: Address;
    amountRaw: bigint;
  }): Promise<TransactionDraft> {
    const account = privateKeyToAccount(input.privateKey);
    const balance = await this.erc20Balance(input.token, account.address);
    if (balance < input.amountRaw) {
      throw new Error(
        `Insufficient ERC20 token balance: balance_raw=${balance}, required_raw=${input.amountRaw}, missing_raw=${input.amountRaw - balance}`,
      );
    }
    return this.buildContractCall({
      privateKey: input.privateKey,
      to: input.token,
      valueWei: 0n,
      data: this.buildErc20TransferData(input.to, input.amountRaw),
      from: account.address,
    });
  }

  async buildContractCall(input: {
    privateKey: Hex;
    to: Address;
    valueWei?: bigint;
    data: Hex;
    from?: Address;
  }): Promise<TransactionDraft> {
    const account = input.from ?? privateKeyToAccount(input.privateKey).address;
    return {
      from: getAddress(account),
      to: getAddress(input.to),
      value: input.valueWei ?? 0n,
      data: input.data,
      nonce: await this.transactionCount(account),
      gasPrice: await this.gasPrice(),
    };
  }

  async estimate(draft: TransactionDraft): Promise<TransactionDraft> {
    const gas = await this.publicClient.estimateGas({
      account: draft.from,
      to: draft.to,
      value: draft.value,
      data: draft.data,
    });
    return { ...draft, gas, feeWei: gas * draft.gasPrice };
  }

  async preflightFee(draft: TransactionDraft): Promise<FeePreflight> {
    if (draft.feeWei === undefined) {
      throw new Error("Estimate transaction before fee preflight");
    }
    const nativeBalanceWei = await this.balanceWei(draft.from);
    const requiredWei = draft.value + draft.feeWei;
    const missingWei = requiredWei > nativeBalanceWei ? requiredWei - nativeBalanceWei : 0n;
    return {
      ok: missingWei === 0n,
      from: draft.from,
      nativeBalanceWei,
      valueWei: draft.value,
      feeWei: draft.feeWei,
      requiredWei,
      missingWei,
    };
  }

  async signDraft(draft: TransactionDraft, privateKey: Hex): Promise<Hex> {
    const account = privateKeyToAccount(privateKey);
    return account.signTransaction({
      chainId: this.config.chainId,
      to: draft.to,
      value: draft.value,
      data: draft.data,
      nonce: draft.nonce,
      gas: draft.gas,
      gasPrice: draft.gasPrice,
    });
  }

  async sendDraft(draft: TransactionDraft, privateKey: Hex, broadcast = false): Promise<TransactionResult> {
    try {
      const estimated = draft.gas ? draft : await this.estimate(draft);
      const preflight = await this.preflightFee(estimated);
      if (!preflight.ok) {
        return {
          success: false,
          gas: estimated.gas,
          feeWei: estimated.feeWei,
          feeDel: estimated.feeWei === undefined ? undefined : formatEther(estimated.feeWei),
          preflight,
          error: `Insufficient DEL for transaction value and fee: missing_wei=${preflight.missingWei}`,
        };
      }
      const rawTx = await this.signDraft(estimated, privateKey);
      if (!broadcast) {
        return {
          success: true,
          rawTx,
          gas: estimated.gas,
          feeWei: estimated.feeWei,
          feeDel: estimated.feeWei === undefined ? undefined : formatEther(estimated.feeWei),
          preflight,
        };
      }
      const txHash = await this.publicClient.sendRawTransaction({ serializedTransaction: rawTx });
      return {
        success: true,
        txHash,
        rawTx,
        gas: estimated.gas,
        feeWei: estimated.feeWei,
        feeDel: estimated.feeWei === undefined ? undefined : formatEther(estimated.feeWei),
        preflight,
      };
    } catch (error) {
      return { success: false, error: error instanceof Error ? error.message : String(error) };
    }
  }

  private async tryReadContract<T>(address: Address, functionName: "name" | "symbol"): Promise<T | undefined> {
    try {
      return (await this.publicClient.readContract({
        address,
        abi: erc20Abi,
        functionName,
      })) as T;
    } catch {
      return undefined;
    }
  }
}

export class AgentOrchestrator {
  constructor(private readonly agents: DecimalAgent[] = []) {}

  add(agent: DecimalAgent): void {
    this.agents.push(agent);
  }

  async runParallel(context: AgentContext, timeoutMs = 5000): Promise<AgentResult[]> {
    return Promise.all(this.agents.map((agent) => this.runOne(agent, context, timeoutMs)));
  }

  private async runOne(
    agent: DecimalAgent,
    context: AgentContext,
    timeoutMs: number,
  ): Promise<AgentResult> {
    let timer: ReturnType<typeof setTimeout> | undefined;
    try {
      const timeout = new Promise<AgentResult>((resolve) => {
        timer = setTimeout(
          () =>
            resolve({
              name: agent.name,
              success: false,
              error: `Agent timed out after ${timeoutMs}ms`,
            }),
          timeoutMs,
        );
      });
      return await Promise.race([agent.run(context), timeout]);
    } catch (error) {
      return { name: agent.name, success: false, error: String(error) };
    } finally {
      if (timer) clearTimeout(timer);
    }
  }
}

async function fetchJson<T>(url: string, params?: Record<string, string | number | boolean>): Promise<T> {
  const target = new URL(url);
  for (const [key, value] of Object.entries(params ?? {})) {
    target.searchParams.set(key, String(value));
  }
  const response = await fetch(target);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status} for ${target}`);
  }
  return response.json() as Promise<T>;
}

function joinUrl(base: string, path: string): string {
  return `${base.replace(/\/+$/, "")}/${path.replace(/^\/+/, "")}`;
}
