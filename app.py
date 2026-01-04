from pathlib import Path

import streamlit as st

from ai_agent import sales_chat
from payments import create_checkout

import stripe
from emailer import send_download_email
from resend import find_latest_paid_session_by_email

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

if "success" in query:
    st.success("✅ Payment received! Your download is ready.")
    st.markdown("### 🎁 Download your pack")

    download_link = st.secrets.get("PROMPT_PACK_LINK", "").strip()

    if download_link:
        st.link_button("⬇️ Download the full package", download_link)
        st.caption("If the download doesn’t start, open the link in a new tab or check your email/spam.")
    else:
        st.warning("Download link not configured. Please contact support: igmargfranken@gmail.com")

    st.markdown("---")
    st.markdown("### 🚀 Want the Advanced version?")
    st.markdown("Upgrade for premium templates, funnels, and launch systems.")

    # OPTIONAL: Put your Beacons Advanced product link here
    ADVANCED_UPSELL_URL = st.secrets.get("ADVANCED_UPSELL_URL", "").strip()
    if ADVANCED_UPSELL_URL:
        st.link_button("Upgrade to Advanced ($59)", ADVANCED_UPSELL_URL)

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

st.markdown("---")
st.markdown("## 📩 Resend your download link")

st.caption("If you purchased but didn’t receive the email, enter the same email used at checkout.")

# Basic rate limit (per browser session)
if "resend_attempts" not in st.session_state:
    st.session_state.resend_attempts = 0

# Same generic message always (prevents email enumeration)
generic_msg = (
    "If a paid order is found for this email, we will send your download link shortly. "
    "Please check your inbox and spam folder."
)

with st.form("resend_form"):
    resend_email = st.text_input("Email used at checkout", placeholder="name@example.com")
    submitted = st.form_submit_button("Resend download email")

if submitted:
    st.session_state.resend_attempts += 1

    if st.session_state.resend_attempts > 5:
        st.error("Too many attempts. Please wait a bit and try again.")
    else:
        email_clean = (resend_email or "").strip().lower()
        download_link = st.secrets.get("PROMPT_PACK_LINK", "").strip()

        # If misconfigured, tell YOU (admin) but still be kind to customers
        if not download_link:
            st.warning("Delivery link is temporarily unavailable. Please contact support.")
            st.stop()

        # If empty email, do not query Stripe
        if not email_clean:
            st.success(generic_msg)