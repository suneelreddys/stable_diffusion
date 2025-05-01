from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import torch
import numpy as np
import cv2
from diffusers import StableDiffusionControlNetImg2ImgPipeline, ControlNetModel
from PIL import Image
import io
import uuid
import os
from utility import style_presets

# Global variable for the pipeline
pipeline = None

# Create output directory
os.makedirs("outputs", exist_ok=True)

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load models on startup
    global pipeline
    
    # Load ControlNet models
    controlnet_canny = ControlNetModel.from_pretrained(
        "lllyasviel/control_v11p_sd15_canny",
        torch_dtype=torch.float16
    )
    
    controlnet_face = ControlNetModel.from_pretrained(
        "lllyasviel/control_v11p_sd15_openpose",
        torch_dtype=torch.float16
    )
    
    # Load pipeline with standard Stable Diffusion instead of RunwayML
    pipeline = StableDiffusionControlNetImg2ImgPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4",  # Standard Stable Diffusion model
        controlnet=[controlnet_canny, controlnet_face],
        torch_dtype=torch.float16,
        safety_checker=None
    )
    
    # Move to GPU and enable memory optimizations
    pipeline.enable_model_cpu_offload()
    
    yield
    
    # Clean up resources
    del pipeline

# Initialize FastAPI
app = FastAPI(lifespan=lifespan)

@app.post("/transform/")
async def transform_image(
    image: UploadFile = File(...),
    style: str = Form("Ghibli")
):
    """
    Transform an uploaded image using the selected style preset
    """
    # Get prompt and negative prompt for the style
    if style in style_presets:
        prompt = style_presets[style]["prompt"]
        negative_prompt = style_presets[style]["negative_prompt"]
    else:
        # Default prompts if style not found
        prompt = "Transform this image while maintaining its core composition and subject."
        negative_prompt = "blurry, low quality, distorted, poor composition"
    
    # Read the uploaded image
    image_data = await image.read()
    init_image = Image.open(io.BytesIO(image_data))
    
    # Create canny edge map
    init_image_np = np.array(init_image)
    canny_image = cv2.Canny(init_image_np, 100, 200)
    canny_image = canny_image[:, :, None]
    canny_image = np.concatenate([canny_image, canny_image, canny_image], axis=2)
    canny_image = Image.fromarray(canny_image)
    
    # Use the original image for face preservation
    face_image = init_image
    
    # Generate the transformed image
    result = pipeline(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=init_image,
        control_image=[canny_image, face_image],
        controlnet_conditioning_scale=[0.8, 0.6],  # Increased edge control for sharper lines
        guidance_scale=8.5,         # Slightly increased prompt adherence
        strength=0.4,               # Keep the same strength
        num_inference_steps=40,     # Quality
        generator=torch.Generator().manual_seed(42)  # Reproducibility
    ).images[0]
    
    # Save the result
    output_filename = f"outputs/{style}_{uuid.uuid4()}.png"
    result.save(output_filename)
    
    # Return the image file
    return FileResponse(output_filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)