# Snapshot 📸

A simple game with the primary interface being sms

Users are able to sign up by texting a specific number, and will receive a
weekly prompt. Users can submit a photo for the prompt by sending an image over sms

Once a user has submitted a response, they will receive a link to a webpage to
view all of the photos submitted by users.

Uses the Twilio API, written in Go

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

Format using gofumpt
```bash
go fmt
```

Run the tests
```bash
go test ./...
```

Run the server to debug
```bash
go run .
```

Run the server with some debug environment variables
```bash
DEBUG=1 SHELL=1 IN_MEMORY_DB=1 go run .
```

Build the server (prod)
```bash
go build
./snapshot
```

### Beta environment

The beta environment allows us to test changes before pushing to production, while still only using a single twilio number.
In the .env, set the environment to `BETA`, and confirm you have set the `beta_code` and `beta_allowlist`.

In twilio, add a backup message webhook, which points to the beta url.

To route messages to the beta webhook, start any message with the `beta_code`.
To route images to the beta webhook, first send a single message containing only the `beta_code`. Then, send an image normally.
