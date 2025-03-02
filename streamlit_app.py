import streamlit as st
import io
import qrcode
from PIL import Image
import google.generativeai as genai

# Configure API keys securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# QR Code Generator Function
def generate_qr(data):
    qr = qrcode.QRCode(
        version=None,  # Automatically determine the smallest version suitable for the data
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
