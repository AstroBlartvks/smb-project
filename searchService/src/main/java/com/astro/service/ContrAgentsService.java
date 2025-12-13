package com.astro.service;

import com.astro.exceptions.TaxpayerIdNumberIsBadException;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.springframework.stereotype.Service;

import java.io.IOException;

@Service
public class ContrAgentsService {

    public String getURI(String TaxpayerIdentificationNumber) throws IOException, TaxpayerIdNumberIsBadException {
        if (TaxpayerIdentificationNumber == null || TaxpayerIdentificationNumber.isEmpty()) {
            throw new TaxpayerIdNumberIsBadException("Taxpayer is undefined");
        }

        if (TaxpayerIdentificationNumber.length() != 10) {
            throw new TaxpayerIdNumberIsBadException("Taxpayer should be 10 digits long");
        }

        String uri = "https://datanewton.ru/search?query={TPIN}&type=all";
        Document doc = Jsoup.connect(uri.replace("{TPIN}", TaxpayerIdentificationNumber))
                .userAgent("Mozilla/5.0")
                .timeout(2000)
                .get();

        Element link = doc.select(".list-group-item-action").first();

        if (link == null){
            throw new TaxpayerIdNumberIsBadException("Taxpayer doesn't exist");
        }

        return "https://datanewton.ru" + link.attr("href");
    }
}
