# Snapshot 📸

A simple game with the primary interface being sms

Users are able to sign up by texting a specific number, and will receive a
weekly prompt. Users can submit a photo for the prompt by sending an image over sms

Once a user has submitted a response, they will receive a link to a webpage to
view all of the photos submitted by users.

API built using FastAPI.
Uses Twilio api for the sms interface
SQLAlchemy as an ORM for Sqlite3.

### Development

Initialize the database

```bash
sqlite3 snapshot.db < schema.sql
```

Setup the .env
```
environment=
twilio_account_sid=
twilio_auth_token=
twilio_phone_number=
db_name=
hash_secret=
admin_pass=
beta_code=
beta_allowlist=
```

Run the tests
```bash
pytest
```

Start the server
```bash
fastapi run main.py
```

Format code before new changes
```bash
black .
```
