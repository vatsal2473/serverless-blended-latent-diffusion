# Must use a Cuda version 11+
FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime

WORKDIR /

# Install git
RUN apt-get update && apt-get install -y git
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install gdown
RUN gdown 1wcOK4co3EnbFAL6UpX1SVChMBKAzkMOx -O models/ldm/tex2img-large/

# Install python packages
RUN pip3 install --upgrade pip
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip install -e git+https://github.com/openai/CLIP.git@main#egg=clip

# We add the banana boilerplate here
ADD server.py .
EXPOSE 8000

# Add your model weight files 
# (in this case we have a python script)
# ADD download.py .
# RUN python3 download.py

# Add your custom app code, init() and inference()
ADD app.py .

CMD python3 -u server.py