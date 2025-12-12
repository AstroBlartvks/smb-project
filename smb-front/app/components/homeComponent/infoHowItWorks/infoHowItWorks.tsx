import React from "react";

export default function InfoHowItWorks() {
    return (
        <section className="how-it-works">
            <h2>Как это работает</h2>
            <div className="steps">
                <div className="step">
                    <div className="step-icon">1</div>
                    <h3>Ввод ИНН компании</h3>
                    <p>Введите ИНН или название компании для анализа</p>
                </div>
                <div className="step">
                    <div className="step-icon">2</div>
                    <h3>Сбор данных</h3>
                    <p>Система собирает данные из ФНС, ЕГРЮЛ, новостей и судебных дел</p>
                </div>
                <div className="step">
                    <div className="step-icon">3</div>
                    <h3>Анализ моделями ИИ</h3>
                    <p>4 алгоритма машинного обучения анализируют риски</p>
                </div>
                <div className="step">
                    <div className="step-icon">4</div>
                    <h3>Получение результата</h3>
                    <p>Вероятность банкротства и рекомендации по снижению рисков</p>
                </div>
            </div>
        </section>
    );
}
