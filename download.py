import os
import requests

def download_model():
    if os.path.exists("models/ldm/text2img-large/model.ckpt"):
        print("Model already downloaded")
    else:
        print("Downloading model...")
        os.makedirs(os.path.dirname('models/ldm/text2img-large/'), exist_ok=True)
        url = "https://ommer-lab.com/files/latent-diffusion/nitro/txt2img-f8-large/model.ckpt"
        r = requests.get(url, allow_redirects=True)
        open("models/ldm/text2img-large/model.ckpt", "wb").write(r.content)
        print("Model downloaded")

if __name__ == "__main__":
    download_model()