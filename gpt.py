from typing import Dict, List

import httpx

from const import AI_BASE_URL, MODEL_NAME, OPENAI_API_KEY


class GptAgent:
    def __init__(
            self,
            model: str = MODEL_NAME,
            max_tokens: int = 3354,
            temperature: float = 0,
            timeout: int = 60,
            max_attempts: int = 3,
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout
        self.max_attempts = max_attempts

        if not OPENAI_API_KEY:
            raise RuntimeError("Please set the DEEPSEEK_API_KEY environment variable")

        self.openai_api_key = OPENAI_API_KEY

    def ask_ai(
            self,
            words: str,
    ) -> str:
        """Send request to AI and get answer text.

        Args:
            system_message: System context message (maybe blank str).
            words: Instruction message.
            message_history: Message history.
            temperature: Temperature.

        Returns:
            Answer from API.

        Raises:
            RuntimeError: If no correct answer was received after several attempts.
        """
        default_temperature = self.temperature

        url = f"https://{AI_BASE_URL}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "content-type": "application/json"
        }

        messages = []

        system_message="""
        Дан спсиок слов разделенный запятыми. 
        Найди из них глаголы, страны, имена, фамилии, прилагательные, ласкательные и уменьшительные слова, города, марки машин. 
        Дай ответ ввиде json массива без лишних слов и синволов, не обособля код ковычками
        Пример ответа:
        ["москва", "иван", "мерседес"]
        """

        if system_message:
            messages.append({"role": "system", "content": system_message})

        messages.append({"role": "user", "content": words})

        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": 0,
            "messages": messages,
        }

        self.temperature = default_temperature

        for attempt in range(1, self.max_attempts + 1):
            try:
                with httpx.Client() as client:
                    response = client.post(
                        url=url,
                        headers=headers,
                        json=payload,
                        timeout=self.timeout
                    )
                    print(response.status_code)
                    if response.status_code != 200:
                        print()

                    return response.json()
            except Exception as e:
                print(f"OpenAI API attempt {attempt} encountered an error: {e}")

        raise RuntimeError("Failed to get response from OpenAI API after multiple attempts")