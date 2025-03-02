import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO

# Configure the API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("Ever AI")
st.write("Use generative AI to get responses based on your prompt.")

# Hardcode a pre-prompt that instructs the model to limit response to 2500 characters
pre_prompt = "Generate the content in the input text area within 2500 characters."

# Prompt input field where the user can enter their own prompt
user_prompt = st.text_area("Enter your prompt:", "Best alternatives to javascript?")

# Combine the pre-prompt with the user input
full_prompt = pre_prompt + "\n" + user_prompt

# Button to generate response
if st.button("Generate Response"):
    try:
        # Load and configure the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate response from the model with the combined prompt
        response = model.generate_content(full_prompt)
        
        # Extract the response text
        response_text = response.text
        
        # Limit the response to 2500 characters
        response_text = response_text[:2500]
        
        # Remove any instances of '**' from the response text
        response_text = response_text.replace("**", "")
        
        # Display the response in Streamlit
        st.write("Response:")
        st.write(response_text)
        
        # Generate QR code for the response text
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(response_text)
        qr.make(fit=True)
        
        # Convert QR code to image (PIL image)
        img = qr.make_image(fill='black', back_color='white')
        
        # Convert PIL image to BytesIO for Streamlit to render
        img_bytes = BytesIO()
        img.save(img_bytes)
        img_bytes.seek(0)
        
        # Display the QR code with the new parameter
        st.image(img_bytes, caption="QR Code for the Response", use_container_width=True)
        
        # Convert response text to a downloadable file
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
