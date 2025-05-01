# utility.py
# Dictionary containing style presets with both prompts and negative prompts

style_presets = {
    "Ghibli": {
        "prompt": "Generate a Ghibli-style image based on the provided input image. "
                 "Maintain the original content and composition of the input while transforming the visual style to reflect "
                 "the enchanting and whimsical characteristics of Studio Ghibli animation. "
                 "Focus on incorporating vibrant colors, soft edges, and a dreamlike atmosphere typical of Ghibli films. "
                 "Ensure that key elements of the input image are preserved and reimagined in the Ghibli aesthetic, "
                 "creating a harmonious blend of the original content and the new artistic style.",
        "negative_prompt": "photorealistic, harsh lighting, high contrast, sharp edges, CGI, 3D render, "
                          "gritty texture, dull colors, overly detailed, dark atmosphere, "
                          "distorted faces, anatomical errors, deformed features"
    },
    
    "Photorealistic": {
        "prompt": "Convert this image into a photorealistic version, enhancing lighting, shadows, "
                 "texture details, and overall realism while preserving the original composition and subject. "
                 "Professional photography, cinematic lighting, detailed textures, 8K resolution, "
                 "natural environment, ultra-realistic details, perfect exposure.",
        "negative_prompt": "cartoon, anime, sketch, painting style, low resolution, blurry, "
                          "distorted proportions, unnatural colors, simplified features, "
                          "flat shading, unrealistic lighting, excessive grain, poor composition"
    },
    
    "Manga": {
        "prompt": "Generate a manga-style image based on the provided input image. "
                 "Maintain all original content and elements from the input image while transforming it "
                 "into a unique manga aesthetic. Ensure that the characteristics typical of manga art, "
                 "such as line work, shading, and stylization, are applied without altering the original "
                 "content or composition. The output should be a high-quality manga image that reflects "
                 "the essence of the input image while showcasing the distinctive features of manga art.",
        "negative_prompt": "photorealistic, watercolor, oil painting, 3D render, western comic style, "
                          "blurry details, overly complex backgrounds, excessive grain, "
                          "western cartoon style, distorted faces, inconsistent line art"
    }
}