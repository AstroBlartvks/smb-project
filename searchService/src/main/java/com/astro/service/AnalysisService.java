package com.astro.service;

import com.astro.dto.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Service
public class AnalysisService {

    private final RestTemplate restTemplate;
    private final SearchInfoService searchInfoService;
    private final ObjectMapper objectMapper;

    // В env вывести, чтобы не хардкодить
    @Value("${ml.service.url:http://localhost:8000}")
    private String mlServiceUrl;

    public AnalysisService(SearchInfoService searchInfoService) {
        this.restTemplate = new RestTemplate();
        this.searchInfoService = searchInfoService;
        this.objectMapper = new ObjectMapper();
    }

    public AnalysisResponse performAnalysis(String inn) throws Exception {
        Map<String, Object> companyData = searchInfoService.getInfoMap(
            new SearchRequest(inn, java.util.List.of())
        );

        ComprehensiveAnalysisRequest mlRequest = buildMLRequest(companyData);

        ResponseEntity<ComprehensiveAnalysisResponse> mlResponse = restTemplate.postForEntity(
            mlServiceUrl + "/api/ml/comprehensive",
            mlRequest,
            ComprehensiveAnalysisResponse.class
        );

        return new AnalysisResponse(companyData, mlResponse.getBody());
    }

    private ComprehensiveAnalysisRequest buildMLRequest(Map<String, Object> companyData) {
        double revenue = getDoubleValue(companyData, "revenue", 1000000.0);
        double netProfit = getDoubleValue(companyData, "netProfit", 50000.0);
        double totalAssets = getDoubleValue(companyData, "totalAssets", 800000.0);
        double totalLiabilities = getDoubleValue(companyData, "totalLiabilities", 400000.0);
        double currentAssets = getDoubleValue(companyData, "currentAssets", 500000.0);
        double currentLiabilities = getDoubleValue(companyData, "currentLiabilities", 300000.0);
        double equity = totalAssets - totalLiabilities;
        String region = getStringValue(companyData, "region", "Moscow");
        String industry = getStringValue(companyData, "industry", "Trade");
        int companyAge = getIntValue(companyData, "companyAge", 5);
        double authorizedCapital = getDoubleValue(companyData, "authorizedCapital", 100000.0);
        String courtData = getStringValue(companyData, "courtData", null);

        return new ComprehensiveAnalysisRequest(
            revenue, netProfit, totalAssets, totalLiabilities,
            currentAssets, currentLiabilities, equity,
            region, industry, companyAge, authorizedCapital, courtData
        );
    }

    private double getDoubleValue(Map<String, Object> map, String key, double defaultValue) {
        Object value = map.get(key);
        if (value instanceof Number) {
            return ((Number) value).doubleValue();
        }
        return defaultValue;
    }

    private String getStringValue(Map<String, Object> map, String key, String defaultValue) {
        Object value = map.get(key);
        return value != null ? value.toString() : defaultValue;
    }

    private int getIntValue(Map<String, Object> map, String key, int defaultValue) {
        Object value = map.get(key);
        if (value instanceof Number) {
            return ((Number) value).intValue();
        }
        return defaultValue;
    }
}
