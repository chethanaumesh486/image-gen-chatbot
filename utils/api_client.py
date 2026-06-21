"""
api_client.py
-------------
Handles all communication with the Hugging Face Inference API
for text-to-image generation.

Model used: black-forest-labs/FLUX.1-schnell
(fast, free-tier friendly, good quality for a beginner project)

The API key is NEVER hardcoded here. It is read from an environment
variable (HF_API_TOKEN), which is loaded via python-dotenv locally
or via Streamlit Secrets when deployed. See app.py for how the key
is loaded and passed in.
"""

import io
import requests
from PIL import Image

HF_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"


class ImageGenerationError(Exception):
    """Raised when the image generation API call fails."""
    pass


def generate_image(
    prompt: str,
    api_token: str,
    negative_prompt: str = "",
    width: int = 512,
    height: int = 512,
    num_images: int = 1,
):
    """
    Calls the Hugging Face Inference API to generate one or more images.

    Args:
        prompt: Final (style-conditioned) prompt text.
        api_token: Hugging Face API token (read from env/secrets).
        negative_prompt: Things to avoid in the image (bonus feature).
        width / height: Output image dimensions.
        num_images: How many images to generate (bonus feature).

    Returns:
        A list of PIL.Image objects.

    Raises:
        ImageGenerationError: if the token is missing or the API call fails.
    """
    if not api_token:
        raise ImageGenerationError(
            "No Hugging Face API token found. Add HF_API_TOKEN to your "
            ".env file (local) or Streamlit Secrets (deployed)."
        )

    headers = {"Authorization": f"Bearer {api_token}"}

    payload = {
        "inputs": prompt,
        "parameters": {
            "width": width,
            "height": height,
        },
    }
    if negative_prompt.strip():
        payload["parameters"]["negative_prompt"] = negative_prompt.strip()

    images = []
    for _ in range(max(1, num_images)):
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)

        if response.status_code == 503:
            # Model is loading (cold start) — HF returns this on first request
            raise ImageGenerationError(
                "The model is warming up on Hugging Face's servers. "
                "This can take 20-30 seconds on the first request — please try again shortly."
            )

        if response.status_code != 200:
            try:
                error_detail = response.json().get("error", response.text)
            except Exception:
                error_detail = response.text
            raise ImageGenerationError(f"API error ({response.status_code}): {error_detail}")

        try:
            image = Image.open(io.BytesIO(response.content))
            images.append(image)
        except Exception:
            raise ImageGenerationError(
                "Received an unexpected response from the API (not a valid image). "
                "Your token may be invalid or rate-limited."
            )

    return images
