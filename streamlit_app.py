import streamlit as st
import pyqrcode
import cv2
import numpy as np

# Function to generate QR code
def generate_qr_code(message):
    qr = pyqrcode.create(message)
    qr.png('qr_code.png', scale=6)

# Function to display QR code
def display_qr_code():
    qr_code_img = cv2.imread('qr_code.png')
    st.image(qr_code_img, width=200)

# Streamlit app
st.title("QR Code Communication System")

# Input message
message = st.text_input("Enter message:")

# Generate and display QR code
if st.button("Generate QR Code"):
    generate_qr_code(message)
    display_qr_code()

# Display scanned message (optional)
scanned_message = st.text_input("Scanned message (optional):")
if scanned_message:
    st.success("Received message: " + scanned_message)
