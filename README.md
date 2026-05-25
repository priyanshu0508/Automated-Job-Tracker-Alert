# 🚀 Automated Job Tracker Alert

A fully automated, cloud-native Python microservice that scrapes real-time job postings, processes the data into a structured CSV, and delivers daily email alerts straight to your inbox. 

Built to eliminate the manual grind of daily job hunting, this tool runs autonomously in the cloud via GitHub Actions.

## ✨ Features

- **Real-Time Data Extraction**: Integrates with the JSearch API (RapidAPI) to pull live job postings across major platforms (LinkedIn, Indeed, Glassdoor).
- **Data Processing**: Utilizes `pandas` to clean, structure, and export the scraped data into a highly readable CSV format.
- **Automated Email Delivery**: Implements `smtplib` and `MIME` to securely construct and dispatch emails with the CSV report attached.
- **100% Cloud Automated (CI/CD)**: Deployed using GitHub Actions, ensuring the script executes reliably every single day on a remote server without needing a local machine.

## 🛠️ Tech Stack

- **Language:** Python 3.10
- **Libraries:** `requests`, `pandas`, `smtplib`, `python-dotenv`
- **API:** JSearch via RapidAPI
- **Cloud Automation:** GitHub Actions

## ⚙️ Local Setup & Installation

If you wish to run this project locally on your machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/priyanshu0508/Automated-Job-Tracker-Alert.git
   cd Automated-Job-Tracker-Alert
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your credentials:
   ```env
   RAPIDAPI_KEY=your_rapidapi_jsearch_key
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_gmail_app_password
   RECEIVER_EMAIL=receiver_email@gmail.com
   ```
   *(Note: If using Gmail, you must use an [App Password](https://myaccount.google.com/apppasswords), not your standard login password).*

4. **Run the script:**
   ```bash
   python main.py
   ```

## ☁️ Cloud Deployment (GitHub Actions)

This project is configured to run automatically in the cloud every day at 09:00 UTC. To deploy it to your own GitHub account:

1. Fork or push this repository to your GitHub account.
2. Go to your repository **Settings** > **Secrets and variables** > **Actions**.
3. Add the 4 environment variables from the `.env` setup as **Repository Secrets**.
4. The GitHub Actions workflow (located in `.github/workflows/job_scraper.yml`) will now trigger automatically based on the defined CRON schedule.

---
*Built to make the job hunt a little easier and showcase end-to-end automation skills.*
