package ru.mintcandy.decimal;

import java.math.BigInteger;

public record TransactionResult(
    boolean success,
    String txHash,
    BigInteger gas,
    BigInteger feeWei,
    FeePreflight preflight,
    String error
) {
    public static TransactionResult failed(String error) {
        return new TransactionResult(false, null, null, null, null, error);
    }
}
