"""
app.py
------
Image Generation Chatbot — Streamlit frontend.

This file ONLY handles UI/UX and orchestration. All API logic lives in
utils/api_client.py and all prompt logic lives in utils/prompt_builder.py,
keeping the codebase clean and modular.

Run locally:
    streamlit run app.py
"""

import os
import io
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from utils.prompt_builder import build_final_prompt, get_style_list, get_style_description
from utils.api_client import generate_image, ImageGenerationError
from utils.random_prompts import get_random_prompt

# ──────────────────────────────────────────────────────────────────────
# Setup
# ──────────────────────────────────────────────────────────────────────
load_dotenv()  # loads .env file locally (no-op on Streamlit Cloud)

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide",
)

def get_api_token():
    """
    Reads the Hugging Face API token from environment variables.
    Locally this comes from .env (via python-dotenv).
    On Streamlit Community Cloud, this comes from st.secrets instead,
    so we check both sources.
    """
    token = os.getenv("HF_API_TOKEN")
    if not token:
        try:
            token = st.secrets["HF_API_TOKEN"]
        except Exception:
            token = None
    return token


# Session state initialization
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {prompt, style, final_prompt, images, timestamp}
if "prompt_text" not in st.session_state:
    st.session_state.prompt_text = ""
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# ──────────────────────────────────────────────────────────────────────
# Theme toggle (bonus) — simple CSS injection
# ──────────────────────────────────────────────────────────────────────
def inject_theme_css(theme: str):
    if theme == "Dark":
        st.markdown("""
            <style>
            .stApp { background-color: #0f0f12; color: #f0f0f0; }
            </style>
        """, unsafe_allow_html=True)
    # "Light" uses Streamlit's default — no override needed


# ──────────────────────────────────────────────────────────────────────
# Sidebar — settings & theme toggle
# ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    st.session_state.theme = st.radio(
        "Theme", ["Dark", "Light"],
        index=0 if st.session_state.theme == "Dark" else 1,
        horizontal=True,
    )

    st.divider()

    st.subheader("🖼️ Image Options")
    image_size = st.selectbox(
        "Image size",
        ["512x512", "768x768", "1024x1024"],
        index=0,
        help="Larger images take longer to generate.",
    )
    num_images = st.slider(
        "Number of images", min_value=1, max_value=4, value=1,
        help="Generate multiple variations of the same prompt at once.",
    )

    st.divider()
    st.subheader("🚫 Negative Prompt")
    negative_prompt = st.text_area(
        "Things to avoid (optional)",
        placeholder="e.g. blurry, low quality, watermark, text",
        height=80,
    )

    st.divider()
    api_token = get_api_token()
    if api_token:
        st.success("✅ API token loaded")
    else:
        st.error("⚠️ No API token found. Add HF_API_TOKEN to .env or Streamlit Secrets.")

inject_theme_css(st.session_state.theme)

# ──────────────────────────────────────────────────────────────────────
# Main UI
# ──────────────────────────────────────────────────────────────────────
st.title("🎨 AI Image Generation Chatbot")
st.caption(
    "Type a prompt, pick a style, and generate an AI image — powered by "
    "Hugging Face's FLUX.1-schnell model."
)

col_input, col_random = st.columns([5, 1])
with col_input:
    user_prompt = st.text_input(
        "Describe the image you want to create",
        value=st.session_state.prompt_text,
        placeholder="e.g. A futuristic Indian city at night",
        key="prompt_input",
    )
with col_random:
    st.write("")  # vertical spacer to align button with text input
    st.write("")
    if st.button("🎲 Surprise Me", use_container_width=True):
        st.session_state.prompt_text = get_random_prompt()
        st.rerun()

st.markdown("**Choose a style**")
style = st.radio(
    label="Style",
    options=get_style_list(),
    horizontal=True,
    label_visibility="collapsed",
)
st.caption(f"ℹ️ {get_style_description(style)}")

generate_clicked = st.button("✨ Generate Image", type="primary", use_container_width=True)

# ──────────────────────────────────────────────────────────────────────
# Generation logic
# ──────────────────────────────────────────────────────────────────────
if generate_clicked:
    if not user_prompt.strip():
        st.warning("⚠️ Please enter a prompt before generating an image.")
    elif not api_token:
        st.error(
            "⚠️ No Hugging Face API token configured. "
            "Add `HF_API_TOKEN` to your `.env` file (see README.md)."
        )
    else:
        final_prompt = build_final_prompt(user_prompt, style)
        width, height = map(int, image_size.split("x"))

        with st.spinner(f"Generating {num_images} image(s) — this can take 10-30 seconds…"):
            try:
                images = generate_image(
                    prompt=final_prompt,
                    api_token=api_token,
                    negative_prompt=negative_prompt,
                    width=width,
                    height=height,
                    num_images=num_images,
                )

                # Save to history
                st.session_state.history.insert(0, {
                    "prompt": user_prompt,
                    "style": style,
                    "final_prompt": final_prompt,
                    "images": images,
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                })
                st.session_state.history = st.session_state.history[:10]  # cap history

            except ImageGenerationError as e:
                st.error(f"❌ {e}")

# ──────────────────────────────────────────────────────────────────────
# Display latest result
# ──────────────────────────────────────────────────────────────────────
if st.session_state.history:
    latest = st.session_state.history[0]
    st.divider()
    st.subheader("🖼️ Result")
    st.code(latest["final_prompt"], language=None)

    cols = st.columns(len(latest["images"]))
    for i, (col, img) in enumerate(zip(cols, latest["images"])):
        with col:
            st.image(img, use_container_width=True)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button(
                label="⬇️ Download",
                data=buf.getvalue(),
                file_name=f"ai_image_{latest['timestamp'].replace(':','-')}_{i+1}.png",
                mime="image/png",
                use_container_width=True,
                key=f"download_{i}",
            )

# ──────────────────────────────────────────────────────────────────────
# Prompt history / gallery (bonus)
# ──────────────────────────────────────────────────────────────────────
if len(st.session_state.history) > 1:
    st.divider()
    st.subheader("📚 Prompt History")

    for entry in st.session_state.history[1:]:
        with st.expander(f"🕐 {entry['timestamp']} — \"{entry['prompt']}\" ({entry['style']})"):
            st.code(entry["final_prompt"], language=None)
            hist_cols = st.columns(len(entry["images"]))
            for col, img in zip(hist_cols, entry["images"]):
                with col:
                    st.image(img, use_container_width=True)

if st.session_state.history:
    if st.button("🗑️ Clear history"):
        st.session_state.history = []
        st.rerun()
