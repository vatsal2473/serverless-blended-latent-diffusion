# This file is used to verify your http server acts as expected
# Run it with `python3 test.py``

import requests
import base64
from io import BytesIO
from PIL import Image

model_inputs = {'prompt': 'realistic field of grass', 
                'input_image': 'https://tmpfiles.org/dl/474606/img.png', 
                'mask_image': 'https://tmpfiles.org/dl/474608/mask.png'}

res = requests.post('https://felvintestapi.pagekite.me/', json = model_inputs)

print(res.json())