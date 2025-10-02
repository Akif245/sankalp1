import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
for i in range(10):
    sender_email = "abdulakif44570@gmail.com"
    receiver_email = "aslammd3770@gmail.com"
    password ="mmbv xksy jlaa moyk"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Automated Email"
    body = "Hello, this is an automated email."
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    break


# import os
# import time
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from getpass import getpass

# sender_email = "abdulakif44570@gmail.com"
# receiver_email = "aslammd3770@gmail.com"

# # Prefer storing the password in an environment variable; fallback to prompt if not set
# password = os.environ.get("mmbv xksy jlaa moyk") or getpass("Enter email password (or app password): ")

# message = MIMEMultipart()
# message["From"] = sender_email
# message["To"] = receiver_email
# message["Subject"] = "Automated Email"
# body = "Hello, this is an automated email."
# message.attach(MIMEText(body, "plain"))

# # Connect once, login once, then loop sends
# try:
#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#         server.login(sender_email, password)
#         for i in range(10):  # send 10 times
#             try:
#                 server.sendmail(sender_email, receiver_email, message.as_string())
#                 print(f"Sent email #{i+1}")
#             except Exception as e:
#                 print(f"Failed to send email #{i+1}: {e}")
#             time.sleep(1)  # optional: small delay between sends
# except Exception as e:
#     print("SMTP connection/login failed:", 