import os
from google import genai
import logging

logging.getLogger("google_genai").setLevel(logging.ERROR)


MODEL_NAME = "gemini-3.8-flash"

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set")
        _client = genai.Client(api_key=api_key)
    return _client


def llm_summarize_change(change: dict) -> str:
    client = _get_client()

    prompt = f"""You are writing one entry in an email report about changes to the U.S. Harmonized Tariff Schedule (HTS), for a member of the Consumer Product Safety Commission (CPSC) who may not be a tariff expert.

For the change below, write 2-3 plain-language sentences that:
1. State clearly what changed (the HTS code, its product description, and the specific field/rate that changed).
2. Explain what this means in practical terms for someone importing or exporting this product (e.g. cost impact direction, whether this is a new classification becoming available, or one disappearing).
3. Do NOT speculate about *why* the change happened (no guessing about trade policy, negotiations, etc.) — only describe the change itself and its direct practical effect.
4. Give the change a score from 1 to 10, with 1 being not at all relevant and 10 being urgently relevant with regards to the line of work the Consumer Product Safety Commission is in. Also provide a very brief justification as to why you assigned that score.

Change data:
{change}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    text = response.text.strip()
    if not text:
        raise ValueError("Empty response from Gemini")
    return text