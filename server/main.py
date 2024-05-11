from test_client import TestClient

client = TestClient()

while True:
    text = input()
    client.receive_message("9517518340", text)
