import streamlit as st
from PIL import Image
import qrcode
from io import BytesIO
import zipfile
import cv2
import numpy as np

# Helper function to generate a QR code
def generate_qr(data, fill_color="black", back_color="white", box_size=10, border=4, error_correction=qrcode.constants.ERROR_CORRECT_M):
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

# Function to convert PIL image to byte stream
def pil_to_bytes(img):
    byte_arr = BytesIO()
    img.save(byte_arr, format="PNG")
    byte_arr.seek(0)
    return byte_arr

# Function to decode QR Code using OpenCV
def decode_qr(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    # Create a QRCodeDetector object
    detector = cv2.QRCodeDetector()
    
    # Detect and decode the QR code
    value, pts, qr_code = detector(gray)
    
    if value:
        return value
    return "No QR Code detected"

# Main page of the app
st.title("QR Code Utilities")
st.sidebar.title("QR Code Utilities")
app_mode = st.selectbox("Choose a tool", [
    "Generate QR Code", "Batch QR Generation", "Customize QR Code", "QR Code with Logo", "QR Code Decoder",
    "QR Code Styling", "QR Code Animation", "Add a Border", "Error Correction Level", "QR Code Info",
    "Contact (vCard) Generator", "WiFi QR Generator", "Location QR Generator", "Social Media Link QR",
    "Payment QR Generator", "QR Code Timer", "Date-based QR Codes", "Dynamic QR Codes", "Tracking QR Codes",
    "Short URL QR Generator", "QR Code for App Download", "QR Code for Calendar Events", "SMS QR Code Generator",
    "Email QR Code Generator", "Multi-Use QR Codes", "Encrypted QR Codes", "Geolocation-based QR Codes",
    "QR Code with Multiple Data Types", "Custom QR Code Templates"
])

# QR Code Generator with Multiple Types
if app_mode == "Generate QR Code":
    qr_type = st.selectbox("Select QR Code Type", ["Text/URL", "Contact (vCard)", "WiFi", "Calendar Event", "SMS", "Email", "Location", "Phone Number", "YouTube Link"])

    if qr_type == "Text/URL":
        data = st.text_input("Enter text or URL for QR Code")
    elif qr_type == "Contact (vCard)":
        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email")
        address = st.text_area("Address")
        data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL:{phone}\nEMAIL:{email}\nADR:{address}\nEND:VCARD"
    elif qr_type == "WiFi":
        ssid = st.text_input("SSID")
        password = st.text_input("Password", type="password")
        hidden = st.selectbox("Is Network Hidden?", ["No", "Yes"])
        hidden_val = "true" if hidden == "Yes" else "false"
        data = f"WIFI:S:{ssid};T:WPA;P:{password};H:{hidden_val};;"
    elif qr_type == "Calendar Event":
        event = st.text_input("Event Title")
        start_date = st.date_input("Start Date")
        start_time = st.time_input("Start Time")
        end_date = st.date_input("End Date")
        end_time = st.time_input("End Time")
        data = f"BEGIN:VEVENT\nSUMMARY:{event}\nDTSTART:{start_date}T{start_time}Z\nDTEND:{end_date}T{end_time}Z\nEND:VEVENT"
    elif qr_type == "SMS":
        phone = st.text_input("Phone Number")
        message = st.text_area("Message")
        data = f"SMSTO:{phone}:{message}"
    elif qr_type == "Email":
        email = st.text_input("Email Address")
        subject = st.text_input("Subject")
        body = st.text_area("Body")
        data = f"mailto:{email}?subject={subject}&body={body}"
    elif qr_type == "Location":
        latitude = st.text_input("Latitude")
        longitude = st.text_input("Longitude")
        data = f"geo:{latitude},{longitude}"
    elif qr_type == "Phone Number":
        data = st.text_input("Enter Phone Number")
    elif qr_type == "YouTube Link":
        video_id = st.text_input("Enter YouTube Video ID")
        data = f"https://www.youtube.com/watch?v={video_id}"

    if data:
        qr_img = generate_qr(data)
        st.image(qr_img, caption="Generated QR Code", use_column_width=True)

        # Convert to byte stream for download button
        buffer = pil_to_bytes(qr_img)
        st.download_button("Download QR Code as PNG", buffer, file_name="qr_code.png", mime="image/png")

# Batch QR Code Generation
elif app_mode == "Batch QR Generation":
    batch_data = st.text_area("Enter data, one item per line")
    if batch_data:
        data_list = batch_data.strip().split("\n")
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for i, item in enumerate(data_list):
                img = generate_qr(item)
                img_buffer = pil_to_bytes(img)
                zip_file.writestr(f"qr_code_{i+1}.png", img_buffer.read())

        st.download_button("Download ZIP file of QR Codes", zip_buffer.getvalue(), file_name="qr_codes.zip", mime="application/zip")

# Customize QR Code
elif app_mode == "Customize QR Code":
    data = st.text_input("Enter text or URL for QR Code")
    if data:
        fill_color = st.color_picker("Select fill color", "#000000")
        back_color = st.color_picker("Select background color", "#FFFFFF")
        error_correction = st.selectbox("Error Correction Level", ["L", "M", "Q", "H"])
        error_levels = {"L": qrcode.constants.ERROR_CORRECT_L, "M": qrcode.constants.ERROR_CORRECT_M,
                        "Q": qrcode.constants.ERROR_CORRECT_Q, "H": qrcode.constants.ERROR_CORRECT_H}
        qr_img = generate_qr(data, fill_color, back_color, error_correction=error_levels[error_correction])
        st.image(qr_img, caption="Customized QR Code", use_column_width=True)

        # Convert to byte stream for download button
        buffer = pil_to_bytes(qr_img)
        st.download_button("Download Customized QR Code", buffer, file_name="custom_qr_code.png", mime="image/png")

# QR Code with Logo
elif app_mode == "QR Code with Logo":
    data = st.text_input("Enter text or URL for QR Code")
    uploaded_logo = st.file_uploader("Upload a logo to embed in the QR code", type=["png", "jpg", "jpeg"])
    if data and uploaded_logo:
        qr_img = generate_qr(data)
        logo = Image.open(uploaded_logo).convert("RGBA")
        logo.thumbnail((qr_img.size[0] // 3, qr_img.size[1] // 3))
        pos = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)
        qr_img.paste(logo, pos, mask=logo)

        st.image(qr_img, caption="QR Code with Logo", use_column_width=True)

        # Convert to byte stream for download button
        buffer = pil_to_bytes(qr_img)
        st.download_button("Download QR Code with Logo", buffer, file_name="qr_code_with_logo.png", mime="image/png")

# QR Code Decoder
elif app_mode == "QR Code Decoder":
    st.title("QR Code Decoder")
    uploaded_qr = st.file_uploader("Upload a QR Code image", type=["png", "jpg", "jpeg"])
    if uploaded_qr:
        img = Image.open(uploaded_qr)
        decoded_info = decode_qr(img)
        st.write(f"Decoded Data: {decoded_info}")

# Additional Features - Explained:
# 1. **QR Code Styling**: Customize the QR code's appearance (colors, shapes, etc.)
# 2. **QR Code Animation**: Integrate animated QR codes (create sequence-based animations)
# 3. **Add a Border**: Add a border to the QR code (size, color, etc.)
# 4. **Error Correction Level**: Choose from
