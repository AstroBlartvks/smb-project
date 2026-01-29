package com.astro.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;

import java.util.Map;

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public record MLPredictionResponse(
        @JsonProperty("bankruptcy_probability")
        double bankruptcyProbability,
        @JsonProperty("risk_level")
        String riskLevel,
        @JsonProperty("model_predictions")
        Map<String, Double> modelPredictions,
        @JsonProperty("timestamp")
        String timestamp
) {}
