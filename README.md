# 🚀 Automated Job Tracker Alert

A fully automated, cloud-native Python microservice that scrapes **real-time Full Stack Developer job postings** specifically in **Bengaluru, India**, filters for brand-new unique listings using a smart memory system, and delivers targeted email alerts — entirely autonomously via GitHub Actions, with zero dependency on your local machine.

---

## ✨ Features

- **Real-Time Data Extraction**: Integrates with the JSearch API (RapidAPI) to pull live job postings from **every company** across all major platforms (LinkedIn, Indeed, Glassdoor, etc.).
- **Smart Memory System**: Maintains a `seen_jobs.csv` memory file that tracks all previously alerted jobs, ensuring you **never receive duplicate alerts**.
- **15-Day Auto Memory Reset**: The memory file automatically resets every 15 days to prevent file bloat, re-establishing a fresh baseline seamlessly.
- **Silent Trigger**: If no new job openings are found on a given day, the system stays **completely silent** — no email, no noise.
- **Intelligent Error Alerting**: If the RapidAPI service fails or exceeds its quota, the script intentionally crashes, causing GitHub Actions to turn **Red** and immediately send you a **"Workflow Failed"** alert email.
- **Automated Email Delivery**: Sends a beautifully structured email with a CSV attachment containing **only fresh, unseen job listings**.
- **100% Cloud Automated (CI/CD)**: Runs every day at **2:30 PM India Time (IST)** on GitHub's servers — no local machine, no open terminal required.

---

## 🎯 Search Configuration

| Parameter       | Value                   |
|----------------|--------------------------|
| **Job Role**    | Full Stack Developer     |
| **Location**    | Bengaluru, India         |
| **Companies**   | ALL (No filters applied) |
| **Schedule**    | Daily at 2:30 PM IST     |

---

## 🛠️ Tech Stack

| Technology        | Purpose                              |
|------------------|--------------------------------------|
| Python 3.10       | Core scripting language              |
| `requests`        | API communication with JSearch       |
| `pandas`          | Data structuring and CSV management  |
| `smtplib`         | SMTP email delivery via Gmail        |
| `python-dotenv`   | Secure environment variable loading  |
| JSearch (RapidAPI)| Real-time job data source            |
| GitHub Actions    | Cloud scheduling and CI/CD pipeline  |

---

## ⚙️ How the Smart Workflow Works

### 📅 Day 1 (Setting the Baseline)
- Memory file `seen_jobs.csv` does not exist yet.
- Script fetches ALL live Full Stack Developer jobs in Bengaluru.
- Since memory is empty, **all jobs are treated as new**.
- Email alert is sent with all jobs. Memory file is created and pushed to GitHub.
- A date stamp `seen_jobs_date.txt` is created to start the 15-day clock.

### 📅 Days 2–15 (Smart Filtering Phase)
- **Situation A — New Jobs Found:** Script fetches live jobs, filters out everything already in memory, and emails **only the brand-new listings**. New jobs are appended to memory.
- **Situation B — No New Jobs:** Every live job is already in memory. Script stays **completely silent**. No email is sent.
- **Situation C — API Failure:** RapidAPI fails or quota is exceeded. Script intentionally crashes. GitHub turns **Red** and sends a **failure alert email** to your account.

### 📅 Day 16 (Memory Reset)
- The 15-day clock expires.
- Both `seen_jobs.csv` and `seen_jobs_date.txt` are **completely wiped**.
- Day 16 is treated exactly like Day 1 — a fresh baseline is re-established with today's date stamp.
- This cycle repeats forever, automatically.

---

## ☁️ Local Setup & Installation

Follow these steps if you want to run the project on your own machine:

**1. Clone the repository:**
```bash
git clone https://github.com/priyanshu0508/Automated-Job-Tracker-Alert.git
cd Automated-Job-Tracker-Alert
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Configure Environment Variables:**

Create a `.env` file in the root directory:
```env
RAPIDAPI_KEY=your_rapidapi_jsearch_key
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_gmail_app_password
RECEIVER_EMAIL=receiver_email@gmail.com
```
> ⚠️ If using Gmail, you **must** use an [App Password](https://myaccount.google.com/apppasswords), not your regular login password.

**4. Run the script:**
```bash
python main.py
```

---

## ☁️ Cloud Deployment (GitHub Actions)

This project is fully configured for autonomous cloud execution. To deploy it:

1. Fork or push this repository to your GitHub account.
2. Navigate to **Settings → Secrets and variables → Actions**.
3. Add the following **Repository Secrets** (matching your `.env` values):

| Secret Name       | Value                        |
|------------------|------------------------------|
| `RAPIDAPI_KEY`    | Your JSearch RapidAPI key    |
| `SENDER_EMAIL`    | Your Gmail address           |
| `SENDER_PASSWORD` | Your Gmail App Password      |
| `RECEIVER_EMAIL`  | Your alert destination email |

4. The workflow (`.github/workflows/job_scraper.yml`) will automatically trigger daily via the CRON schedule.
5. To test immediately: go to **Actions → Daily Job Tracker Automated Alert → Run workflow**.

---

## 📁 Project Structure

```
Automated-Job-Tracker-Alert/
│
├── .github/
│   └── workflows/
│       └── job_scraper.yml     # GitHub Actions cloud automation
│
├── main.py                     # Core logic: fetch, filter, email
├── requirements.txt            # Python dependencies
├── seen_jobs.csv               # Auto-generated memory file (gitignored locally)
├── seen_jobs_date.txt          # Auto-generated 15-day reset clock
├── .gitignore                  # Prevents .env from being pushed
└── README.md                   # Project documentation
```

---

## 📬 Email Alert Sample

**Subject:** `🚀 5 New Full Stack Developer Job(s) Found Today!`

**Body:** Friendly notification stating the number of brand-new listings found.

**Attachment:** `new_jobs_today.csv` containing:

| Role | Company | Location | Link |
|------|---------|----------|------|
| Full Stack Developer | XYZ Corp | Bengaluru, IN | [Apply Here](#) |

---

*Built to automate the job hunt and demonstrate end-to-end cloud pipeline engineering.*
