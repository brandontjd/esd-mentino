import smtplib
from channel import Channel
import json
from os import environ

USERNAME = environ.get("EMAIL_USERNAME")
PASSWORD = environ.get("EMAIL_PASSWORD")

hostname = environ.get("RABBITMQ_HOSTNAME", default="localhost")
port = int(environ.get("RABBITMQ_PORT", default="5672"))
exchangename = "esd_exchange"
exchangetype = "topic"

pika_channel = Channel(
    hostname,
    port,
    exchangename,
    exchangetype
)

monitorBindingKey='*.email'

def callback(channel, method, properties, body): # required signature for the callback; no return
    payload = json.loads(body)

    try:
        emails = payload["emails"]
        event_name = payload["event"]
        bubble_name = payload["bubble_name"]

        subject, body = get_message(event_name, bubble_name)

        msg = "\r\n".join([
            "From: " + USERNAME,
            "To: " + ", ".join(emails),
            "Subject: " + subject,
            "",
            body
        ])
        print(msg)
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, emails, msg)
        server.quit()
    except Exception as e:
        print(str(e))

def get_message(event_name, bubble_name):
    if event_name == "mentor_joined":
        subject = "The Mentoring Bubble - Mentor Joined!"
        body = f"Hello!\n\nA mentor just joined in the Bubble - {bubble_name}. Do take a look!\n\nTMB Team"
        return subject, body

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, exchangename))

    pika_channel.set_consume_callback(queue="send_email", callback=callback)
    pika_channel.start_consuming()