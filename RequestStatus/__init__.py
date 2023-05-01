# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import json
import logging
import os
from azure.communication.email import EmailClient
import random


def main(name: str) -> str:

    response = "Your Request is " + str(name) + "."
    html_message = "<html><h1>" + response + "</h1></html>"
    # Create the EmailClient object that you use to send Email messages.
    email_client = EmailClient.from_connection_string("endpoint=https://xxxx.communication.azure.com/;accesskey=xxxxxx")

    message = {
    "content": {
        "subject": "Request Status "+ str(name) + ".",
        "plainText": response,
        "html": html_message
    },
    "recipients": {
        "to": [
            {
                "address": "xxx@xxxx.com",
                "displayName": "xxx xxxx"
            }
        ]
    },
    "senderAddress": "DoNotReply@xxxxxxxxx.azurecomm.net"
}

    poller = email_client.begin_send(message)
    logging.info(poller.result())

    #return f"Hello {name}!"
    logging.info(response)
    return str(response)
    #return f"Hello {name}!"

# This function is not intended to be invoked directly. Instead it will be