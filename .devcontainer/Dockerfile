FROM python:3.12.1-slim-bullseye
USER root

RUN apt-get update && \
    apt-get -y install --reinstall ca-certificates && \
    apt-get -y install software-properties-common && \
    pip install --upgrade pip

# Install Basic Packages
RUN pip install ipykernel jupyter numpy opencv-pythonimport numpy as np
import cv2

print("NumPy version:", np.__version__)
print("OpenCV version:", cv2.__version__)