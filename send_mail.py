import smtplib
from email.mime.text import MIMEText

def send_mail(customer,dealer,rating,comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '533d26e657dd98'
    password = 'd22b8c47331801'
    message = f"<h2>Customer Feedback</h2><br><h3>Customer: {customer}</h3><br><h3>Dealer: {dealer}</h3><br><h3>Rating: {rating}</h3><br><h3>Comments: {comments}</h3>"

    sender_email = 'Xj5kG@example.com'       
    receiver_email = 'email2@example.com'
    message = MIMEText(message, 'html')
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Lexus Feedback'

    # Send email
    with smtplib.SMTP(smtp_server,port) as server:
        server.login(login,password)
        server.sendmail(sender_email, receiver_email, message.as_string())