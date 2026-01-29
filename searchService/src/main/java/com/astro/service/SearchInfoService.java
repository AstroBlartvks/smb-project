package com.astro.service;

import com.astro.dto.SearchRequest;
import com.astro.dto.SearchResponse;
import com.astro.exceptions.InfoOfThisCompanyIsBadException;
import com.astro.exceptions.TaxpayerIdNumberIsBadException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@Service
public class SearchInfoService {
    private final ObjectMapper mapper = new ObjectMapper();
    private final ContrAgentsService contrAgentsService;
    private final GetCompanyInfoService getCompanyInfoService;

    @Autowired
    public SearchInfoService(ContrAgentsService contrAgentsService,
                             GetCompanyInfoService getCompanyInfoService) {
        this.contrAgentsService = contrAgentsService;
        this.getCompanyInfoService = getCompanyInfoService;
    }

    public SearchResponse search(SearchRequest request) {
        String result;

        try {
            String uri = contrAgentsService.getURI(request.TaxpayerIdentificationNumber().replace(" ", ""));
            Map<String, Object> info = getCompanyInfoService.parseCompanyInfoFromPage(uri);
            result = mapper.writeValueAsString(info);
        } catch (TaxpayerIdNumberIsBadException | InfoOfThisCompanyIsBadException e) {
            return new SearchResponse(e.getMessage());
        } catch (IOException e) {
            return new SearchResponse("Ошибка с доступом на сайт-ресурс!");
        }

        return new SearchResponse(result);
    }

    public Map<String, Object> getInfoMap(SearchRequest request) throws IOException {
        return new HashMap<String, Object>() {{}};
    }
}
