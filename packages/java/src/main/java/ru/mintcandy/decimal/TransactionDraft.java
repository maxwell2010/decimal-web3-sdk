package ru.mintcandy.decimal;

import java.math.BigInteger;

public record TransactionDraft(
    String from,
    String to,
    BigInteger valueWei,
    String data,
    BigInteger nonce,
    BigInteger gasPriceWei,
    BigInteger gas,
    BigInteger feeWei
) {
    public TransactionDraft withEstimate(BigInteger estimatedGas) {
        return new TransactionDraft(
            from,
            to,
            valueWei,
            data,
            nonce,
            gasPriceWei,
            estimatedGas,
            estimatedGas.multiply(gasPriceWei)
        );
    }
}
