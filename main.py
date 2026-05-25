import os
import requests
import pandas as pd
import smtplib
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fetch_jobs(role, location):
    """Fetches real-time job data from the JSearch API."""
    print(f"Fetching real-time jobs for '{role}' in '{location}'...")
    
    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("ERROR: RapidAPI Key is missing or invalid in the .env file.")
        return []

    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {
        "query": f"{role} in {location}",
        "page": "1",
        "num_pages": "1"
    }
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        
        extracted_jobs = []
        if 'data' in data:
            for job in data['data']:
                extracted_jobs.append({
                    "Role": job.get("job_title", "N/A"),
                    "Company": job.get("employer_name", "N/A"),
                    "Location": f"{job.get('job_city', '')}, {job.get('job_country', '')}".strip(', '),
                    "Link": job.get("job_apply_link", "N/A")
                })
        
        print(f"Successfully found {len(extracted_jobs)} jobs.")
        return extracted_jobs
        
    except Exception as e:
        print(f"An error occurred while fetching jobs: {e}")
        return []

def save_to_csv(jobs_data, filename="jobs.csv"):
    """Saves the structured data to a CSV file."""
    if not jobs_data:
        print("No job data to save.")
        return False

    df = pd.DataFrame(jobs_data)
    df.to_csv(filename, index=False)
    print(f"Data successfully saved to {filename}!")
    return True

def send_email_alert(filename="jobs.csv"):
    """Sends the daily email alert with the CSV attached."""
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    if not sender_email or sender_email == "your_email@gmail.com":
        print("ERROR: Email credentials are not set up in the .env file.")
        print("Please configure your email settings to receive alerts.")
        return

    print("Preparing to send email alert...")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Your Daily Automated Job Tracker Alert 🚀"

    body = "Hello!\n\nHere is your daily list of real-time job matches for Full Stack Developer in Bengaluru.\nPlease find the attached CSV file with the latest opportunities.\n\nGood luck with your applications!"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            msg.attach(part)
    except FileNotFoundError:
        print(f"Could not find {filename} to attach.")
        return

    try:
        print("Connecting to email server...")
        # We are using Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Email alert sent successfully!")
        
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
        print("If you are using Gmail, make sure you used an 'App Password', not your regular password.")
    finally:
        server.quit()


def run_tracker():
    print("=== Automated Job Tracker Started ===\n")
    
    target_role = "Full Stack Developer"
    target_location = "Bengaluru, India"
    
    # Step 1: Fetch Jobs
    jobs = fetch_jobs(target_role, target_location)
    
    # Step 2: Save to CSV
    saved_successfully = save_to_csv(jobs)
    
    # Step 3: Send Email
    if saved_successfully:
        send_email_alert()
    
    print("\n=== Process Complete ===")

if __name__ == "__main__":
    # Since we are moving to Cloud Automation, the cloud server 
    # will handle the scheduling. This script just needs to run once and exit.
    run_tracker()
