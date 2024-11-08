import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import smtplib
from email.mime.text import MIMEText

# Step 1: Data Extraction
def get_general_info(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises an error for unsuccessful status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        
        keywords = ['about', 'overview', 'company', 'services', 'products']
        info_text = ""

        for keyword in keywords:
            section = soup.find(lambda tag: tag.name in ["section", "div", "p", "article"] and keyword in tag.get_text().lower())
            if section:
                info_text += section.get_text(strip=True) + "\n"
        
        if info_text == "":
            print("No relevant information found. Please check the website structure.")
        return info_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return ""

# Step 2: Summarize the Extracted Data
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(text):
    if not text:
        return "No content available to summarize."
    try:
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error generating summary: {e}")
        return ""

# Step 3: Save the Summary (Optional)
def save_summary(summary, filename="summary.txt"):
    if summary:
        with open(filename, "w") as file:
            file.write(summary)
        print(f"Summary saved to {filename}")
    else:
        print("No summary to save.")

# Step 4: Delivery Options
def send_summary(summary, delivery_method, recipient=None):
    if delivery_method == "slack":
        send_to_slack(summary, recipient)  # Assuming recipient is the webhook URL
    elif delivery_method == "email":
        send_email(summary, recipient)
    else:
        print(f"Invalid delivery method: {delivery_method}")

# Slack and Email Sending Functions
def send_to_slack(summary, webhook_url):
    if not webhook_url:
        print("No Slack webhook URL provided.")
        return
    try:
        response = requests.post(webhook_url, json={"text": summary})
        if response.status_code == 200:
            print("Summary sent to Slack successfully.")
        else:
            print(f"Failed to send to Slack: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending to Slack: {e}")

def send_email(summary, recipient_email):
    sender_email = "your-email@example.com"
    password = "your-email-password"  # Replace with environment variable in production
    smtp_server = "smtp.example.com"  # Replace with actual SMTP server
    port = 587  # Typical port for TLS

    if not recipient_email:
        print("No recipient email provided.")
        return

    msg = MIMEText(summary)
    msg['Subject'] = "Prospect Summary"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Summary sent via email successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Execute Workflow
url = "https://www.hubspot.com/"
general_info = get_general_info(url)
summary = generate_summary(general_info)

# Prompt user for delivery method
delivery_method = input("Choose delivery method ('slack' or 'email'): ").strip().lower()
if delivery_method == "slack":
    slack_webhook_url = "https://hooks.slack.com/services/your/webhook/url"  # Replace with your actual webhook URL
    send_summary(summary, "slack", recipient=slack_webhook_url)
elif delivery_method == "email":
    recipient_email = "sales-team@example.com"  # Replace with recipient email
    send_summary(summary, "email", recipient=recipient_email)

# Optional: Save the summary locally
save_summary(summary)