from sms import SmsClient

twilio_client = SmsClient()

if __name__ == "__main__":
    twilio_client.send_prompts()
