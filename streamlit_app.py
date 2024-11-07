import streamlit as st
from PIL import Image
import qrcode
from io import BytesIO
import csv
import zipfile
from pyzbar.pyzbar import decode
import base64
from datetime import datetime

# Helper function to generate QR code
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

# Sidebar for app navigation
st.sidebar.title("QR Code Utilities")
app_mode = st.sidebar.selectbox("Choose a tool", [
    "Generate QR Code", "Decode QR Code", "Batch QR Generation", "Customize QR Code", "QR Code with Logo"
])

# QR Code Generator with Multiple Types
if app_mode == "Generate QR Code":
    st.title("QR Code Generator")
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

        # Download QR code options
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        st.download_button("Download QR Code as PNG", buffer.getvalue(), file_name="qr_code.png", mime="image/png")
        svg_buffer = BytesIO()
        qr_img.save(svg_buffer, format="SVG")
        st.download_button("Download QR Code as SVG", svg_buffer.getvalue(), file_name="qr_code.svg", mime="image/svg+xml")

# QR Code Decoder
elif app_mode == "Decode QR Code":
    st.title("QR Code Decoder")
    uploaded_file = st.file_uploader("Upload a QR Code image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded QR Code", use_column_width=True)

        decoded_info = decode(img)
        if decoded_info:
            st.subheader("Decoded Information")
            for obj in decoded_info:
                st.write(obj.data.decode("utf-8"))
        else:
            st.error("No QR code found in the uploaded image.")

# Batch QR Code Generation
elif app_mode == "Batch QR Generation":
    st.title("Batch QR Code Generator")
    st.write("Upload a CSV file with a column of data to generate multiple QR codes.")
    uploaded_csv = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_csv:
        csv_data = uploaded_csv.getvalue().decode("utf-8")
        reader = csv.reader(csv_data.splitlines())
        data_list = list(reader)

        if st.button("Generate Batch QR Codes"):
            with st.spinner("Generating QR codes..."):
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                    for i, row in enumerate(data_list):
                        if row:  # Non-empty row
                            img = generate_qr(row[0])
                            img_buffer = BytesIO()
                            img.save(img_buffer, format="PNG")
                            zip_file.writestr(f"qr_code_{i+1}.png", img_buffer.getvalue())
                
                st.success("Batch QR code generation completed!")
                st.download_button("Download ZIP file", zip_buffer.getvalue(), file_name="qr_codes.zip", mime="application/zip")

# QR Code Customization
elif app_mode == "Customize QR Code":
    st.title("Customized QR Code Generator")
    data = st.text_input("Enter text or URL for QR Code")
    if data:
        fill_color = st.color_picker("Select fill color", "#000000")
        back_color = st.color_picker("Select background color", "#FFFFFF")
        error_correction = st.selectbox("Error Correction Level", ["L", "M", "Q", "H"])
        error_levels = {"L": qrcode.constants.ERROR_CORRECT_L, "M": qrcode.constants.ERROR_CORRECT_M,
                        "Q": qrcode.constants.ERROR_CORRECT_Q, "H": qrcode.constants.ERROR_CORRECT_H}
        qr_img = generate_qr(data, fill_color, back_color, error_correction=error_levels[error_correction])
        st.image(qr_img, caption="Customized QR Code", use_column_width=True)

        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        st.download_button("Download Customized QR Code", buffer.getvalue(), file_name="custom_qr_code.png", mime="image/png")

# QR Code with Logo
elif app_mode == "QR Code with Logo":
    st.title("QR Code with Embedded Logo")
    data = st.text_input("Enter text or URL for QR Code")
    uploaded_logo = st.file_uploader("Upload a logo to embed in the QR code", type=["png", "jpg", "jpeg"])
    if data and uploaded_logo:
        qr_img = generate_qr(data)
        logo = Image.open(uploaded_logo).convert("RGBA")
        logo.thumbnail((qr_img.size[0] // 3, qr_img.size[1] // 3))
        pos = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)
        qr_img.paste(logo, pos, mask=logo)

        st.image(qr_img, caption="QR Code with Logo", use_column_width=True)

        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        st.download_button("Download QR Code with Logo", buffer.getvalue(), file_name="qr_code_with_logo.png", mime="image/png")
