package com.astro.dto;

import java.util.Map;

public record AnalysisResponse(
        Map<String, Object> companyInfo,
        ComprehensiveAnalysisResponse analysis
) {}
