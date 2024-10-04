import time

from celery import shared_task

from mobicrowd.models.submisson import Submission
import logging

logger = logging.getLogger(__name__)


@shared_task
def process_image(submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
        logger.info(f"Initial status for submission {submission_id}: {submission.status}")

        # Simulate AI processing
        time.sleep(10)  # Replace this with actual AI processing

        # AI Decision Logic
        decision = some_ai_decision_logic(submission)
        logger.info(f"AI decision for submission {submission_id}: {decision}")

        if decision:
            submission.status = Submission.APPROVED
            submission.proceed_or_not = Submission.YES
        else:
            submission.status = Submission.REFUSED
            submission.proceed_or_not = Submission.NO
            logger.info(f"Submission {submission_id} was refused. Ending task.")
            submission.save()
            return  # End the task here if the submission is refused

        logger.info(f"Final status for submission {submission_id}: {submission.status}")
        submission.save()

        # Notify the frontend of the outcome
        notify_frontend(submission.id, submission.status)

    except Submission.DoesNotExist:
        logger.error(f"Submission with ID {submission_id} does not exist.")


import random
def some_ai_decision_logic(submission):
    # Generate a random float between 0 and 1
    random_value = random.random()
    logger.info("random_value", random_value)

    # Decide based on the random value: return True for approval if random_value is greater than 0.5, otherwise return False
    if random_value > 0.5:
        return True
    else:
        return True

def notify_frontend(submission_id, status):
    # Implement your notification logic here
    pass
