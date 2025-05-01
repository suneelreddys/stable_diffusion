from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import torch
import numpy as np
import cv2
from diffusers import AutoPipelineForImage2Image
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
    
    # Load Kandinsky 2.2 pipeline
    pipeline = AutoPipelineForImage2Image.from_pretrained(
        "kandinsky-community/kandinsky-2-2-decoder", 
        torch_dtype=torch.float16, 
        use_safetensors=True
    )
    
    # Move to GPU and enable memory optimizations
    pipeline.enable_model_cpu_offload()
    
    # Enable memory efficient attention if xFormers is installed
    try:
        pipeline.enable_xformers_memory_efficient_attention()
    except:
        print("xFormers not available, using standard attention")
    
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
    # Get prompt for the style
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
    
    # Create edge-enhanced version for sketch styles
    if style == "Sketch":
        # Pre-process the image to enhance edges for sketch style
        init_image_np = np.array(init_image)
        
        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(init_image_np, cv2.COLOR_RGB2GRAY)
        
        # Apply edge detection
        edges = cv2.Canny(gray, 100, 200)
        
        # Dilate edges to make them more prominent
        kernel = np.ones((2, 2), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        
        # Create a mask from edges
        edge_mask = edges.astype(np.float32) / 255.0
        
        # Enhance contrast for sketch effect
        alpha = 1.2  # Contrast control
        beta = 10    # Brightness control
        contrast_adjusted = cv2.convertScaleAbs(init_image_np, alpha=alpha, beta=beta)
        
        # Convert back to PIL
        init_image = Image.fromarray(contrast_adjusted)
    
    # Generate the transformed image using Kandinsky
    result = pipeline(
        prompt=prompt,
        image=init_image,
        negative_prompt=negative_prompt,
        guidance_scale=7.5,         # Control prompt adherence
        strength=0.7,               # Control how much to preserve original image
        num_inference_steps=50,     # Quality
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