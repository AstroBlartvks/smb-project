package com.astro.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public record ComprehensiveAnalysisRequest(
        double revenue,
        @JsonProperty("net_profit")
        double netProfit,
        @JsonProperty("total_assets")
        double totalAssets,
        @JsonProperty("total_liabilities")
        double totalLiabilities,
        @JsonProperty("current_assets")
        double currentAssets,
        @JsonProperty("current_liabilities")
        double currentLiabilities,
        double equity,
        String region,
        String industry,
        @JsonProperty("company_age")
        int companyAge,
        @JsonProperty("authorized_capital")
        double authorizedCapital,
        @JsonProperty("court_data")
        String courtData
) {}
