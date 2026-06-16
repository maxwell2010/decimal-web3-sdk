import { createPublicClient, createWalletClient, encodeFunctionData, formatEther, getAddress, http, parseAbi, parseEther } from "viem";
import { mnemonicToAccount } from "viem/accounts";
import { decimalConfig } from "./config";
import type { Asset } from "@/types";

const chain = {
  id: decimalConfig.chainId,
  name: "Decimal",
  nativeCurrency: { name: "Decimal", symbol: "DEL", decimals: 18 },
  rpcUrls: { default: { http: decimalConfig.web3Urls } },
} as const;

const erc20Abi = parseAbi([
  "function balanceOf(address owner) view returns (uint256)",
  "function decimals() view returns (uint8)",
  "function symbol() view returns (string)",
  "function name() view returns (string)",
  "function transfer(address to, uint256 amount) returns (bool)",
  "function buy(uint256 amountOutMin, address recipient) payable",
  "function sell(uint256 amountIn, uint256 amountOutMin, address recipient)",
  "function calculateBuyOutput(uint256 amount) view returns (uint256)",
  "function calculateSellOutput(uint256 amount) view returns (uint256)",
]);

const delegationAddress = "0xa16c34ed1c0601c0e749e17ebef19752a15faa01";
const delTokenAddress = "0x16049a46126d69211de7c042465122badefa360c";

const delegationAbi = parseAbi([
  "function delegateDEL(address validator) payable",
  "function delegate(address validator, address token, uint256 amount)",
  "function withdraw(address validator, address token, uint256 amount)",
]);

type TxResult = { hash: string; feeDel: string; confirmed: boolean };

export class DecimalMobileClient {
  private readonly publicClient = createPublicClient({
    chain,
    transport: http(decimalConfig.web3Urls[0]),
  });

  async getDelBalance(address: string): Promise<string> {
    const balance = await this.publicClient.getBalance({ address: getAddress(address) });
    return formatEther(balance);
  }

  async getKnownAssets(address: string): Promise<Asset[]> {
    const delBalance = await this.getDelBalance(address).catch(() => "0");
    const assets: Asset[] = [
      {
        id: "del",
        type: "coin",
        symbol: "DEL",
        name: "Decimal",
        balance: trimAmount(delBalance),
        decimals: 18,
      },
    ];

    const tokenAssets = await Promise.allSettled(
      decimalConfig.trackedErc20Tokens.map((token) => this.getErc20Asset(token, address)),
    );
    for (const result of tokenAssets) {
      if (result.status === "fulfilled" && result.value.balance !== "0") {
        assets.push(result.value);
      }
    }
    return assets;
  }

  async getErc20Asset(token: string, owner: string): Promise<Asset> {
    const address = getAddress(token);
    const [symbol, name, decimals, balance] = await Promise.all([
      this.publicClient.readContract({ address, abi: erc20Abi, functionName: "symbol" }),
      this.publicClient.readContract({ address, abi: erc20Abi, functionName: "name" }),
      this.publicClient.readContract({ address, abi: erc20Abi, functionName: "decimals" }),
      this.publicClient.readContract({ address, abi: erc20Abi, functionName: "balanceOf", args: [getAddress(owner)] }),
    ]);
    return {
      id: address,
      type: "erc20",
      address,
      symbol: String(symbol),
      name: String(name),
      decimals: Number(decimals),
      balance: trimAmount(formatUnits(balance, Number(decimals))),
    };
  }

  async sendDel(params: { mnemonic: string; to: string; amount: string }): Promise<TxResult> {
    const account = mnemonicToAccount(params.mnemonic);
    const to = getAddress(params.to);
    const value = parseEther(params.amount);
    const gas = await this.publicClient.estimateGas({ account, to, value });
    const gasPrice = await this.publicClient.getGasPrice();
    const fee = gas * gasPrice;
    const balance = await this.publicClient.getBalance({ address: account.address });
    if (balance < value + fee) {
      throw new Error(`Недостаточно DEL: нужно ${formatEther(value + fee)} DEL с учетом комиссии.`);
    }
    const walletClient = createWalletClient({ account, chain, transport: http(decimalConfig.web3Urls[0]) });
    const hash = await walletClient.sendTransaction({ to, value, gas, gasPrice });
    const confirmed = await this.waitForFastConfirmation(hash);
    return { hash, feeDel: trimAmount(formatEther(fee)), confirmed };
  }

  async sendErc20(params: { mnemonic: string; token: string; to: string; amount: string; decimals: number }): Promise<TxResult> {
    const account = mnemonicToAccount(params.mnemonic);
    const token = getAddress(params.token);
    const to = getAddress(params.to);
    const value = parseUnits(params.amount, params.decimals);
    const tokenBalance = await this.publicClient.readContract({ address: token, abi: erc20Abi, functionName: "balanceOf", args: [account.address] });
    if (tokenBalance < value) {
      throw new Error("Недостаточно токенов для отправки.");
    }
    const data = encodeFunctionData({ abi: erc20Abi, functionName: "transfer", args: [to, value] });
    return this.estimateAndSend({ mnemonic: params.mnemonic, to: token, data });
  }

  async delegateDel(params: { mnemonic: string; validator: string; amount: string }): Promise<TxResult> {
    const validator = getAddress(params.validator);
    const value = parseEther(params.amount);
    const data = encodeFunctionData({ abi: delegationAbi, functionName: "delegateDEL", args: [validator] });
    return this.estimateAndSend({ mnemonic: params.mnemonic, to: delegationAddress, data, value });
  }

  async withdrawDel(params: { mnemonic: string; validator: string; amount: string }): Promise<TxResult> {
    const validator = getAddress(params.validator);
    const value = parseEther(params.amount);
    const data = encodeFunctionData({ abi: delegationAbi, functionName: "withdraw", args: [validator, delTokenAddress, value] });
    return this.estimateAndSend({ mnemonic: params.mnemonic, to: delegationAddress, data });
  }

  async delegateErc20(params: { mnemonic: string; token: string; validator: string; amount: string; decimals: number }): Promise<TxResult> {
    const account = mnemonicToAccount(params.mnemonic);
    const token = getAddress(params.token);
    const validator = getAddress(params.validator);
    const value = parseUnits(params.amount, params.decimals);
    const tokenBalance = await this.publicClient.readContract({ address: token, abi: erc20Abi, functionName: "balanceOf", args: [account.address] });
    if (tokenBalance < value) throw new Error("Недостаточно токенов для делегирования.");
    const data = encodeFunctionData({ abi: delegationAbi, functionName: "delegate", args: [validator, token, value] });
    return this.estimateAndSend({ mnemonic: params.mnemonic, to: delegationAddress, data });
  }

  async withdrawErc20(params: { mnemonic: string; token: string; validator: string; amount: string; decimals: number }): Promise<TxResult> {
    const token = getAddress(params.token);
    const validator = getAddress(params.validator);
    const value = parseUnits(params.amount, params.decimals);
    const data = encodeFunctionData({ abi: delegationAbi, functionName: "withdraw", args: [validator, token, value] });
    return this.estimateAndSend({ mnemonic: params.mnemonic, to: delegationAddress, data });
  }

  async buyTokenWithDel(params: { mnemonic: string; token: string; amountDel: string }): Promise<TxResult> {
    const account = mnemonicToAccount(params.mnemonic);
    const token = getAddress(params.token);
    const value = parseEther(params.amountDel);
    const data = encodeFunctionData({ abi: erc20Abi, functionName: "buy", args: [0n, account.address] });
    return this.estimateAndSend({ mnemonic: params.mnemonic, to: token, data, value });
  }

  async sellTokenForDel(params: { mnemonic: string; token: string; amount: string; decimals: number }): Promise<TxResult> {
    const account = mnemonicToAccount(params.mnemonic);
    const token = getAddress(params.token);
    const value = parseUnits(params.amount, params.decimals);
    const tokenBalance = await this.publicClient.readContract({ address: token, abi: erc20Abi, functionName: "balanceOf", args: [account.address] });
    if (tokenBalance < value) throw new Error("Недостаточно токенов для обмена.");
    const data = encodeFunctionData({ abi: erc20Abi, functionName: "sell", args: [value, 0n, account.address] });
    return this.estimateAndSend({ mnemonic: params.mnemonic, to: token, data });
  }

  async calculateBuyOutput(tokenAddress: string, amountDel: string, decimals: number): Promise<string> {
    const token = getAddress(tokenAddress);
    const result = await this.publicClient.readContract({ address: token, abi: erc20Abi, functionName: "calculateBuyOutput", args: [parseEther(amountDel || "0")] });
    return trimAmount(formatUnits(result, decimals));
  }

  private async estimateAndSend(params: { mnemonic: string; to: string; data?: `0x${string}`; value?: bigint }): Promise<TxResult> {
    const account = mnemonicToAccount(params.mnemonic);
    const to = getAddress(params.to);
    const value = params.value || 0n;
    const gas = await this.publicClient.estimateGas({ account, to, data: params.data, value });
    const gasPrice = await this.publicClient.getGasPrice();
    const fee = gas * gasPrice;
    const balance = await this.publicClient.getBalance({ address: account.address });
    if (balance < value + fee) {
      throw new Error(`Недостаточно DEL: нужно ${trimAmount(formatEther(value + fee))} DEL с учетом комиссии.`);
    }
    const walletClient = createWalletClient({ account, chain, transport: http(decimalConfig.web3Urls[0]) });
    const hash = await walletClient.sendTransaction({ to, data: params.data, value, gas, gasPrice });
    const confirmed = await this.waitForFastConfirmation(hash);
    return { hash, feeDel: trimAmount(formatEther(fee)), confirmed };
  }

  private async waitForFastConfirmation(hash: `0x${string}`): Promise<boolean> {
    try {
      const receipt = await Promise.race([
        this.publicClient.waitForTransactionReceipt({ hash }),
        new Promise<null>((resolve) => setTimeout(() => resolve(null), 5000)),
      ]);
      return receipt?.status === "success";
    } catch {
      return false;
    }
  }
}

export function trimAmount(value: string): string {
  const [whole, fraction = ""] = value.split(".");
  const cut = fraction.slice(0, 4).replace(/0+$/, "");
  return cut ? `${whole}.${cut}` : whole;
}

function formatUnits(value: bigint, decimals: number): string {
  const base = 10n ** BigInt(decimals);
  const whole = value / base;
  const fraction = String(value % base).padStart(decimals, "0").replace(/0+$/, "");
  return fraction ? `${whole}.${fraction}` : String(whole);
}

function parseUnits(value: string, decimals: number): bigint {
  const [whole, fraction = ""] = value.split(".");
  const normalized = `${whole || "0"}${fraction.padEnd(decimals, "0").slice(0, decimals)}`;
  return BigInt(normalized);
}
