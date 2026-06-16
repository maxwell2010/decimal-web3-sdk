package ru.mintcandy.decimal;

import java.math.BigInteger;

public record FeePreflight(
    boolean ok,
    String from,
    BigInteger nativeBalanceWei,
    BigInteger valueWei,
    BigInteger feeWei,
    BigInteger requiredWei,
    BigInteger missingWei
) {
    public static FeePreflight of(String from, BigInteger balanceWei, BigInteger valueWei, BigInteger feeWei) {
        BigInteger required = valueWei.add(feeWei);
        BigInteger missing = required.compareTo(balanceWei) > 0 ? required.subtract(balanceWei) : BigInteger.ZERO;
        return new FeePreflight(
            missing.signum() == 0,
            from,
            balanceWei,
            valueWei,
            feeWei,
            required,
            missing
        );
    }
}
