package ru.mintcandy.decimal;

public record TransactionPolicy(
    double targetTotalSeconds,
    double buildTimeoutSeconds,
    double estimateTimeoutSeconds,
    double broadcastTimeoutSeconds,
    double receiptPollSeconds,
    int maxRpcAttempts
) {
    public static TransactionPolicy fast() {
        return new TransactionPolicy(5.0, 1.0, 1.5, 1.5, 1.0, 2);
    }

    public void validate() {
        double stages = buildTimeoutSeconds + estimateTimeoutSeconds + broadcastTimeoutSeconds + receiptPollSeconds;
        if (targetTotalSeconds <= 0) {
            throw new IllegalArgumentException("targetTotalSeconds must be positive");
        }
        if (stages > targetTotalSeconds) {
            throw new IllegalArgumentException("Stage timeouts exceed targetTotalSeconds");
        }
    }
}

