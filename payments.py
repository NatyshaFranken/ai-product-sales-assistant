import streamlit as st
import stripe
from products import PRODUCTS

# Stripe key from Streamlit Secrets (works on Cloud)
stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]

# Your domain from secrets (fallback to localhost for local testing)
DOMAIN = st.secrets.get("DOMAIN", "http://localhost:8501").rstrip("/")


def create_checkout(product_key: str) -> str:
    product = PRODUCTS[product_key]

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": product["name"]},
                    "unit_amount": int(product["price"]),  # cents
                },
                "quantity": 1,
            }
        ],
        success_url=f"{DOMAIN}/?success=true&session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{DOMAIN}/?canceled=true",
        metadata={"product_key": product_key},
    )

    return session.url