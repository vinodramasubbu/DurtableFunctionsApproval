# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

from datetime import timedelta
import logging
import json

import azure.functions as func
import azure.durable_functions as df


def orchestrator_function(context: df.DurableOrchestrationContext):
    challenge_code = yield context.call_activity('SendApprovalRequest', "")
    logging.info(challenge_code)
    expiration = context.current_utc_datetime + timedelta(seconds=180)
    timeout_task = context.create_timer(expiration)
    
    authorized = False
    for _ in range(3):
        challenge_response_task = context.wait_for_external_event("SmsChallengeResponse")
        approval = yield context.task_any([challenge_response_task, timeout_task])
        logging.info(approval.result)

        #if (approval == challenge_response_task):


        if (str(approval.result) == challenge_code):
            logging.info("i have reached if loop approval")
            logging.info(approval.result)
            logging.info(challenge_code)
            authorized = True
            response = yield context.call_activity('RequestStatus', "Approved")
            break
        else:
            # Timeout expired
            logging.info("i have reached else loop")
            logging.info(approval.result)
            logging.info(challenge_code)
            response = yield context.call_activity('RequestStatus', "Not Approved")
            break
  
    if not timeout_task.is_completed:
        logging.info("i have reached timeout_task.is_completed check")
        # All pending timers must be complete or canceled before the function exits.
        timeout_task.cancel()


    return [response]

main = df.Orchestrator.create(orchestrator_function)