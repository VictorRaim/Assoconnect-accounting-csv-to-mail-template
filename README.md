# Setup:

Install the packages using `pip install -r requirements.txt` in a virtual environment (conda, venv etc.)

# mail_gen.py:

The emails are written for each person to a different text file using this script.
The script takes the following arguments:

- dettes_creances csv file path (`-d`)
- annuaire csv file path (`-a`)
- banking infos csv file path (`-b`)

You can follow the default location (`data/`) and names (see `mail_gen.py`) for those files.

The emails will be written to text files in `data/emails`.
Also, a summary of the emails will be written to `data/emails/summary.txt`. It will contain, the name of the person,
their email address and the path to the email file.

# send_emails.py:

Dummy script to send a mail to a single person at the moment.

It takes the following arguments:

- sender_info json path (`-s`). Should contain the following entries:
    - "sender_name": "Michel Tresorier"
    - "sender_email": "michel@asso.fr"
    - "recipient_email": "random_adherent@gmail.com"
