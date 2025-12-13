package com.astro.dto;

import java.util.List;

public record SearchRequest(
        String TaxpayerIdentificationNumber,
        List<String> models
) { }
