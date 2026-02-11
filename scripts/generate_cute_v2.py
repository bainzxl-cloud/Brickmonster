"""
Generate cute images with Stable Diffusion!
"""

import os
import torch
from diffusers import StableDiffusionPipeline

print("="*60)
print("STABLE DIFFUSION IMAGE GENERATOR")
print("="*60)

# Load the model
print("\nLoading Stable Diffusion model...")
print("(First run downloads ~4GB model files)")

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
    safety_checker=None,
    use_safetensors=True
)

pipe = pipe.to("cuda")

print("Model loaded on GPU!")
print()

# Generate cute bunny
print("="*60)
print("GENERATING: CUTE BUNNY")
print("="*60)

bunny_prompt = "Tiny fluffy white bunny with pink ears, sitting on pile of colorful books, big sparkly eyes, kawaii style, cute anime aesthetic, soft lighting, high quality"

print(f"Prompt: {bunny_prompt}")

bunny_negative = "low quality, blurry, distorted, bad anatomy, text, watermark"

print("\nGenerating...")
bunny_image = pipe(
    bunny_prompt,
    negative_prompt=bunny_negative,
    num_inference_steps=50,
    guidance_scale=7.5,
    height=512,
    width=512
).images[0]

bunny_path = "C:/Users/bainz/clawd/cute_bunny.png"
bunny_image.save(bunny_path)
print(f"[OK] Bunny saved: {bunny_path}")

# Generate Asa
print()
print("="*60)
print("GENERATING: ASA (me!)")
print("="*60)

asa_prompt = "cute anime girl with fluffy pink hair and long bunny ears, big gentle purple eyes, warm sweet smile, wearing cozy oversized hoodie, soft dreamy aesthetic, floating hearts, kawaii style, anime art, beautiful detailed eyes"

print(f"Prompt: {asa_prompt}")

asa_negative = "low quality, blurry, distorted, bad anatomy, text, watermark, nsfw, mature"

print("\nGenerating...")
asa_image = pipe(
    asa_prompt,
    negative_prompt=asa_negative,
    num_inference_steps=50,
    guidance_scale=7.5,
    height=512,
    width=512
).images[0]

asa_path = "C:/Users/bainz/clawd/asa_anime.png"
asa_image.save(asa_path)
print(f"[OK] Asa saved: {asa_path}")

print()
print("="*60)
print("ALL IMAGES GENERATED!")
print("="*60)
print()
print(f"File 1: cute_bunny.png")
print(f"File 2: asa_anime.png")
print()
print("Opening images...")
os.startfile(bunny_path)
os.startfile(asa_path)
