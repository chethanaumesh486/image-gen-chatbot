"""
random_prompts.py
------------------
Bonus feature: generates a random creative prompt idea
when the user clicks "🎲 Surprise Me".
"""

import random

SUBJECTS = [
    "a futuristic Indian city at night",
    "a dragon sleeping on a pile of gold",
    "an astronaut riding a horse on Mars",
    "a cozy cabin in a snowy forest",
    "a robot tending to a flower garden",
    "a floating island with waterfalls",
    "a cat wearing sunglasses and a leather jacket",
    "an underwater city made of coral",
    "a steampunk airship over Victorian London",
    "a samurai standing in a bamboo forest at sunset",
    "a tiny mouse in a tiny medieval castle",
    "a neon-lit ramen shop in the rain",
    "an ancient library hidden inside a tree",
    "a fox spirit walking through a glowing forest",
    "a mountain village covered in cherry blossoms",
    "a spaceship docking at a desert space station",
    "a wizard's tower surrounded by lightning",
    "a vintage car driving through a desert at sunset",
    "a city built on the back of a giant turtle",
    "an owl wearing tiny round glasses, reading a book",
]

MODIFIERS = [
    "at golden hour",
    "during a thunderstorm",
    "covered in fog",
    "under a starry sky",
    "in the style of a fairytale",
    "with dramatic lighting",
    "",  # sometimes no extra modifier
]


def get_random_prompt() -> str:
    """Returns a randomly assembled creative prompt string."""
    subject = random.choice(SUBJECTS)
    modifier = random.choice(MODIFIERS)
    prompt = f"{subject} {modifier}".strip()
    # Capitalize first letter
    return prompt[0].upper() + prompt[1:]
