import torch
from torch import autocast
import base64
from io import BytesIO
from omegaconf import OmegaConf
from ldm.models.diffusion.ddpm import LatentDiffusion
from ldm.models.diffusion.ddim import DDIMSampler
from ldm.util import instantiate_from_config
from ldm.image_editor import ImageEditor
import requests
import shutil
import os
import tmpfiles

def get_image_from_url(url, save_path):

    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def load_model_from_config(config, ckpt, device, verbose=False) -> LatentDiffusion:
    print(f"Loading model from {ckpt}")
    pl_sd = torch.load(ckpt, map_location="cpu")
    sd = pl_sd["state_dict"]
    model = instantiate_from_config(config.model)
    m, u = model.load_state_dict(sd, strict=False)
    if len(m) > 0 and verbose:
        print("missing keys:")
        print(m)
    if len(u) > 0 and verbose:
        print("unexpected keys:")
        print(u)

    model.to(device)
    model.cond_stage_model.device = device
    model.cond_stage_model.tknz_fn.device = device
    model.eval()
    return model

# Init is ran on server startup
# Load your model to GPU as a global variable here using the variable name "model"
def init():
    global model, sampler
    config = OmegaConf.load("configs/latent-diffusion/txt2img-1p4B-eval.yaml")

    device = (
        torch.device(f"cuda:0")
        if torch.cuda.is_available()
        else torch.device("cpu")
    )

    model = load_model_from_config(
        config=config, ckpt="models/ldm/text2img-large/model.ckpt", device=device
    )
    sampler = DDIMSampler(model)

# Inference is ran for every server call
# Reference your preloaded global model variable here.
def inference(model_inputs:dict) -> dict:
    global model, sampler   

    # Parse out your arguments
    prompt = model_inputs.get('prompt', None)
    # height = model_inputs.get('height', 512)
    # width = model_inputs.get('width', 512)
    input_image = model_inputs.get('input_image', None)
    mask_image = model_inputs.get('mask_image', None)

    get_image_from_url(input_image, "inputs/img.png")
    get_image_from_url(mask_image, "inputs/mask.png")
    
    
    if prompt == None:
        return {'message': "No prompt provided"}
    
    editor = ImageEditor()
    editor.edit_image(prompt, model=model, sampler=sampler)

    res = tmpfiles.upload_data()

    return res