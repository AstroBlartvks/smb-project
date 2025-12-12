import React from "react";

export default function DataSources() {
    return (
        <section className="data-sources">
            <h2>Источники данных</h2>
            <div className="sources-grid">
                <div className="source-item">
                    <h3>ФНС и ЕГРЮЛ</h3>
                    <p>Финансовая отчетность, реквизиты, учредители</p>
                </div>
                <div className="source-item">
                    <h3>Новости и СМИ</h3>
                    <p>Упоминания в СМИ, тональность новостей</p>
                </div>
                <div className="source-item">
                    <h3>Судебные дела</h3>
                    <p>Арбитражные дела, иски, исполнительные производства</p>
                </div>
                <div className="source-item">
                    <h3>Связи компаний</h3>
                    <p>Поставщики, покупатели, аффилированные лица</p>
                </div>
            </div>
        </section>
    );
}
