package com.astro.controller;

import com.astro.dto.AnalysisResponse;
import com.astro.service.AnalysisService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping
public class AnalysisController {

    private final AnalysisService analysisService;

    @Autowired
    public AnalysisController(AnalysisService analysisService) {
        this.analysisService = analysisService;
    }

    @CrossOrigin
    @PostMapping("analysis/{inn}")
    public ResponseEntity<AnalysisResponse> analyzeCompany(@PathVariable String inn) {
        try {
            AnalysisResponse response = analysisService.performAnalysis(inn);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            System.err.println(e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
}
