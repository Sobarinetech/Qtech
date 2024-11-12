import streamlit as st
import io
import qrcode
from PIL import Image, ImageDraw, ImageOps
import google.generativeai as genai
import random

# Configure API keys securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# QR Code Generator Function
def generate_qr(data, error_correction, box_size, border, fill_color, back_color, logo=None, rounded=False, shadow=False, rotate_angle=0, background_img=None, custom_icon=None):
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    if logo:
        logo_img = Image.open(logo)
        pos = ((img.size[0] - logo_img.size[0]) // 2, (img.size[1] - logo_img.size[1]) // 2)
        img.paste(logo_img, pos)

    if rounded:
        img = ImageOps.expand(img, border=10, fill=fill_color)
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((10, 10, img.size[0] - 10, img.size[1] - 10), fill=255)
        img.putalpha(mask)

    if shadow:
        img = ImageOps.expand(img, border=5, fill=back_color)

    if rotate_angle:
        img = img.rotate(rotate_angle, expand=True)

    if background_img:
        background = Image.open(background_img)
        background.paste(img, ((background.size[0] - img.size[0]) // 2, (background.size[1] - img.size[1]) // 2))
        img = background

    if custom_icon:
        icon_img = Image.open(custom_icon)
        img.paste(icon_img, ((img.size[0] - icon_img.size[0]) // 2, (img.size[1] - icon_img.size[1]) // 2))

    return img

# Streamlit App UI for Generative AI with QR Code
st.title("Advanced QR Code Generator with Generative AI")
st.write("Use Google Generative AI to get responses and generate customized QR codes based on your prompt.")

# Generative AI Prompt input field
prompt = st.text_input("Enter your prompt for AI response:", "most powerful free TTS?")

# Button to generate AI response
if st.button("Generate AI Response"):
    try:
        # Load and configure the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate response from the model
        response = model.generate_content(prompt)
        
        # Display response in Streamlit
        st.write("AI Response:")
        st.write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")

# QR Code Generation UI
st.header("QR Code Generator")

option = st.selectbox(
    "Select the type of QR code you want to create:",
    ("URL", "Contact Information (vCard)", "Email", "Geo Location", "Event (vCalendar)", "Text", "Wi-Fi", "SMS", "Payment Link", "3D Effect", "Dynamic Content")
)

# Input fields based on selected QR code type
if option == "URL":
    data = st.text_input("Enter the URL:")
elif option == "Contact Information (vCard)":
    name = st.text_input("Enter your name:")
    email = st.text_input("Enter your email:")
    phone = st.text_input("Enter your phone number:")
    address = st.text_input("Enter your address:")
    company = st.text_input("Enter your company name:")
    data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nEMAIL:{email}\nTEL:{phone}\nADR:{address}\nORG:{company}\nEND:VCARD"
elif option == "Email":
    email = st.text_input("Enter the email address:")
    subject = st.text_input("Enter the subject:")
    body = st.text_area("Enter the email body:")
    data = f"mailto:{email}?subject={subject}&body={body}"
elif option == "Geo Location":
    latitude = st.number_input("Enter Latitude:")
    longitude = st.number_input("Enter Longitude:")
    data = f"geo:{latitude},{longitude}"
elif option == "Event (vCalendar)":
    event_name = st.text_input("Enter the event name:")
    start_date = st.date_input("Enter the start date:")
    end_date = st.date_input("Enter the end date:")
    location = st.text_input("Enter event location:")
    data = f"BEGIN:VEVENT\nSUMMARY:{event_name}\nDTSTART:{start_date}\nDTEND:{end_date}\nLOCATION:{location}\nEND:VEVENT"
elif option == "Text":
    data = st.text_area("Enter the text data:")
elif option == "Wi-Fi":
    ssid = st.text_input("Enter Wi-Fi SSID:")
    password = st.text_input("Enter Wi-Fi Password:")
    encryption = st.selectbox("Select Encryption Type:", ["WPA", "WEP", "None"])
    data = f"WIFI:S:{ssid};T:{encryption};P:{password};;"
elif option == "SMS":
    phone = st.text_input("Enter the phone number:")
    message = st.text_input("Enter your message:")
    data = f"SMSTO:{phone}:{message}"
elif option == "Payment Link":
    payment_url = st.text_input("Enter your payment link:")
    data = payment_url
elif option == "3D Effect":
    data = st.text_input("Enter the data for 3D QR code:")
elif option == "Dynamic Content":
    data = f"https://api.example.com/qrdata/{random.randint(1000, 9999)}"

# Customization options
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
logo = st.file_uploader("Upload Logo (optional):", type=["png", "jpg", "jpeg"])
rounded = st.checkbox("Rounded QR Code Blocks")
shadow = st.checkbox("Apply Shadow Effect")
rotate_angle = st.slider("Rotate QR Code (degrees):", 0, 360, 0)
background_img = st.file_uploader("Upload Background Image (optional):", type=["png", "jpg", "jpeg"])
custom_icon = st.file_uploader("Upload Custom Icon (optional):", type=["png", "jpg", "jpeg"])

# Generate QR Code button
if st.button("Generate QR Code"):
    if data:
        img = generate_qr(data, error_correction, box_size, border, fill_color, back_color, logo, rounded, shadow, rotate_angle, background_img, custom_icon)
        
        if img:
            # Display the generated QR code
            st.image(img, caption="Your QR Code", use_column_width=True)

            # Convert image to byte stream for download
            img_buffer = io.BytesIO()
            img.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            # Provide the option to download the QR code image
            st.download_button(
                label="Download QR Code",
                data=img_buffer,
                file_name="qr_code.png",
                mime="image/png",
            )
        else:
            st.error("QR Code generation failed.")
    else:
        st.error("Please enter data for QR code generation.")
