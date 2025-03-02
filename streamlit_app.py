import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO
import time
from datetime import datetime, timedelta
import threading

# Configure the API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Constants for rate-limiting
MAX_GENERATIONS = 2  # Max number of generations per user
TIME_LIMIT = timedelta(minutes=15)  # Time window of 15 minutes

# Session state to track the user's generation history
if "last_generated" not in st.session_state:
    st.session_state.last_generated = []
    
# Helper function to track and enforce rate-limiting
def check_rate_limit():
    # Remove any old timestamps that are outside the 15-minute window
    now = datetime.now()
    st.session_state.last_generated = [
        timestamp for timestamp in st.session_state.last_generated if now - timestamp < TIME_LIMIT
    ]
    
    if len(st.session_state.last_generated) >= MAX_GENERATIONS:
        return False
    return True

# Streamlit App UI with enhanced features and animations
st.title("Ever AI")
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# Instructional text with animation
st.write("""
    <h3 style="color: #2d87f0;">Use generative AI to get responses based on your prompt!</h3>
    <p style="color: #555;">Enter your prompt below and click "Generate Response". You can only generate up to 2 responses every 15 minutes to avoid abuse.</p>
""", unsafe_allow_html=True)

# Hardcode a pre-prompt that instructs the model to limit response to 2500 characters
pre_prompt = "Generate the content in the input text area within 2500 characters."

# Prompt input field where the user can enter their own prompt
user_prompt = st.text_area("Enter your prompt:", "Best alternatives to javascript?")

# Combine the pre-prompt with the user input
full_prompt = pre_prompt + "\n" + user_prompt

# Rate limit check
if not check_rate_limit():
    st.error("You have reached the maximum limit of 2 responses in the past 15 minutes. Please try again later.")
else:
    # Button to generate response
    if st.button("Generate Response"):
        # Enforce rate-limiting by storing the current time of the generation
        st.session_state.last_generated.append(datetime.now())

        try:
            # Load and configure the model
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Generate response from the model with the combined prompt
            with st.spinner("Generating response... Please wait."):

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
    
    # Display some cool animations after the process finishes
    st.balloons()  # Trigger streamlit balloons after generation

    # Add a footer to the page
    st.markdown("""
        <footer style="text-align: center; color: #999;">
            <p>Powered by Streamlit and Google Generative AI | <a href="https://github.com/yourusername/yourrepo">GitHub</a></p>
        </footer>
    """, unsafe_allow_html=True)
