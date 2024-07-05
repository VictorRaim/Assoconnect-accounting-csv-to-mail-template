# Setup:

Install the packages using `pip install -r requirements.txt` in a virtual environment (conda, venv etc.)

# mail_gen.py:

The emails are written for each person to a different html file using this script.
The script takes the following arguments:
- dettes_creances csv file path (`-d`)
- annuaire csv file path (`-a`)
- banking infos csv file path (`-b`)

You can follow the default location (`data/`) and names (see `mail_gen.py`) for those files.

The emails will be written to html files in `data/emails`.
Also, a csv file summarizing everything will be written to `data/emails/summary.csv`. It will contain, the name of the
person, their email address and the path to the email html file.

# send_emails.py:

Script to send emails to everyone. If you don't modify it (uncomment the danger zone), it will just send one email to
the dummy recipient address indicated in the sender_info json file.

It takes the following arguments:
- sender_info json path (`-s`). Should contain the following entries:
    - "sender_name": "Michel Tresorier"
    - "sender_email": "michel@asso.fr"
    - "dummy_recipient_email": "random_adherent@gmail.com"
- summary csv file (generated by `mail_gen.py`) path (`-c`) 
