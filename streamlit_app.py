import streamlit as st
import google.generativeai as genai
import qrcode
from PIL import Image, ImageDraw, ImageOps
import io
import random
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import sentencepiece as sp

# Configure API keys securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI for Generative AI with QR Code
st.title("AI-Powered QR Code Generator")
st.write("Use Google Generative AI to generate customized QR codes.")

# AI Model for QR Code Description
def generate_qr_description(prompt):
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    output = model.generate(input_ids, max_length=50)
    description = tokenizer.decode(output[0], skip_special_tokens=True)
    return description

# QR Code Generator Options
st.header("QR Code Generator")

# QR Code Type Selection
option = st.selectbox(
    "Select QR code type:",
    ("URL", "Contact", "Email", "Geo Location", "Event", "Text", "Wi-Fi", "SMS", "Payment Link")
)

# Collecting data based on selected QR code type
if option == "URL":
    data = st.text_input("Enter URL:")
elif option == "Contact":
    name = st.text_input("Enter name:")
    email = st.text_input("Enter email:")
    phone = st.text_input("Enter phone number:")
    data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nEMAIL:{email}\nTEL:{phone}\nEND:VCARD"
elif option == "Email":
    email = st.text_input("Enter email address:")
    subject = st.text_input("Enter subject:")
    body = st.text_area("Enter email body:")
    data = f"mailto:{email}?subject={subject}&body={body}"
elif option == "Geo Location":
    latitude = st.number_input("Enter Latitude:")
    longitude = st.number_input("Enter Longitude:")
    data = f"geo:{latitude},{longitude}"
elif option == "Event":
    event_name = st.text_input("Enter event name:")
    start_date = st.date_input("Enter start date:")
    end_date = st.date_input("Enter end date:")
    location = st.text_input("Enter event location:")
    data = f"BEGIN:VEVENT\nSUMMARY:{event_name}\nDTSTART:{start_date}\nDTEND:{end_date}\nLOCATION:{location}\nEND:VEVENT"
elif option == "Text":
    data = st.text_area("Enter text data:")
elif option == "Wi-Fi":
    ssid = st.text_input("Enter Wi-Fi SSID:")
    password = st.text_input("Enter Wi-Fi Password:")
    encryption = st.selectbox("Select Encryption Type:", ["WPA", "WEP", "None"])
    data = f"WIFI:S:{ssid};T:{encryption};P:{password};;"
elif option == "SMS":
    phone = st.text_input("Enter phone number:")
    message = st.text_input("Enter message:")
    data = f"SMSTO:{phone}:{message}"
elif option == "Payment Link":
    payment_url = st.text_input("Enter payment link:")
    data = payment_url

# Additional customization options
error_correction = st.selectbox("Select Error Correction Level:", [
    qrcode.constants.ERROR_CORRECT_L,
    qrcode.constants.ERROR_CORRECT_M,
    qrcode.constants.ERROR_CORRECT_Q,
    qrcode.constants.ERROR_CORRECT_H,
])
box_size = st.slider("Select QR Code Size (box size):", 1, 10, 5)
border = st.slider("Select Border Size:", 1, 10, 4)
fill_color = st.color_picker("Select QR Code Color:", "#000000")
back_color = st.color_picker("Select Background Color:", "#FFFFFF")

def generate_qr(data, error_correction, box_size, border, fill_color, back_color):
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    return img

# Generate QR Code button
if st.button("Generate QR Code"):
    if data:
        description = generate_qr_description(option)
        st.write("Generated QR Code Description:")
        st.write(description)
        
        img = generate_qr(data, error_correction, box_size, border, fill_color, back_color)

        # Show the generated QR Code
        st.image(img, caption="Your QR Code")

        # Allow download
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        st.download_button(
            label="Download QR Code",
            data=img_buffer,
            file_name="qr_code.png",
            mime="image/png",
        )
