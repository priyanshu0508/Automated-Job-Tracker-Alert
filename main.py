import os
import sys
import requests
import pandas as pd
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
TARGET_ROLE     = "Full Stack Developer"
TARGET_LOCATION = "Bengaluru, India"
MEMORY_FILE     = "seen_jobs.csv"
MEMORY_DATE_FILE = "seen_jobs_date.txt"
MEMORY_RESET_DAYS = 15   # Reset memory every 15 days


# ─────────────────────────────────────────────
# STEP 1: FETCH JOBS FROM API
# ─────────────────────────────────────────────
def fetch_jobs(role, location):
    """Fetches real-time job data from the JSearch API."""
    print(f"Fetching real-time jobs for '{role}' in '{location}'...")

    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("ERROR: RapidAPI Key is missing or invalid.")
        sys.exit(1)  # Fire alarm – crash immediately so GitHub turns Red

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
                    "Role":     job.get("job_title",       "N/A"),
                    "Company":  job.get("employer_name",   "N/A"),
                    "Location": f"{job.get('job_city', '')}, {job.get('job_country', '')}".strip(', '),
                    "Link":     job.get("job_apply_link",  "N/A")
                })

        print(f"Successfully fetched {len(extracted_jobs)} live jobs from API.")
        return extracted_jobs

    except Exception as e:
        # FIX: Instead of silently returning [], we CRASH the script.
        # This forces GitHub to turn RED and email you a failure notice.
        print(f"FATAL ERROR while fetching jobs: {e}")
        raise e   # <-- The "Fire Alarm"


# ─────────────────────────────────────────────
# STEP 2: MEMORY SYSTEM (15-Day Reset)
# ─────────────────────────────────────────────
def load_memory():
    """
    Loads the list of previously seen job links from seen_jobs.csv.
    If the memory file is older than 15 days, it wipes it clean (reset).
    Returns a Python SET of job links already sent to the user.
    """
    # Check if a date file exists to track when memory was first created
    if os.path.exists(MEMORY_DATE_FILE):
        with open(MEMORY_DATE_FILE, "r") as f:
            start_date_str = f.read().strip()
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        days_elapsed = (datetime.now() - start_date).days

        if days_elapsed >= MEMORY_RESET_DAYS:
            # ─── 15-DAY RESET ───
            print(f"Memory is {days_elapsed} days old. Resetting memory to start fresh!")
            if os.path.exists(MEMORY_FILE):
                os.remove(MEMORY_FILE)
            if os.path.exists(MEMORY_DATE_FILE):
                os.remove(MEMORY_DATE_FILE)
            return set()   # Return empty memory after wipe

    # Load existing memory if file exists
    if os.path.exists(MEMORY_FILE):
        df = pd.read_csv(MEMORY_FILE)
        seen_links = set(df["Link"].dropna().tolist())
        print(f"Memory loaded: {len(seen_links)} previously seen jobs found.")
        return seen_links

    # No memory file yet (Day 1)
    print("No memory file found. This is Day 1 – treating all jobs as new.")
    return set()


def save_memory(new_jobs):
    """
    Appends newly emailed jobs to the memory file (seen_jobs.csv).
    Also creates the date file on Day 1 to track the 15-day reset clock.
    """
    # Create or stamp the date file on first run
    if not os.path.exists(MEMORY_DATE_FILE):
        with open(MEMORY_DATE_FILE, "w") as f:
            f.write(datetime.now().strftime("%Y-%m-%d"))
        print("Memory clock started today (Day 1).")

    new_df = pd.DataFrame(new_jobs)

    if os.path.exists(MEMORY_FILE):
        # Append new jobs to existing memory
        existing_df = pd.read_csv(MEMORY_FILE)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df.drop_duplicates(subset=["Link"], inplace=True)
        combined_df.to_csv(MEMORY_FILE, index=False)
    else:
        # Create new memory file from scratch
        new_df.to_csv(MEMORY_FILE, index=False)

    print(f"Memory updated: {len(new_jobs)} new job(s) saved to memory.")


# ─────────────────────────────────────────────
# STEP 3: SMART FILTER
# ─────────────────────────────────────────────
def filter_new_jobs(live_jobs, seen_links):
    """
    Compares live jobs from the API against the memory.
    Returns ONLY brand new jobs never seen before.
    """
    new_jobs = [job for job in live_jobs if job["Link"] not in seen_links]
    print(f"Smart Filter result: {len(new_jobs)} brand new job(s) found out of {len(live_jobs)} live jobs.")
    return new_jobs


# ─────────────────────────────────────────────
# STEP 4: SEND EMAIL
# ─────────────────────────────────────────────
def send_email_alert(new_jobs):
    """Sends the email alert with ONLY the new unique jobs attached as a CSV."""
    sender_email    = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    receiver_email  = os.getenv("RECEIVER_EMAIL")

    if not sender_email or sender_email == "your_email@gmail.com":
        print("ERROR: Email credentials are missing in environment variables.")
        sys.exit(1)

    # Save the new jobs to a temporary CSV to attach to the email
    temp_csv = "new_jobs_today.csv"
    pd.DataFrame(new_jobs).to_csv(temp_csv, index=False)

    print(f"Preparing email with {len(new_jobs)} new job(s)...")

    msg = MIMEMultipart()
    msg['From']    = sender_email
    msg['To']      = receiver_email
    msg['Subject'] = f"🚀 {len(new_jobs)} New Full Stack Developer Job(s) Found Today!"

    body = (
        f"Hello!\n\n"
        f"Great news! Your Automated Job Tracker has found {len(new_jobs)} brand NEW "
        f"Full Stack Developer job opening(s) in Bengaluru today.\n\n"
        f"These are FRESH postings you have never been alerted about before.\n"
        f"Please find the attached CSV file with all the latest opportunities.\n\n"
        f"Good luck with your applications!\n\n"
        f"— Your Automated Job Tracker Bot 🤖"
    )
    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(temp_csv, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename=new_jobs_today.csv")
            msg.attach(part)
    except FileNotFoundError:
        print(f"Could not find {temp_csv} to attach.")
        sys.exit(1)

    try:
        print("Connecting to Gmail server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("✅ Email alert sent successfully!")
    except Exception as e:
        print(f"FATAL ERROR sending email: {e}")
        raise e
    finally:
        server.quit()

    # Clean up the temporary CSV
    if os.path.exists(temp_csv):
        os.remove(temp_csv)


# ─────────────────────────────────────────────
# MAIN RUNNER
# ─────────────────────────────────────────────
def run_tracker():
    print("=" * 50)
    print("   Automated Job Tracker Started")
    print("=" * 50)

    # Step 1: Fetch all live jobs from API
    live_jobs = fetch_jobs(TARGET_ROLE, TARGET_LOCATION)

    # Step 2: Load memory (with 15-day reset check)
    seen_links = load_memory()

    # Step 3: Smart Filter – keep only brand new jobs
    new_jobs = filter_new_jobs(live_jobs, seen_links)

    # Step 4: Silent Trigger – only act if new jobs exist
    if len(new_jobs) == 0:
        print("\n🔇 Silent Trigger: No new job openings found today.")
        print("   No email will be sent. Going back to sleep...")
    else:
        print(f"\n🔔 Silent Trigger: {len(new_jobs)} new job(s) found! Sending email alert...")
        send_email_alert(new_jobs)
        save_memory(new_jobs)

    print("\n" + "=" * 50)
    print("   Process Complete")
    print("=" * 50)


if __name__ == "__main__":
    run_tracker()
