import json
import logging
import os
from dataclasses import dataclass
from openai import AsyncOpenAI

logger = logging.getLogger("spam-classifier")
logger.setLevel(logging.INFO)

CLASSIFICATION_SYSTEM_PROMPT = """\
You are a spam call classifier. Analyze the transcript and determine if the call is spam or not.

Return ONLY a valid JSON object with this exact structure:
{
    "is_spam": true or false,
    "confidence": a float between 0.0 and 1.0,
    "reason": "A brief one-sentence explanation of why this is or isn't spam",
    "evidence_lines": ["exact line(s) from the transcript that indicate spam, or empty array if not spam"]
}

Spam indicators:
- Trying to sell products, services, insurance, loans, investments
- Claiming to be from a bank, government, or tech support unsolicited
- Asking for personal/financial information
- Urgent threats about accounts, penalties, or legal action
- Prize/lottery winnings that require action

If there is insufficient transcript to classify, set is_spam to false with low confidence.
"""


@dataclass(frozen=True)
class ClassificationResult:
    is_spam: bool
    confidence: float
    reason: str
    evidence_lines: list[str]
    full_transcript: str


async def classify_transcript(transcript: str) -> ClassificationResult:
    if not transcript.strip():
        return ClassificationResult(
            is_spam=False,
            confidence=0.0,
            reason="No transcript to analyze",
            evidence_lines=[],
            full_transcript=transcript,
        )

    client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

    try:
        response = await client.chat.completions.create(
            model=os.environ.get("SPAM_CLASSIFICATION_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": CLASSIFICATION_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Classify this call transcript:\n\n{transcript}",
                },
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )

        raw = response.choices[0].message.content
        logger.info("Classification raw response: %s", raw)

        result = json.loads(raw)

        return ClassificationResult(
            is_spam=bool(result.get("is_spam", False)),
            confidence=float(result.get("confidence", 0.0)),
            reason=str(result.get("reason", "")),
            evidence_lines=result.get("evidence_lines", []),
            full_transcript=transcript,
        )

    except Exception as e:
        logger.error("Classification failed: %s", e, exc_info=True)
        return ClassificationResult(
            is_spam=False,
            confidence=0.0,
            reason=f"Classification error: {e}",
            evidence_lines=[],
            full_transcript=transcript,
        )
