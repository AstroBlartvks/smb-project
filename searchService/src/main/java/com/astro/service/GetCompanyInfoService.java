package com.astro.service;

import com.astro.exceptions.InfoOfThisCompanyIsBadException;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@Service
public class GetCompanyInfoService {

    public Map<String, Object> parseCompanyInfoFromPage(String url) throws IOException, InfoOfThisCompanyIsBadException {
        Document doc = Jsoup.connect(url)
                .userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
                .timeout(10000)
                .get();

        Element table = findCompanyInfoTable(doc);

        if (table == null) {
            throw new InfoOfThisCompanyIsBadException("No table found");
        }

        return parseTable(table);
    }

    private Element findCompanyInfoTable(Document doc) {

        Element table = doc.selectFirst("table.two-columns-table");
        if (table != null) return table;

        table = doc.selectFirst("table.table.two-columns-table.table-sm");
        if (table != null) return table;

        Elements allTables = doc.select("table");
        for (Element t : allTables) {
            String text = t.text();
            if (containsCompanyInfo(text)) {
                return t;
            }
        }

        table = doc.selectFirst("div:contains(Сокращённое наименование) ~ table");
        if (table != null) return table;

        return null;
    }

    private boolean containsCompanyInfo(String text) {
        String[] keywords = {
                "Сокращённое наименование",
                "Полное наименование",
                "Дата регистрации",
                "Статус",
                "Регион",
                "Уставный капитал"
        };

        int matches = 0;
        for (String keyword : keywords) {
            if (text.contains(keyword)) {
                matches++;
            }
        }

        return matches >= 3;
    }


    private Map<String, Object> parseTable(Element table) {
        Map<String, Object> result = new HashMap<>();

        Elements rows = table.select("tr");

        for (Element row : rows) {
            Elements cells = row.select("td");

            if (cells.size() >= 2) {
                String key = cells.get(0).text()
                        .replace(":", "")
                        .trim();

                String value = extractValueFromCell(cells.get(1));

                if (!key.isEmpty() && !value.isEmpty()) {
                    result.put(key, value);
                }
            }
        }

        return result;
    }

    private String extractValueFromCell(Element cell) {
        Element clonedCell = cell.clone();

        clonedCell.select("button").remove();

        clonedCell.select("i.mso-icon, span.fbcMcs, span.iGqhJH").remove();

        clonedCell.select("span[class*=fuvqZz], span[class*=feVRDp], span[class*=hMKRHA]").remove();

        clonedCell.select("div:empty, span:empty").remove();

        return clonedCell.text()
                .replaceAll("\\s+", " ")
                .replace("&nbsp;", " ")
                .trim();
    }
}
