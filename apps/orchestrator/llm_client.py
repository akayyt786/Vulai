from openai import OpenAI
from django.conf import settings
from utils.error_logger import log_error

class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL
        )
        self.model = settings.LLM_MODEL
        self.max_tokens = settings.LLM_MAX_TOKENS

    def call_llm(self, system_prompt, user_prompt):
        """
        Calls the LLM with system and user prompts.
        Returns the raw string response.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.0 # Deterministic for reasoning
            )
            return response.choices[0].message.content
        except Exception as e:
            log_error(
                "apps.orchestrator.llm_client", "LLMAPIError",
                f"Error calling LLM API: {str(e)}",
                {"model": self.model, "base_url": settings.LLM_BASE_URL},
                exc=e
            )
            return ""
