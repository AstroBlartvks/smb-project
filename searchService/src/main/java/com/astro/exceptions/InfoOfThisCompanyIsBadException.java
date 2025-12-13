package com.astro.exceptions;

public class InfoOfThisCompanyIsBadException extends RuntimeException {
    public InfoOfThisCompanyIsBadException(String message) {
        super(message);
    }
}
