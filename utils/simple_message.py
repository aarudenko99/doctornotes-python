import requests


def send_simple_message(subject, message, send_from, send_to):
    return requests.post(
        "https://api.mailgun.net/v3/anastomy.com/messages",
        auth=("api", "key-524880b093fe690b6c967d790f9ae7a8"),
        data={"from": send_from,
              "to": send_to,
              "subject": subject,
              "text": message})
