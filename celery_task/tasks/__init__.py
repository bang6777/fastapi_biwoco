from celery_task import celery_app
import time

@celery_app.task(name="send_email_task")
def send_email_task(to_email: str, subject: str, body: str):
    try:
        # Simulate sending an email (replace this with actual logic)
        print(f"Sending email to {to_email} with subject: {subject}")
        time.sleep(2)  # Simulate time delay for sending email
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
