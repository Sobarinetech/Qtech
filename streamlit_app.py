import streamlit as st
import io
import qrcode
from PIL import Image
import google.generativeai as genai

# Configure API keys securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Function to dynamically calculate QR code version based on data length
def calculate_qr_version(data):
    # Length-based version calculation to avoid errors, ensuring it falls within 1 to 40
    data_length = len(data)
    
    # Adjust QR code version based on data length, ensuring the version stays within bounds
    if data_length < 100:
        return 1
    elif data_length < 200:
        return 2
    elif data_length < 300:
        return 3
    elif data_length < 400:
        return 4
    elif data_length < 500:
        return 5
    elif data_length < 600:
        return 6
    elif data_length < 700:
        return 7
    elif data_length < 800:
        return 8
    elif data_length < 900:
        return 9
    elif data_length < 1000:
        return 10
    elif data_length < 1100:
        return 11
    elif data_length < 1200:
        return 12
    elif data_length < 1300:
        return 13
    elif data_length < 1400:
        return 14
    elif data_length < 1500:
        return 15
    elif data_length < 1600:
        return 16
    elif data_length < 1700:
        return 17
    elif data_length < 1800:
        return 18
    elif data_length < 1900:
        return 19
    elif data_length < 2000:
        return 20
    elif data_length < 2100:
        return 21
    elif data_length < 2200:
        return 22
    elif data_length < 2300:
        return 23
    elif data_length < 2400:
        return 24
    elif data_length < 2500:
        return 25
    elif data_length < 2600:
        return 26
    elif data_length < 2700:
        return 27
    elif data_length < 2800:
        return 28
    elif data_length < 2900:
        return 29
    elif data_length < 3000:
        return 30
    elif data_length < 3100:
        return 31
    elif data_length < 3200:
        return 32
    elif data_length < 3300:
        return 33
    elif data_length < 3400:
        return 34
    elif data_length < 3500:
        return 35
    elif data_length < 3600:
        return 36
    elif data_length < 3700:
        return 37
    elif data_length < 3800:
        return 38
    elif data_length < 3900:
        return 39
    else:
        return 40  # Return the highest valid version (40)

# QR Code Generator Function
def generate_qr(data):
    # Dynamically adjust version based on data size
    version = calculate_qr_version(data)
    
    qr = qrcode.QRCode(
        version=version,  # Set the version based on data length
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# Streamlit App UI for Generative AI with QR Code
st.title("Advanced QR Code Generator with Generative AI")
st.write("Use AI to get responses and generate customized QR codes based on your prompt.")

# Generative AI Prompt input field
prompt = st.text_input("Enter your prompt for AI response:", "best alternatives to Power BI?")

# Button to generate AI response and QR code
if st.button("Generate AI Response and QR Code"):
    try:
        # Load and configure the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate response from the model
        response = model.generate_content(prompt)
        
        # Display AI Response
        st.write("AI Response:")
        st.write(response.text)
        
        # Generate QR Code for the response
        data = response.text  # Content generated by AI will be the QR code data
        if data:
            # Generate QR Code
            img = generate_qr(data)
            
            if img:
                # Display the generated QR code
                img_buffer = io.BytesIO()
                img.save(img_buffer, format="PNG")
                img_bytes = img_buffer.getvalue()
                st.image(img_bytes, caption="Your QR Code", use_column_width=True)

                # Provide the option to download the QR code image
                st.download_button(
                    label="Download QR Code",
                    data=img_bytes,
                    file_name="qr_code.png",
                    mime="image/png",
                )
            else:
                st.error("QR Code generation failed.")
        else:
            st.error("No AI response to generate QR code.")
    except Exception as e:
        st.error(f"Error: {e}")
