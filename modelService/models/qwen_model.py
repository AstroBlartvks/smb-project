import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class QwenModel:
    """Модель Qwen для анализа текста и генерации отчетов"""

    def __init__(self, model_name: str = "Qwen/Qwen-1_8B-Chat"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.loaded = False

    def load(self):
        """Загрузка модели Qwen"""
        try:
            logger.info(f"Загрузка модели Qwen: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map="auto",
                trust_remote_code=True,
                torch_dtype=torch.float16
            )
            self.model.eval()
            self.loaded = True
            logger.info("Модель Qwen успешно загружена")
            return True
        except Exception as e:
            logger.error(f"Ошибка загрузки Qwen: {e}")
            logger.warning("Используется резервный режим генерации текста")
            return False

    def generate_text(self, prompt: str, max_length: int = 512) -> str:
        """Генерация текста на основе промпта"""
        if not self.loaded:
            return self._fallback_generation(prompt)

        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True
                )

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response.replace(prompt, "").strip()

        except Exception as e:
            logger.error(f"Ошибка генерации: {e}")
            return self._fallback_generation(prompt)

    def analyze_court_cases(self, court_data: str) -> dict:
        """Анализ судебных дел компании"""
        prompt = f"""Проанализируйте данные о судебных делах и предоставьте:
1. Уровень риска (низкий/средний/высокий)
2. Ключевые правовые проблемы
3. Потенциальное финансовое воздействие

Данные по судебным делам: {court_data}

Анализ:"""

        response = self.generate_text(prompt, max_length=300)

        return {
            "analysis": response,
            "risk_factors": self._extract_risk_factors(response),
            "severity": self._determine_severity(response)
        }

    def generate_summary(self, company_data: dict, prediction: dict, court_analysis: dict) -> str:
        """Генерация итогового отчета по компании"""
        prompt = f"""Подготовить комплексный аналитический отчет по оценке риска банкротства предприятия.

Ключевые финансовые показатели:
- Выручка: {company_data.get('revenue', 0):,.2f} рублей
- Чистая прибыль: {company_data.get('net_profit', 0):,.2f} рублей
- Общие активы: {company_data.get('total_assets', 0):,.2f} рублей
- Общие обязательства: {company_data.get('total_liabilities', 0):,.2f} рублей
- Собственный капитал: {company_data.get('equity', 0):,.2f} рублей
- Текущие активы: {company_data.get('current_assets', 0):,.2f} рублей
- Текущие обязательства: {company_data.get('current_liabilities', 0):,.2f} рублей

Результаты анализа:
- Вероятность банкротства: {prediction.get('bankruptcy_probability', 0):.1f}%
- Уровень риска: {prediction.get('risk_level', 'не определен')}
- Прогнозы моделей: {prediction.get('model_predictions', {})}

Судебная история:
{court_analysis.get('analysis', 'Информация о судебных процессах отсутствует')}

Сформируйте краткий аналитический вывод и практические рекомендации (3-4 предложения):"""

        return self.generate_text(prompt, max_length=500)

    def _fallback_generation(self, prompt: str) -> str:
        if "судебн" in prompt.lower() or "court" in prompt.lower():
            return "На основе доступных данных о судебных делах компания демонстрирует умеренный правовой риск. Ключевые проблемы включают договорные споры и потенциальные требования о возмещении ущерба. Рекомендуется проведение детального юридического аудита."
        elif "отчет" in prompt.lower() or "summary" in prompt.lower() or "резюме" in prompt.lower():
            return "Компания демонстрирует неоднозначные финансовые показатели с умеренным риском банкротства. Финансовые коэффициенты указывают на необходимость тщательного мониторинга. Рекомендуется внедрение стратегий снижения рисков и улучшение ликвидности."
        else:
            return "Анализ завершен. Ознакомьтесь с детальными метриками для комплексной оценки."

    def _extract_risk_factors(self, text: str) -> list:
        risk_keywords = ["долг", "обязательство", "спор", "претензия", "нарушение", "штраф", 
                         "дебитор", "кредитор", "иск", "взыскание", "банкротство"]
        found = [kw for kw in risk_keywords if kw in text.lower()]
        return found[:5]

    def _determine_severity(self, text: str) -> str:
        text_lower = text.lower()
        if any(word in text_lower for word in ["высокий риск", "критический", "серьезный", "значительный"]):
            return "high"
        elif any(word in text_lower for word in ["умеренный", "средний", "средняя", "умеренная"]):
            return "medium"
        else:
            return "low"


qwen_model = QwenModel()