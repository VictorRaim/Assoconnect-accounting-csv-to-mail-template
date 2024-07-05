from __future__ import print_function
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
import getpass
import argparse
import json
import pandas as pd


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
        html_content=email_text,
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
    parser.add_argument("-s", "--sender_info",
                        help="Path to json file with sender_name and sender_email "
                             "(and dummy_recipient_email for testing).",
                        default="data/sender_info.json")
    parser.add_argument("-c", "--csv_file", default="data/emails/summary.csv",
                        help="Path to csv file with email htlm path and recipient email.", )

    args = parser.parse_args()

    sender_info_path = args.sender_info

    with open(sender_info_path, 'r') as file:
        sender_info = json.load(file)

    # Email sender and recipients info
    sender_name = sender_info["sender_name"]
    sender_email = sender_info["sender_email"]

    df_summary = pd.read_csv(args.csv_file)

    # Dummy email for testing
    dummy_subject = "Dettes Revos Test 12!"

    email_file_path = df_summary["Email File"][0]

    with open(email_file_path, 'r') as file:
        dummy_email_content = file.read()

    # Create an API instance
    api_instance = create_api_instance()

    # Send the email
    dummy_recipient_email = sender_info["dummy_recipient_email"]
    send_email(sender_name, sender_email, dummy_recipient_email, dummy_email_content, dummy_subject, api_instance)

    # DANGER ZONE: To uncomment to send everything.

    # subject = "Dettes Revos"
    # for index, row in df_summary.iterrows():
    #     email_file_path = row["Email File"]
    #     recipient_email = row["Email Address"]
    #     recipient_name = row["Name"]
    #
    #     # Check if email address is valid
    #     if "@" not in recipient_email:
    #         print(f"Invalid email address: \"{recipient_email}\" for \"{recipient_name}\". Skipping.")
    #         continue
    #
    #     with open(email_file_path, 'r') as file:
    #         email_content = file.read()
    #
    #     # Send the email
    #     send_email(sender_name, sender_email, recipient_email, email_content, subject, api_instance)
