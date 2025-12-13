package com.astro.exceptions;

public class TaxpayerIdNumberIsBadException extends RuntimeException {
    public TaxpayerIdNumberIsBadException(String message) {
        super(message);
    }
}
