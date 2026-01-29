package com.astro.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public record ComprehensiveAnalysisResponse(
        @JsonProperty("prediction")
        MLPredictionResponse prediction,
        @JsonProperty("explanation")
        MLExplanationResponse explanation,
        @JsonProperty("court_analysis")
        CourtAnalysisResponse courtAnalysis,
        @JsonProperty("ai_summary")
        String aiSummary,
        @JsonProperty("timestamp")
        String timestamp
) {}