"""Local, free chatbot logic.

This intentionally avoids paid APIs and heavy ML dependencies.
It answers common questions using a small FAQ knowledge base + fuzzy matching.

Later, you can swap `generate_reply()` to call a real model (local Ollama or hosted LLM)
without changing the frontend widget or API contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Iterable, Optional

from .models import DeliverySettings, SiteSetting


@dataclass(frozen=True)
class FAQEntry:
    intent: str
    examples: tuple[str, ...]
    answer: str


def _norm(text: str) -> str:
    return " ".join((text or "").strip().lower().split())


def _score(query: str, example: str) -> float:
    # Simple fuzzy score in [0, 1]
    return SequenceMatcher(a=_norm(query), b=_norm(example)).ratio()


def _first_site_settings() -> Optional[SiteSetting]:
    try:
        return SiteSetting.objects.first()
    except Exception:
        return None


def _first_delivery_settings() -> Optional[DeliverySettings]:
    try:
        return DeliverySettings.objects.first()
    except Exception:
        return None


def build_faq() -> list[FAQEntry]:
    site = _first_site_settings()
    delivery = _first_delivery_settings()

    site_name = site.site_name if site and site.site_name else "Sip and Sunshine"
    phone = site.phone if site and site.phone else ""
    email = site.email if site and site.email else ""
    address = site.address if site and site.address else ""

    delivery_enabled = delivery.delivery_enabled if delivery else True
    pickup_enabled = delivery.pickup_enabled if delivery else True
    min_delivery_amount = float(delivery.min_delivery_amount) if delivery and delivery.min_delivery_amount is not None else 10.0
    min_pickup_amount = float(delivery.min_pickup_amount) if delivery and delivery.min_pickup_amount is not None else 5.0
    est_pickup = int(delivery.estimated_pickup_time) if delivery and delivery.estimated_pickup_time is not None else 15
    est_delivery = int(delivery.estimated_delivery_time) if delivery and delivery.estimated_delivery_time is not None else 30

    contact_bits = []
    if phone:
        contact_bits.append(f"Phone: {phone}")
    if email:
        contact_bits.append(f"Email: {email}")
    if address:
        contact_bits.append(f"Address: {address}")

    contact_line = "\n".join(contact_bits) if contact_bits else "You can reach us via the Contact page."

    delivery_text = (
        f"Delivery is currently {'available' if delivery_enabled else 'not available'}. "
        f"Pickup is currently {'available' if pickup_enabled else 'not available'}.\n"
        f"Estimated pickup time: ~{est_pickup} minutes.\n"
        f"Estimated delivery time: ~{est_delivery} minutes.\n"
        f"Minimum delivery amount: €{min_delivery_amount:.2f}.\n"
        f"Minimum pickup amount: €{min_pickup_amount:.2f}."
    )

    return [
        FAQEntry(
            intent="greeting",
            examples=("hi", "hello", "hey", "good morning", "good evening"),
            answer=f"Hi! I’m the {site_name} assistant. Ask me about menu, delivery, pickup, reservations, or your order tracking.",
        ),
        FAQEntry(
            intent="thanks",
            examples=("thanks", "thank you", "thx", "thanks a lot", "thank u"),
            answer="You’re welcome! If you need anything else, just ask.",
        ),
        FAQEntry(
            intent="goodbye",
            examples=("bye", "goodbye", "see you", "see ya"),
            answer="Thanks for visiting! If you need help later, I’ll be here.",
        ),
        FAQEntry(
            intent="hours",
            examples=("open hours", "opening hours", "what time are you open", "when do you close"),
            answer="Our opening hours are shown in the footer. If you tell me the day, I can help you double-check.",
        ),
        FAQEntry(
            intent="menu",
            examples=("menu", "show menu", "what do you have", "food", "drinks"),
            answer="You can view our menu on the Menu page. Use “Add to Order” to build your cart and checkout.",
        ),
        FAQEntry(
            intent="specials",
            examples=(
                "special",
                "specials",
                "today's special",
                "todays special",
                "chef special",
                "chef's special",
                "featured",
                "featured item",
                "lunch menu",
                "lunch",
            ),
            answer="For featured items and today’s specials, please check the Home page and the Menu page (they’re kept up to date there).",
        ),
        FAQEntry(
            intent="contact",
            examples=("contact", "phone number", "email", "address", "location", "where are you"),
            answer=contact_line,
        ),
        FAQEntry(
            intent="delivery_pickup",
            examples=(
                "do you deliver",
                "delivery",
                "pickup",
                "takeaway",
                "minimum order",
                "how long for delivery",
                "how long for pickup",
            ),
            answer=delivery_text,
        ),
        FAQEntry(
            intent="reservation",
            examples=("reservation", "book a table", "table booking", "reserve"),
            answer="You can reserve a table from the Reservation page in the menu.",
        ),
        FAQEntry(
            intent="payment",
            examples=("payment", "pay", "cash", "card", "stripe", "paypal"),
            answer="We support cash, Stripe (card), and PayPal for pickup/delivery. Dine-in is pay-at-table.",
        ),
        FAQEntry(
            intent="tracking",
            examples=(
                "my order",
                "track order",
                "order status",
                "where is my order",
                "tracking",
                "SIP-000015",
            ),
            answer="You can track your order on the Track Order page. If you have an order reference like SIP-000015, paste it there.",
        ),
        FAQEntry(
            intent="apology",
            examples=("sorry", "my bad", "apologies", "oops", "sry"),
            answer="No worries — how can I help? You can ask about delivery, pickup, reservations, payments, or tracking.",
        ),
        FAQEntry(
            intent="fallback",
            examples=(),
            answer="I can help with delivery, pickup, reservations, payments, and tracking. If you need a human, please use the Contact page.",
        ),
    ]


def generate_reply(message: str, *, threshold: float = 0.62) -> tuple[str, str, float]:
    """Return (reply, intent, confidence)."""
    message = (message or "").strip()
    if not message:
        return ("Please type a question.", "empty", 0.0)

    faq = build_faq()
    best_entry = None
    best = 0.0

    for entry in faq:
        for ex in entry.examples:
            score = _score(message, ex)
            if score > best:
                best = score
                best_entry = entry

    if best_entry is not None and best >= threshold:
        return (best_entry.answer, best_entry.intent, float(best))

    fallback = next((e for e in faq if e.intent == "fallback"), None)
    return ((fallback.answer if fallback else "How can I help?"), "fallback", float(best))
