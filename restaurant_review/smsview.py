import os
from twilio.rest import Client
from django.shortcuts import render
from .models import SMS
from django.urls import reverse


def send_text_message(request):
    success_message = None
    error_message = None
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        message_body = (
            "Hello "
            + first_name
            + " "
            + last_name
            + ", David gave you a ChatGPT powered number, save it to your contacts and chat with you."
        )

        # Authenticate with Twilio
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)

        # Get an available Twilio phone number
        numbers = client.available_phone_numbers("US").local.list(
            sms_enabled=True,
            voice_enabled=True,
            mms_enabled=True,
            fax_enabled=True,
            limit=1,
        )
        if len(numbers) > 0:
            number = client.incoming_phone_numbers.create(
                phone_number=numbers[0].phone_number,
                sms_url="http://a6a10f0403c4.ngrok.io/sms_webhook/",
            )
            twilio_number = number.phone_number
        else:
            twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

        # Send the text message
        message = client.messages.create(
            body=message_body,
            from_=twilio_number,
            to=phone_number,
        )

        # Save the SMS message to the database
        sms = SMS(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            message_body=message_body,
            twilio_number=twilio_number,
        )
        sms.save()

        success_message = "Text message sent successfully!"

    return render(
        request,
        "restaurant_review/send_text_message.html",
        {"success_message": success_message, "error_message": error_message},
    )
