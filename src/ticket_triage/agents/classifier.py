import json
import logging
import re

from src.ticket_triage.config import ClassifierBackend, settings
from src.ticket_triage.graph.state import TicketState
from src.ticket_triage.models import Category, ClassificationResult, RiskTier, Urgency
from src.ticket_triage.sanitize import sanitize_ticket

logger = logging.getLogger(__name__)

_PROMPT = """\
You are a support ticket classifier. Analyze the ticket below and return ONLY a JSON object.

JSON fields:
- "category": one of ["vpn","password","software","billing","security","email","hardware","data_loss","other"]
- "urgency": one of ["low","medium","high","critical"]
- "risk_tier":
    "low"    = routine issue, no data or security risk
    "medium" = affects productivity or requires account changes
    "high"   = security incident, data loss, financial or legal impact
- "reasoning": brief explanation, max 80 words

<ticket>
{ticket_text}
</ticket>

Respond with valid JSON only. No prose, no markdown."""


def _parse(raw: str) -> ClassificationResult:
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in classifier response")
    return ClassificationResult(**json.loads(match.group()))


def _fallback() -> ClassificationResult:
    return ClassificationResult(
        category=Category.OTHER,
        urgency=Urgency.HIGH,
        risk_tier=RiskTier.HIGH,
        reasoning="Classification failed — defaulting to high risk for safety.",
    )


def _call_classifier(prompt: str) -> str:
    if settings.classifier_backend == ClassifierBackend.OLLAMA:
        import ollama

        response = ollama.chat(
            model=settings.classifier_model,
            messages=[{"role": "user", "content": prompt}],
            format="json",
            options={"temperature": 0},
        )
        return response.message.content

    if settings.classifier_backend == ClassifierBackend.GROQ:
        from groq import Groq

        client = Groq(api_key=settings.groq_api_key)
        response = client.chat.completions.create(
            model=settings.classifier_model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0,
        )
        return response.choices[0].message.content

    raise ValueError(f"Unsupported classifier backend: {settings.classifier_backend}")


def classify_ticket(state: TicketState) -> dict:
    ticket_text = sanitize_ticket(state["ticket_text"])
    prompt = _PROMPT.format(ticket_text=ticket_text)

    try:
        raw = _call_classifier(prompt)
        classification = _parse(raw)
    except Exception as exc:
        logger.warning("Classifier error: %s — using high-risk fallback", exc)
        classification = _fallback()

    logger.info(
        "Ticket %s classified as %s / risk=%s",
        state["ticket_id"],
        classification.category.value,
        classification.risk_tier.value,
    )
    return {"classification": classification}
