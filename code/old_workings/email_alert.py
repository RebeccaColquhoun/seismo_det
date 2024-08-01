from trycourier import Courier
def notify():
    client = Courier(auth_token="pk_prod_EY2K02YWXAM66WGS578G43MN5R0S")
    resp = client.send_message(
            message={
                "to": {"email": "rcolquhoun13@gmail.com"},
                "content": {"title": "Code is done!", "body":"code is done"}})
