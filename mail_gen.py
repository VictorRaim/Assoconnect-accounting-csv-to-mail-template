import pandas as pd
import os
import argparse


def extract_names(full_name: str):
    """
    Extract the first name and last name from a full name string.
    :param full_name: First name (not all caps) followed by last name (all caps).
    :return: first_name, last_name.
    """
    words = full_name.split(" ")
    first_name_parts = []
    last_name_parts = []

    for index, word in enumerate(words):
        if word.isupper():
            # Split at the first all-caps word
            first_name_parts = words[:index]
            last_name_parts = words[index:]
            break

    first_name = ' '.join(first_name_parts)
    last_name = ' '.join(last_name_parts)

    return first_name, last_name


def find_email_address(annuaire_df: pd.DataFrame, person_name: str):
    """
    Find the email address of a person in the annuaire DataFrame.
    :param annuaire_df: DataFrame with columns 'Prénom', 'Nom', 'Email'.
    :param person_name: Person full name.
    :return: Email address of the person.
    """
    # Extract first name and name from the person_name string
    first_name, name = extract_names(person_name)

    if not first_name or not name:
        raise ValueError(
            "Invalid person name format. Ensure the first name is capitalized and the last name is in all caps.")

    # Find matching entries in the dataframe
    matches = annuaire_df[(annuaire_df['Prénom'] == first_name) & (annuaire_df['Nom'] == name)]

    # Ensure there is exactly one match
    if len(matches) == 1:
        return matches.iloc[0]['Email']
    elif len(matches) == 0:
        print(f"No matching entry found for {person_name}.")
        return None
    else:
        print(f"Multiple matching entries found for {person_name}.")
        return None


def process_person_data(debt_df: pd.DataFrame, annuaire_df: pd.DataFrame, start_idx: int, end_idx: int,
                        header_info: str, banking_info: str):
    """
    Process the data for a single person and generate an email if the balance is negative. If the balance is positive or 0, None None None is returned.
    :param debt_df: debt DataFrame
    :param annuaire_df: Annuaire DataFrame
    :param start_idx: Start idx of the person's data (Début row)
    :param end_idx: End idx of the person's data (Fin row)
    :param header_info: Line just above Début row
    :param banking_info: Bank information string to include in the email
    :return: person_name, person_email_address, email_text.
             If the balance is positive or 0, None None None is returned.
             If the email address is not found, None is returned for the email address.
    """
    person_data = debt_df.iloc[start_idx: end_idx + 1].copy()

    person_name = "-".join(str(header_info).split("-")[2:]).strip()

    first_name = person_name.split()[0]

    # Set "Personne" column to the person's name for start and end rows
    person_data.loc[start_idx, "Personne"] = person_name
    person_data.loc[end_idx, "Personne"] = person_name

    person_data = person_data.fillna("")
    assert person_name == person_data["Personne"].iloc[0]
    total_balance = person_data.iloc[-1]["Solde (EUR)"]

    # Only generate email if the balance is negative (ends with 'D')
    if total_balance.endswith("D"):
        person_email_address = find_email_address(annuaire_df, person_name)

        details = person_data[
            [
                "Id pièce",
                "Date",
                "Intitulé",
                "Débit (EUR)",
                "Crédit (EUR)",
                "Solde (EUR)",
            ]
        ].to_string(index=False, header=False)
        email_text = f"""\
Bonjour {first_name},

Je prends ma casquette de trésorier pour t'informer que ton solde envers le club est négatif. Le détail des dettes au 1er janvier est le suivant :

{header_info}
{details}

Merci de régler ce solde rapidement via un virement sur le compte suivant:
{banking_info}

Si tu ne peux pas régler toute la somme en une seule fois, n'hésite pas à régler le montant d'une ou plusieurs lignes plutôt qu'un montant fixe (c'est plus simple pour la compta de mon côté ;) )
"""
        return person_name, person_email_address, email_text
    return None, None, None


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debt_csv", help="Path to dette_creances.csv file", default="data/dettes_creances.csv")
    parser.add_argument("-a", "--annuaire", help="Path to annuaire file", default="data/annuaire.csv")
    parser.add_argument("-b", "--banking_info", help="Path to bank information file", default="data/banking_info.txt")
    args = parser.parse_args()

    # Read the debt CSV file
    debt_df = pd.read_csv(args.debt_csv)

    # Read the banking information file
    with open(args.banking_info, "r") as file:
        banking_info = file.read()

    # Read the annuaire file
    annuaire_df = pd.read_csv(args.annuaire)

    # Process the DataFrame to find all persons and generate emails
    emails = []
    header_info = None
    i = 0
    while i < len(debt_df):
        if " - " in str(debt_df.iloc[i]["Id pièce"]):
            header_info = str(debt_df.iloc[i]["Id pièce"])
        if debt_df.iloc[i]["Id pièce"] == "Début":
            start_idx = i
        elif debt_df.iloc[i]["Id pièce"] == "Fin":
            end_idx = i
            if (
                    header_info and start_idx > 1
            ):  # Ensure the first empty subtable is ignored
                person_name, person_email_address, email_text = process_person_data(
                    debt_df, annuaire_df, start_idx, end_idx, header_info, banking_info)

                if person_name is not None and email_text is not None:
                    emails.append((person_name, person_email_address, email_text))
        i += 1

    # Create directory for emails
    emails_dir = os.path.join("data", "emails")
    if not os.path.exists(emails_dir):
        os.makedirs(emails_dir)

    # Dataframe with name, emails addresses and emails text file
    summary_df = pd.DataFrame([], columns=["Name", "Email Address", "Email File"])

    # Save emails to text files
    for person_name, person_email_address, email_text in emails:
        if person_name is None:
            raise ValueError("Person name cannot be None.")
        if person_email_address is None:
            person_email_address = "UNKNOWN"
        if email_text is None:
            raise ValueError("Email text cannot be None.")

        filename = os.path.join(
            emails_dir, f"email_{person_name.replace(' ', '_')}.txt"
        )
        with open(filename, "w", encoding="utf-8") as file:
            file.write(email_text)

        summary_df = pd.concat([summary_df, pd.DataFrame([[person_name, person_email_address, filename]],
                                                         columns=["Name", "Email Address", "Email File"])],
                               ignore_index=True)

    print("Emails generated and saved in the 'data/emails' directory.")

    summary_df.to_csv(os.path.join(emails_dir, "summary.csv"), index=False)
