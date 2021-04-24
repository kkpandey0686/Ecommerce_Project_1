import os 
from twilio.rest import Client

account_sid = 'ACdb92b6b2cdbaf144f45e31659c1acbef'
auth_token = '93389b7cf4313e72a5ca89936710fc8c'
client = Client(account_sid,auth_token)

def send_sms(user_code, phone_number):
    message = client.messages.create(
        body = f'Hi! Your user and verification code is {user_code}',
        from_='+15032785568',
        to=f'+91{phone_number}'
    )

    print(message.sid)