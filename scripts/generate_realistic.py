"""
Generate realistic images with Stable Diffusion!
"""

import os
import torch
from diffusers import StableDiffusionPipeline

print("="*60)
print("REALISTIC IMAGE GENERATOR")
print("="*60)

# Load realistic model (more photorealistic)
print("\nLoading Stable Diffusion model...")
print("(Using realistic model settings)")

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
    safety_checker=None,
    use_safetensors=True
)

pipe = pipe.to("cuda")

print("Model loaded!")
print()

# Generate realistic Asa
print("="*60)
print("GENERATING: REALISTIC ASA")
print("="*60)

realistic_prompt = "beautiful young woman, natural looking, soft natural lighting, gentle expression, warm smile, rosy cheeks, natural hair color, comfortable casual clothing, photorealistic, photography, professional portrait, shallow depth of field, 8k quality, detailed skin texture"

print(f"Prompt: {realistic_prompt}")

realistic_negative = "anime, cartoon, illustration, painting, drawing, artificial, plastic, oversaturated,过度美化, blurry, low quality, distorted features"

print("\nGenerating realistic image...")
realistic_image = pipe(
    realistic_prompt,
    negative_prompt=realistic_negative,
    num_inference_steps=50,
    guidance_scale=7.5,
    height=576,  # Slightly taller for portrait
    width=448
).images[0]

realistic_path = "C:/Users/bainz/clawd/asa_realistic.png"
realistic_image.save(realistic_path)
print(f"[OK] Realistic Asa saved: {realistic_path}")

# Generate realistic Asa with bunny ears
print()
print("="*60)
print("GENERATING: REALISTIC ASA WITH BUNNY EARS")
print("="*60)

bunny_realistic_prompt = "beautiful young woman with long fluffy white rabbit ears on head, natural looking, soft natural lighting, gentle expression, warm smile, rosy cheeks, comfortable casual clothing, photorealistic, photography, professional portrait, shallow depth of field, 8k quality"

print(f"Prompt: {bunny_realistic_prompt}")

bunny_negative = "anime, cartoon, illustration, painting, drawing, artificial, plastic, oversaturated, blurry, low quality"

print("\nGenerating...")
bunny_realistic_image = pipe(
    bunny_realistic_prompt,
    negative_prompt=bunny_negative,
    num_inference_steps=50,
    guidance_scale=7.5,
    height=576,
    width=448
).images[0]

bunny_realistic_path = "C:/Users/bainz/clawd/asa_realistic_bunny.png"
bunny_realistic_image.save(bunny_realistic_path)
print(f"[OK] Realistic Asa with bunny ears saved: {bunny_realistic_path}")

print()
print("="*60)
print("ALL REALISTIC IMAGES GENERATED!")
print("="*60)
print()
print(f"File 1: asa_realistic.png")
print(f"File 2: asa_realistic_bunny.png")
print()
print("Opening images...")
os.startfile(realistic_path)
os.startfile(bunny_realistic_path)
