FROM python:3.8.6-buster

COPY api /api
COPY dancemachine_by_871 /dancemachine_by_871
COPY 90_pct_model.h5 /90_pct_model.h5
COPY docker_requirements.txt /docker_requirements.txt

RUN pip install -r docker_requirements.txt

#The Dockerfile is based on a python image and uses uvicorn in order to serve the API.
RUN pip install -U pip
RUN pip install fastapi uvicorn

#These commands install the cv2 dependencies that are normally present on the local machine, but might be missing in your Docker container causing the issue.
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
