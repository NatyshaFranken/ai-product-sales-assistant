import os
import stripe
from products import PRODUCTS

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_checkout(product_key: str) -> str:
    product = PRODUCTS[product_key]

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": product["name"]},
                    "unit_amount": product["price"],  # must be in cents (e.g. 2900 for $29)
                },
                "quantity": 1,
            }
        ],
        success_url="http://localhost:8501/?success=1&session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://localhost:8501/?canceled=1",
        metadata={"product_key": product_key},
    )

    return checkout_session.url