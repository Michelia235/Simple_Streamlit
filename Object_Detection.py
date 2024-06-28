import cv2
import numpy as np
import streamlit as st
from PIL import Image
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model')
PROTOTXT = os.path.join(MODEL_DIR, 'MobileNetSSD_deploy.prototxt.txt')
MODEL = os.path.join(MODEL_DIR, 'MobileNetSSD_deploy.caffemodel')

def load_model():
    net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
    return net

def process_image(image, net):
    blob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5
    )
    net.setInput(blob)
    detections = net.forward()
    return detections

def annotate_image(image, detections, confidence_threshold=0.5):
    (h, w) = image.shape[:2]
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > confidence_threshold:
            int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (start_x, start_y, end_x, end_y) = box.astype("int")
            cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (255, 0, 0), 2)  # Changed color to (255, 0, 0) for red
    return image

def main():
    st.title('Object Detection for Images')
    net = load_model()
    file = st.file_uploader('Upload Image', type=['jpg', 'png', 'jpeg'])
    
    if file is not None:
        uploaded_image = Image.open(file)
        st.image(uploaded_image, caption="Uploaded Image")
        image = np.array(uploaded_image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR
        detections = process_image(image, net)
        processed_image = annotate_image(image.copy(), detections)
        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)  # Convert back to RGB
        st.image(processed_image, caption="Processed Image")

if __name__ == '__main__':
    main()
