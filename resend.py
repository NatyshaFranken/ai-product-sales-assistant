import time
import streamlit as st
import stripe


def find_latest_paid_session_by_email(email: str, lookback_days: int = 30):
    """
    Looks for a paid Stripe Checkout Session matching customer email within last N days.
    Returns the session object or None.
    """
    stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]

    email = (email or "").strip().lower()
    if not email:
        return None

    created_gte = int(time.time()) - (lookback_days * 24 * 60 * 60)

    # Pull recent sessions (sufficient for low-volume stores; can be improved later)
    sessions = stripe.checkout.Session.list(limit=100)

    candidates = []
    for s in sessions.data:
        try:
            # Filter by time
            if s.created < created_gte:
                continue

            # Only paid
            if getattr(s, "payment_status", "") != "paid":
                continue

            # Match email
            details = getattr(s, "customer_details", None)
            if not details or not getattr(details, "email", ""):
                continue

            if details.email.strip().lower() == email:
                candidates.append(s)

        except Exception:
            continue

    if not candidates:
        return None

    # Return most recent paid session
    candidates.sort(key=lambda x: x.created, reverse=True)
    return candidates[0]