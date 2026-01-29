package com.astro.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;

import java.util.List;

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public record CourtAnalysisResponse(
    @JsonProperty("analysis")
    String analysis,
    @JsonProperty("risk_factors")
    List<String> riskFactors,
    @JsonProperty("severity")
    String severity
) {}
