import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO

# Configure the API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.set_page_config(page_title="Ever AI", page_icon="🤖", layout="centered")

# Title and Description
st.title("🤖 Ever AI")
st.subheader("Use generative AI to get responses based on your prompt.")

# Explanation
st.write("""
    This app uses Google Generative AI to generate text-based responses based on the prompts you enter. 
    The output will be limited to 5000 characters, and you can also generate a QR code for easy sharing.
    Enter a prompt below and let the magic begin!
""")

# Initialize session state for the prompt if not already initialized
if "user_prompt" not in st.session_state:
    st.session_state.user_prompt = ""

# Hardcode a pre-prompt that instructs the model to limit response to 2500 characters
pre_prompt = "Generate the content in the input text area within 5000 characters."

# Prompt input field where the user can enter their own prompt
user_prompt = st.text_area(
    "Enter your prompt:",
    value=st.session_state.user_prompt,
    placeholder="e.g., Best alternatives to JavaScript?",
    max_chars=500,
    height=200
)

# Store the input into session state so that it persists between reruns
st.session_state.user_prompt = user_prompt

# Display real-time character count
st.markdown(f"**Character Count:** {len(user_prompt)} / 500 characters")

# Button to clear the input
if st.button("Clear Input"):
    st.session_state.user_prompt = ""  # Clear session state input
    st.experimental_rerun()  # This will refresh the app to reflect the cleared input

# Combine the pre-prompt with the user input
full_prompt = pre_prompt + "\n" + user_prompt

# Button to generate response
if st.button("Generate Response"):

    with st.spinner("Generating response... This might take a few seconds."):

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
            st.write("### Response:")
            st.markdown(f'<div style="white-space: pre-wrap;">{response_text}</div>', unsafe_allow_html=True)

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

            # Display the QR code
            st.image(img_bytes, caption="QR Code for the Response", use_container_width=True)

            # Option to download the QR code image
            qr_image_file = BytesIO()
            img.save(qr_image_file)
            qr_image_file.seek(0)

            st.download_button(
                label="Download QR Code",
                data=qr_image_file,
                file_name="qr_code.png",
                mime="image/png"
            )

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
