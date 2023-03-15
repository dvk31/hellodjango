import os
import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import openai
from .models import SMS
import pytube


openai.api_key = os.getenv("OPENAI_API_KEY")
logging.basicConfig(level=logging.INFO)


class SMSHandler:
    def __init__(self, twilio_number):
        self.twilio_number = twilio_number
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.client = Client(self.account_sid, self.auth_token)

    def get_or_create_sms(self, phone_number):
        sms, created = SMS.objects.get_or_create(phone_number=phone_number)
        return sms

    def handle_message(self, body, phone_number):
        logging.info(f"Received SMS from {phone_number}: {body}")

        # Get or create an SMS instance for the phone_number
        sms = self.get_or_create_sms(phone_number)
        print(f"SMS: {sms}")

        # Save the incoming message in the SMS instance
        incoming_message = sms.messages_received.create(
            direction="incoming", content=body
        )
        sms.save()

        # Call the OpenAI API to generate a response based on the user's message
        chat_history = [
            {
                "role": "user" if m.direction == "incoming" else "assistant",
                "content": m.content,
            }
            for m in sms.messages_received.all()
        ]
        print(f"Chat history: {chat_history}")

        try:
            chat_response = self.send_to_openai(chat_history)
            logging.info(f"Received response from OpenAI: {chat_response}")
            print(f"Outgoing message: {chat_response}")

            # Send the response back to the user who sent the SMS message
            self.send_message(chat_response, phone_number, self.twilio_number)
            logging.info(
                f"Sent SMS from {self.twilio_number} to {phone_number}: {chat_response}"
            )

            # Save the outgoing message in the SMS instance
            outgoing_message = sms.messages_received.create(
                direction="outgoing", content=chat_response
            )
            sms.save()  # Make sure this line is outside the try-except block

        except Exception as e:
            logging.error(f"Error with OpenAI API: {str(e)}")
            print(f"Error with OpenAI API: {str(e)}")
            return

    def send_message(self, message, to_number, from_number=None):
        from_number = from_number or self.twilio_number
        message = self.client.messages.create(
            body=message, from_=from_number, to=to_number
        )
        return message

    def send_to_openai(self, chat_history):
        # Use OpenAI's ChatCompletion API to get the chatbot's response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
            max_tokens=3800,
            stop=None,
            temperature=0.7,
        )

        # Find the first response from the chatbot that has text in it (some responses may not have text)
        for choice in response.choices:
            if "text" in choice:
                return choice.text

        # If no response with text is found, return the first response's content (which may be empty)
        return response.choices[0].message.content


@csrf_exempt
def sms_webhook(request):
    # Get the message body and phone number from the incoming Twilio request
    body = request.POST.get("Body", "")
    phone_number = request.POST.get("From", "")

    # Create an instance of the SMSHandler with the Twilio number from the request
    handler = SMSHandler(request.POST.get("To", ""))

    # Handle the incoming message
    handler.handle_message(body, phone_number)

    # Return an HTTP response to Twilio
    twiml = MessagingResponse()
    return HttpResponse(str(twiml))
