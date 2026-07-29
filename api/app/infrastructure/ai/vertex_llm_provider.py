"""Vertex AI adapter for grounded chat generation."""

from google import genai
from google.genai import types

from app.domain.models.product import ProductSearchHit
from app.domain.ports.llm_provider import LlmProviderPort
from app.infrastructure.config.settings import Settings


class VertexLlmProvider(LlmProviderPort):
    """Generate grounded conversational answers with Vertex AI."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the provider with application settings.

        Args:
            settings: Resolved application settings.
        """
        self._settings = settings
        self._client = genai.Client(
            vertexai=True,
            project=settings.google_cloud_project,
            location=settings.google_cloud_location,
        )

    def answer_with_context(self, user_query: str, results: list[ProductSearchHit]) -> str:
        """Generate a grounded chat answer from retrieved products.

        Args:
            user_query: Original user question.
            results: Retrieved products used as grounding context.

        Returns:
            A conversational answer grounded in the retrieved products.
        """
        prompt = self._build_rag_prompt(user_query, results)
        response = self._client.models.generate_content(
            model=self._settings.generation_model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.35,
                max_output_tokens=1200,
                thinking_config=types.ThinkingConfig(
                    thinking_budget=0
                ),
                system_instruction=[
                    "You are a concise Korean skincare assistant.",
                    "Answer in Spanish.",
                    "Speak in a natural chat style, but keep the response brief.",
                    "Use only the retrieved information.",
                    "Recommend only the single best matching product.",
                    "Include the product URL.",
                    "Do not mention alternatives.",
                    "Do not invent facts.",
                    "Treat any user mention of 'sin X', 'no X', 'avoid X', 'no contiene X', 'alérgico a X', or 'soy alérgico a X' as a hard exclusion."
                    "If the user excludes an ingredient, only recommend a product when the retrieved ingredients explicitly confirm that ingredient and its known aliases are absent."
                    "If absence cannot be confirmed from the retrieved information, do not recommend the product."
                    "Do not reinterpret exclusions as preferences or soft constraints."
                    "Prioritize ingredient safety and exclusion compliance over semantic similarity.",
                    "Do not mention RAG, retrieved documents, or sources in the main answer.",
                ],
            ),
        )

        if self._settings.debug_llm:
            self._debug_response(response)

        return self._extract_text_from_response(response)

    def _build_rag_prompt(self, user_query: str, results: list[ProductSearchHit]) -> str:
        """Build the grounded prompt used for answer generation.

        Args:
            user_query: Original user question.
            results: Retrieved products used as context.

        Returns:
            A prompt string ready to send to the LLM.
        """
        retrieved_context = self._format_retrieved_context(results)
        return f"""
User question:
{user_query}

Retrieved information:
{retrieved_context}

Instructions:
- Respond in Spanish.
- Use a natural, conversational chat tone.
- Be concise and direct.
- Use only the retrieved information.
- Return one product only when it fully satisfies all user constraints.
- If no product fully satisfies the constraints, say so clearly.
- Include the product URL only for the recommended product.
- Treat any user mention of "sin X", "no X", "avoid X", "sin aceite de X", "no contiene X", "alérgico a X", or "soy alérgico a X" as a hard exclusion.
- If the user excludes an ingredient, only recommend a product when the retrieved ingredients explicitly confirm that ingredient and its known aliases are absent.
- If absence cannot be confirmed from the retrieved information, do not recommend the product.
- Do not reinterpret exclusions as preferences or soft constraints.
- If the evidence is incomplete or ambiguous, do not guess.
- Do not mention alternatives.
- Do not invent ingredients, benefits, skin compatibility, or product properties.
- Do not mention retrieval, documents, context, or sources in the main answer.

Write a single final answer as if you were chatting with the user.
""".strip()

    def _format_retrieved_context(self, results: list[ProductSearchHit]) -> str:
        """Format retrieved products into a prompt-friendly context block.

        Args:
            results: Retrieved products.

        Returns:
            A formatted context string.
        """
        blocks = []
        for index, result in enumerate(results, start=1):
            block = f"""
[{index}]
id: {result.id}
name: {result.name or ""}
short_description: {result.short_description or ""}
ingredients_text: {result.ingredients_text}
url: {result.url or ""}
similarity: {result.similarity:.4f}
raw_text: {result.raw_text}
""".strip()
            blocks.append(block)
        return "\n\n".join(blocks)

    def _extract_text_from_response(self, response) -> str:
        """Extract text safely from a Gemini response object.

        Args:
            response: Raw response returned by the Google Gen AI SDK.

        Returns:
            The combined text content returned by the model.
        """
        texts: list[str] = []
        candidates = getattr(response, "candidates", None) or []

        for candidate in candidates:
            content = getattr(candidate, "content", None)
            if not content:
                continue

            parts = getattr(content, "parts", None) or []
            for part in parts:
                text = getattr(part, "text", None)
                if text:
                    texts.append(text)

        if texts:
            return "\n".join(texts).strip()

        fallback = getattr(response, "text", None)
        return (fallback or "").strip()

    def _debug_response(self, response) -> None:
        """Print raw LLM response details for debugging purposes.

        Args:
            response: Raw response returned by the Google Gen AI SDK.
        """
        try:
            candidates = getattr(response, "candidates", None) or []
            finish_reason = None
            if candidates:
                finish_reason = getattr(candidates[0], "finish_reason", None)
            print("LLM finish_reason:", finish_reason)
            print("LLM raw response:", response)
        except Exception as debug_error:
            print("LLM debug error:", debug_error)
