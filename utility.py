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
        "prompt": "Generate a manga-style image based on the provided input image.Maintain all original content and elements from the input image while transforming it into a unique manga aesthetic.Ensure that the characteristics typical of manga art, such as line work, shading, and stylization, are applied without altering the original content or composition.The output should be a high-quality manga image that reflects the essence of the input image while showcasing the distinctive features of manga art.",
        "negative_prompt": "photorealistic, watercolor, 3D render, western comic style, overly detailed background."
    },
    "Sketch": {
    "prompt": "Pure black and white pencil sketch, strong distinct line art, heavy contrast, detailed crosshatching, sharp edges.",
    "negative_prompt": "color, sepia, soft edges, blurry lines, watercolor, gradient shading, photorealistic, subtle, painterly."
}

}