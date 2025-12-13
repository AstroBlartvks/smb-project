package com.astro.controller;


import com.astro.dto.SearchRequest;
import com.astro.dto.SearchResponse;
import com.astro.service.SearchInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping
public class SearchController {
    private final SearchInfoService searchInfoService;

    @Autowired
    public SearchController(SearchInfoService searchInfoService) {
        this.searchInfoService = searchInfoService;
    }

    @CrossOrigin
    @PostMapping("/search")
    public ResponseEntity<SearchResponse> checkPoint(@RequestBody SearchRequest request) {
        SearchResponse response = searchInfoService.search(request);
        return ResponseEntity.ok(response);
    }

}
