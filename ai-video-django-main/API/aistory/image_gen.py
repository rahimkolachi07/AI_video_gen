import requests
import io
from PIL import Image


def query(payload,API_URL,headers):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

import time
def image_gen(loc,prompts,i):
    try:
        API_URL = "https://api-inference.huggingface.co/models/cagliostrolab/animagine-xl-3.0"
        headers = {"Authorization": "Bearer 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"}
        image_bytes = query({"inputs": f"{prompts}",},API_URL,headers)
        # Attempt to open the image
        image = Image.open(io.BytesIO(image_bytes))
        # Display or process the image as needed
        image.save(f"{loc}/image/{i}.png")
        print("part one")
    except:
        try:
            API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
            headers = {"Authorization": "Bearer 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"}
            image_bytes = query({"inputs": f"{prompts}",},API_URL,headers)
            # Attempt to open the image
            image = Image.open(io.BytesIO(image_bytes))
            # Display or process the image as needed
            image.save(f"{loc}/image/{i}.png")
            print("part two")
        except:

            API_URL = "https://api-inference.huggingface.co/models/sayakpaul/diffusion-sdxl-orpo"
            headers = {"Authorization": "Bearer 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"}
            image_bytes = query({"inputs": f"{prompts}",},API_URL,headers)
            # Attempt to open the image
            image = Image.open(io.BytesIO(image_bytes))
            # Display or process the image as needed
            image.save(f"{loc}/image/{i}.png")
            print("part third")
