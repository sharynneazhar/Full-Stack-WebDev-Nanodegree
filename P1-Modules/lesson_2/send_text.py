from twilio.rest import TwilioRestClient

# account sid and auth token from twilio.com/account
account_sid = "AC6ee92ddf906064227893c5f909ec37ae"
auth_token  = "d682589f64a37097c6a60d3379785b01"

client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(
    body="hack bot hello michelle cheung",
    to="+19132718832",    # Replace with your phone number
    from_="+19134395674") # Replace with your Twilio number

print(message.sid)
