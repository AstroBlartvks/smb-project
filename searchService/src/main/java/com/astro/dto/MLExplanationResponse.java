package com.astro.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;

import java.util.List;
import java.util.Map;


@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public record MLExplanationResponse(
        @JsonProperty("top_features")
        List<FeatureImportance> topFeatures,
        @JsonProperty("shap_values")
        Map<String, Double> shapValues
) {}