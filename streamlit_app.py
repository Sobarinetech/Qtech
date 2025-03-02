import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO

# Configure the API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("Ever AI")
st.write("Use generative AI to get responses based on your prompt.")

# Prompt input field
prompt = st.text_input("Enter your prompt:", "Best alternatives to javascript?")

# Button to generate response
if st.button("Generate Response"):
    try:
        # Load and configure the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate response from the model
        response = model.generate_content(prompt)
        
        # Display response in Streamlit
        st.write("Response:")
        st.write(response.text)
        
        # Generate QR code for the response text
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(response.text)
        qr.make(fit=True)
        
        # Convert QR code to image
        img = qr.make_image(fill='black', back_color='white')
        
        # Display the QR code
        st.image(img, caption="QR Code for the Response", use_column_width=True)
        
        # Convert response text to a downloadable file
        response_text = response.text
        response_file = BytesIO()
        response_file.write(response_text.encode())
        response_file.seek(0)
        
        # Add download button for the generated content
        st.download_button(
            label="Download Response",
            data=response_file,
            file_name="generated_response.txt",
            mime="text/plain"
        )
        
    except Exception as e:
        st.error(f"Error: {e}")
