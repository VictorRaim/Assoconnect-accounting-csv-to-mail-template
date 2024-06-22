from __future__ import print_function
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
import getpass
import argparse
import json


# Create an API instance
def create_api_instance():
    api_key = getpass.getpass("Enter your API key: ")
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    return api_instance


def send_email(sender_name: str, sender_email: str, recipient_email: str, email_text: str, subject: str, api_instance):
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        sender={"name": sender_name, "email": sender_email},
        to=[{"email": recipient_email}],
        html_content="<p>{}</p>".format(email_text.replace("\n", "<br>")),
        subject=subject,
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print("Email sent to: {}".format(recipient_email))
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling send_transac_email for recipient {}: {}".format(recipient_email, e))


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sender_info", help="Path to json file with sender_name and sender_email.",
                        default="data/sender_info.json")  # TODO: and recipient_email also (to change)

    args = parser.parse_args()

    sender_info_path = args.sender_info

    with open(sender_info_path, 'r') as file:
        sender_info = json.load(file)

    # Email sender and recipients info
    sender_name = sender_info["sender_name"]
    sender_email = sender_info["sender_email"]

    # TODO: to change
    recipient_email = sender_info["recipient_email"]

    email_text = "Bonjour, \n\nTest 123\n\nCordialement, \nToi"
    subject = "Test email 3"

    # Create an API instance
    api_instance = create_api_instance()

    # Send the email
    send_email(sender_name, sender_email, recipient_email, email_text, subject, api_instance)
