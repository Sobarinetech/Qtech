import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO
from datetime import datetime, timedelta

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
st.set_page_config(page_title="Ever AI", page_icon=":robot:", layout="centered")
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #00c6ff, #0072ff);
        color: white;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #00d1b2;
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00b59d;
    }
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid #00d1b2;
        color: white;
        padding: 10px;
        font-size: 16px;
        border-radius: 8px;
        width: 100%;
        max-width: 800px;
        height: 150px;
        box-sizing: border-box;
    }
    .stTextArea textarea:focus {
        outline: none;
        border-color: #00b59d;
    }
    .stMarkdown h3 {
        text-align: center;
        color: #f0f0f0;
        font-size: 28px;
        font-weight: bold;
    }
    .stMarkdown p {
        color: #f0f0f0;
        font-size: 18px;
        text-align: center;
        padding-bottom: 20px;
    }
    .stSpinner {
        color: #00d1b2;
    }
    .stImage img {
        border-radius: 15px;
    }
    .footer {
        text-align: center;
        color: #ffffff;
        padding: 15px;
        font-size: 14px;
    }
    .footer a {
        color: #00d1b2;
        text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

# Instructional text with animation
st.markdown("""
    <h3>🚀 Welcome to Ever AI!</h3>
    <p>Generate content with cutting-edge AI based on your prompt. You can generate up to 2 responses every 15 minutes.</p>
""", unsafe_allow_html=True)

# Hardcode a pre-prompt that instructs the model to limit response to 2500 characters
pre_prompt = "Generate the content in the input text area upto 2500 characters."

# Prompt input field where the user can enter their own prompt
user_prompt = st.text_area("Enter your prompt here:", "Best alternatives to javascript?", height=150)

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
            with st.spinner("💡 Generating your response... This might take a moment!"):
                response = model.generate_content(full_prompt)
                
                # Extract the response text
                response_text = response.text
                
                # Limit the response to 2500 characters
                response_text = response_text[:2500]
                
                # Remove any instances of '**' from the response text
                response_text = response_text.replace("**", "")
                
                # Display the response in Streamlit
                st.write("### Response:")
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
                st.image(img_bytes, caption="📱 Scan to View Response", use_container_width=True)
                
                # Convert response text to a downloadable file
                response_file = BytesIO()
                response_file.write(response_text.encode())
                response_file.seek(0)
                
                # Add download button for the generated content
                st.download_button(
                    label="💾 Download Response",
                    data=response_file,
                    file_name="generated_response.txt",
                    mime="text/plain"
                )
                
        except Exception as e:
            st.error(f"Error: {e}")

    # Triggering cool animations after the process finishes
    st.balloons()  # Trigger streamlit balloons after generation

# Footer with links
st.markdown("""
    <div class="footer">
        <p>Powered by Streamlit and Google Generative AI | <a href="https://github.com/yourusername/yourrepo" target="_blank">GitHub</a></p>
    </div>
""", unsafe_allow_html=True)
