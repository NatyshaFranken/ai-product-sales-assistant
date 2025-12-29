from pathlib import Path
import os

import streamlit as st
from PIL import Image

from ai_agent import sales_chat
from payments import create_checkout

import stripe
from emailer import send_download_email

# =============================
# PAGE CONFIG (MUST BE FIRST)
# =============================
st.set_page_config(
    page_title="AI Sales Assistant",
    page_icon="🤖",
    layout="centered"
)
# =============================
# LOAD ENV / SECRETS
# =============================
PROMPT_PACK_LINK = st.secrets.get("PROMPT_PACK_LINK", "").strip()

# =============================
# SUCCESS / CANCEL HANDLING
# =============================
query = st.query_params
query = st.query_params

if "success" in query:
    st.success("✅ Payment received! Your download is ready.")
    st.markdown("### 🎁 Download your pack")

    download_link = st.secrets.get("PROMPT_PACK_LINK", "").strip()

    # Show download link on page
    if download_link:
        st.markdown(f"👉 [Download here]({download_link})")
    else:
        st.warning("Download link not configured.")

    # --- AUTO EMAIL DELIVERY (Backup) ---
    session_id = query.get("session_id", "")
    if session_id and download_link:
        # prevent duplicate emails on rerun/refresh
        flag_key = f"email_sent_{session_id}"
        if not st.session_state.get(flag_key, False):
            try:
                # Stripe API key should already be set in payments.py,
                # but we set it again defensively here:
                stripe.api_key = st.secrets.get("STRIPE_SECRET_KEY", "")

                session = stripe.checkout.Session.retrieve(session_id)
                customer_email = ""
                if session and session.get("customer_details"):
                    customer_email = session["customer_details"].get("email", "") or ""

                if customer_email:
                    send_download_email(customer_email, download_link)
                    st.session_state[flag_key] = True
                    st.info(f"📩 Download link emailed to: {customer_email}")
                else:
                    st.warning("Could not read customer email from Stripe (email not sent).")

            except Exception as e:
                st.warning("⚠️ Payment succeeded, but email delivery failed.")
                st.exception(e)

    st.caption("If the link doesn’t open, check your email.")
    st.stop()

# =============================
# STYLING (SAFE CSS)
# =============================
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        max-width: 750px;
    }

    h1, h2, h3 {
        letter-spacing: -0.5px;
    }

    div.stButton > button {
        background: #635BFF !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 700 !important;
        border: none !important;
    }

    div.stButton > button:hover {
        opacity: 0.92;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =============================
# LOGO (SAFE LOAD)
# =============================
logo_path = Path(__file__).parent / "logo.png"
if logo_path.exists():
    try:
        st.image(str(logo_path), width=120)
    except Exception:
        st.warning("Logo found but could not be displayed.")

# =============================
# HERO SECTION (STEP 1 – CONVERSION)
# =============================
st.title("🤖 AI Product Sales Assistant")

st.markdown("""
✔ **500+ ready-to-use AI prompts**  
✔ **For beginners (no tech skills)**  
✔ **Works with ChatGPT, Claude, Gemini**  
✔ **Instant download after purchase**
""")

# =============================
# CHAT
# =============================
if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Ask anything about AI products")

if user_input:
    reply = sales_chat(user_input)
    st.session_state.chat.append(("You", user_input))
    st.session_state.chat.append(("AI", reply))

for speaker, msg in st.session_state.chat:
    st.markdown(f"**{speaker}:** {msg}")

# =============================
# BUY SECTION
# =============================
st.subheader("🔥 Buy Now")
st.markdown("### 🔥 Buy once. Use forever.")

if st.button("Buy AI Prompt Mega Pack for Beginners"):
    try:
        checkout_url = create_checkout("prompt_pack")
        st.success("✅ Redirecting you to secure Stripe checkout...")
        st.link_button("👉 Continue to Stripe Checkout", checkout_url)
        st.stop()
    except Exception as e:
        st.error("❌ Stripe checkout failed. This is the exact error:")
        st.exception(e)
        st.stop()