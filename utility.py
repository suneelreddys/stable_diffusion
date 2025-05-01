# utility.py
# Dictionary containing style presets with concise prompts (within 77 token limit)

style_presets = {
    "Ghibli": {
        "prompt": "Studio Ghibli anime style, whimsical, vibrant colors, soft lighting, dreamlike atmosphere.",
        "negative_prompt": "photorealistic, harsh lighting, high contrast, CGI, 3D render, gritty, distorted."
    },
    
    "Photorealistic": {
        "prompt": "Photorealistic, professional photography, cinematic lighting, detailed textures, 8K resolution.",
        "negative_prompt": "cartoon, anime, sketch, painting style, low resolution, blurry, unnatural colors."
    },
    
    "Manga": {
        "prompt": "Japanese manga style, clean line art, black and white, dramatic shading, expressive features.",
        "negative_prompt": "photorealistic, watercolor, 3D render, western comic style, overly detailed background."
    }
}