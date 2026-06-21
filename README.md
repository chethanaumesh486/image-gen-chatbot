#  AI Image Generation Chatbot

A Streamlit web app that turns text prompts into AI-generated images, with style selection, prompt history, and several creative extras — built with a clean, modular file structure.

---

## What this project does

Type a description, pick a visual style (Anime, Cyberpunk, Watercolor, etc.), and click **Generate** — the app builds a style-conditioned prompt and sends it to the **Hugging Face Inference API** (using the `FLUX.1-schnell` model) to produce an AI image, displayed right in the browser.


### Core features
- Text prompt input
- 10 style options (radio buttons): Realistic, Anime, Cyberpunk, Watercolor, 3D Render, Pixel Art, Fantasy Art, Minimalist, Oil Painting, Sketch
- Generate button with loading spinner
- Generated image displayed inline
- Prompt history (expandable gallery of past generations)

### Bonus features included
-  **Prompt history / gallery view** — every past generation is saved in an expandable list with its image and final prompt
- ⬇ **Download image button** — save any generated image as a PNG
-  **Image size selector** — 512×512 / 768×768 / 1024×1024
-  **Negative prompt input** — tell the model what to avoid
-  **Multiple image generation** — generate 1–4 variations at once
-  **Random prompt generator** — "Surprise Me" button for instant inspiration
-  **Dark/light theme toggle** — switch in the sidebar

---

## Project structure

```
image-gen-chatbot/
├── app.py                      ← Streamlit UI (this is the only file you run)
├── utils/
│   ├── __init__.py
│   ├── api_client.py           ← Hugging Face API call logic
│   ├── prompt_builder.py       ← Style-conditioning logic (style → prompt suffix)
│   └── random_prompts.py       ← Random prompt generator (bonus feature)
├── .env                        ← local API key
├── .gitignore                 
├── requirements.txt
└── README.md
```

UI logic, API logic, and prompt logic are kept in separate files on purpose, this makes the codebase easy to read, test, and extend
