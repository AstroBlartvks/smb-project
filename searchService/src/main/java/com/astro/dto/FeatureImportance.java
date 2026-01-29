package com.astro.dto;

public record FeatureImportance(
    String featureName,
    double importance,
    String direction
) {}
