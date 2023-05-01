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

    approval_code = random.randint(1000, 9999)
    message = "your approval code is " + str(approval_code) + "."
    html_message = "<html><h1>" + str(approval_code) + "</h1></html>"

    # Create the EmailClient object that you use to send Email messages.
    email_client = EmailClient.from_connection_string("endpoint=https://xxxx.communication.azure.com/;accesskey=xxxxxxxx")

    message = {
    "content": {
        "subject": "Here is the your approval code",
        "plainText": message,
        "html": html_message
    },
    "recipients": {
        "to": [
            {
                "address": "xxxx@xxxxxx.com",
                "displayName": "xxxx xxxx"
            }
        ]
    },
    "senderAddress": "DoNotReply@xxxxxxxx.azurecomm.net"
}

    poller = email_client.begin_send(message)
    logging.info(poller.result())

    #return f"Hello {name}!"
    logging.info(approval_code)
    code_str = str(approval_code)
    return code_str
