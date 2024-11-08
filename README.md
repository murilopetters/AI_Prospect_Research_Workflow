AI-Powered Prospect Research Workflow

Overview
This project automates prospect research for a sales team, generating concise company summaries from website data. The workflow uses web scraping, text summarization, and automated delivery to streamline prospect insights.

Workflow Steps
Data Extraction: Scrapes relevant sections (About Us, Products) from company websites.
Summarization: Summarizes extracted text using Hugging Face’s facebook/bart-large-cnn model.
Storage: Saves summaries as text files.
Delivery: Sends summaries to Slack or via email.

Files
prospect_research.py: Main script for extraction, summarization, and delivery.
requirements.txt: List of dependencies.

Setup
1. Clone the repository: git clone https://github.com/yourusername/AI_Prospect_Research_Workflow.git
2. Install dependencies: pip install -r requirements.txt

Usage
Run the script with a website URL to generate and deliver a summary: python prospect_research.py

Configuration
Slack Webhook: Add a Slack webhook URL in the script for Slack delivery.
Email: Configure email settings for email delivery.
