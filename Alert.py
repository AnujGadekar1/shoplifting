import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import cv2

def send_email_alert(frame_number, confidence, video_path, frame):
    # Define the SMTP server credentials
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'your_email@gmail.com'  # Replace with sender's email
    sender_password = 'your_app_password'  # Use App Password if using Gmail
    recipient_email = 'recipient_email@example.com'  # Replace with actual recipient email

    # Create the email content
    subject = "🚨 Shoplifting Alert!"
    body = (
        f"⚠️ Alert! Suspicious activity detected in surveillance footage.\n\n"
        f"📹 Video File: {video_path}\n"
        f"🕒 Frame: {frame_number}\n"
        f"🎯 Confidence Score: {confidence:.2f}\n\n"
        f"Please review the attached frame."
    )

    # Set up MIME message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Encode the frame to attach
    _, img_encoded = cv2.imencode('.jpg', frame)
    img_bytes = img_encoded.tobytes()

    # Attach the image
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(img_bytes)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="frame_{frame_number}.jpg"')
    msg.attach(part)

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
