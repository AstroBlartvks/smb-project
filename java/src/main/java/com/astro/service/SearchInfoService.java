package com.astro.service;

import com.astro.dto.SearchRequest;
import com.astro.dto.SearchResponse;
import org.springframework.stereotype.Service;

@Service
public class SearchInfoService {

    public SearchResponse search(SearchRequest request) {
        return new SearchResponse("Компания с ИНН " + request.TaxpayerIdentificationNumber().replace(" ", "") + " будет расмотрена!");
    }
}
