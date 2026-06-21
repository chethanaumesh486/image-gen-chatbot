"""
prompt_builder.py
------------------
Handles style-conditioned prompt construction.

Takes a raw user prompt + a selected style and returns the final
prompt string that gets sent to the image generation API, along
with an optional negative prompt suffix.
"""

# Each style maps to a suffix that gets appended to the user's prompt.
# This is what "conditions" the output toward a particular visual style.
STYLE_PROMPTS = {
    "Realistic":     "photorealistic, ultra detailed, 8k, professional photography, sharp focus",
    "Anime":         "anime style, detailed, vibrant colors, studio anime artwork, clean lineart",
    "Cyberpunk":     "cyberpunk style, neon lights, futuristic, dystopian, glowing signage, rain-slicked streets",
    "Watercolor":    "watercolor painting, soft brush strokes, pastel palette, artistic, paper texture",
    "3D Render":     "3D render, octane render, cinematic lighting, hyper-detailed, unreal engine 5",
    "Pixel Art":     "pixel art, 16-bit retro game style, crisp pixels, limited color palette",
    "Fantasy Art":   "fantasy concept art, epic, dramatic lighting, intricate detail, digital painting",
    "Minimalist":    "minimalist design, clean lines, simple shapes, flat colors, negative space",
    "Oil Painting":  "oil painting, classical art style, rich textures, visible brushstrokes, museum quality",
    "Sketch":        "pencil sketch, hand-drawn, black and white, detailed linework, cross-hatching",
}

STYLE_DESCRIPTIONS = {
    "Realistic":    "Lifelike, photographic detail",
    "Anime":        "Japanese animation style",
    "Cyberpunk":    "Neon-lit, futuristic, dystopian",
    "Watercolor":   "Soft, painterly, artistic",
    "3D Render":    "Polished, computer-generated look",
    "Pixel Art":    "Retro, 8-bit/16-bit game style",
    "Fantasy Art":  "Epic, mythical, concept-art style",
    "Minimalist":   "Clean, simple, flat design",
    "Oil Painting": "Classical, textured, fine art",
    "Sketch":       "Hand-drawn, pencil illustration",
}


def build_final_prompt(user_prompt: str, style: str) -> str:
    """
    Combines the user's raw prompt with the style-specific suffix.

    Example:
        user_prompt = "A cat wearing sunglasses"
        style = "Anime"
        -> "A cat wearing sunglasses, anime style, detailed, vibrant colors,
            studio anime artwork, clean lineart"
    """
    user_prompt = user_prompt.strip().rstrip(".")
    style_suffix = STYLE_PROMPTS.get(style, "")
    if not style_suffix:
        return user_prompt
    return f"{user_prompt}, {style_suffix}"


def get_style_list():
    """Returns the list of available style names, in display order."""
    return list(STYLE_PROMPTS.keys())


def get_style_description(style: str) -> str:
    """Returns a short human-readable description of a style."""
    return STYLE_DESCRIPTIONS.get(style, "")
