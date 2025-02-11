import os
import logging
import smtplib
from time import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from github import Github
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv('Service_Account_File')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = os.getenv('Spreadsheet_Id')
RANGE_NAME = "Sheet1!A2:F5" 
# Adjust this for the range you need from the Google Sheet(from A2 cell to F2 cell collect all the data)
def authenticate():
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    return service

def get_data(spreadsheet_id, range_name):
    service = authenticate()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    return values

def email(subject, html_text, to_email):
    from_email = os.getenv("Email_Address")
    password = os.getenv("generated_app_password_gmail")
    m = MIMEMultipart("alternative")
    m["Subject"] = subject
    m["From"] = from_email
    m["To"] = to_email

    html = MIMEText(html_text, "html")
    m.attach(html)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, password)
        server.sendmail(from_email, to_email, m.as_string())

def fetch_data_and_start_notifications():
    # to get the GitHub data
    github_token = os.getenv("GitHub_Token")
    g = Github(github_token)
    user = g.get_user()
    repo = user.get_repo("order-of-north-platform")
    issues = repo.get_issues()
    filter_issues = [issue for issue in issues if issue.pull_request is None]
    pull_requests = repo.get_pulls()

    github_issues_html = ""
    for issue in filter_issues:
        issue_state = issue.state.lower() 
        if issue_state == "open":
            issue_color = "#FFA500" 
        elif issue_state == "closed":
            issue_color = "#4CAF50"  
        else:
            issue_color = "#888888"

        github_issues_html += f"""
        <li style="font-size: 14px; color: #555555; padding: 10px; background-color: #f9f9f9; margin-bottom: 10px; border-radius: 5px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);">
          <strong>Issue:</strong> <span style="color: {issue_color}; font-weight: bold;">"{issue.title}"</span><br>
          <span style="font-weight: bold;">Opened by:</span> @{issue.user.login}<br>
          <span style="font-weight: bold;">Status:</span> <span style="color: {issue_color}; font-weight: bold;">{issue_state.capitalize()}</span>
        </li>
        """

    github_pulls_html = ""
    for pr in pull_requests:
        pr_state = pr.state.lower() 
        if pr_state == "open":
            pr_color = "#FFA500" 
        elif pr_state == "closed":
            pr_color = "#4CAF50"  
        else:
            pr_color = "#888888"  

        github_pulls_html += f"""
        <li style="font-size: 14px; color: #555555; padding: 10px; background-color: #f9f9f9; margin-bottom: 10px; border-radius: 5px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);">
          <strong>Pull Request:</strong> <span style="color: {pr_color}; font-weight: bold;">"{pr.title}"</span><br>
          <span style="font-weight: bold;">Opened by:</span> @{pr.user.login}<br>
          <span style="font-weight: bold;">Status:</span> <span style="color: {pr_color}; font-weight: bold;">{pr_state.capitalize()}</span>
        </li>
        """
    # to get the sheet data 
    sheet_data = get_data(SPREADSHEET_ID, RANGE_NAME)

    google_sheets_html = ""
    for row in sheet_data:
      task_name = row[0]  
      task_priority = row[1]
      task_owner = row[2]
      task_status = row[3]  
      task_start_date = row[4]
      task_end_date = row[5]  

      # Give colors to task status
      if task_status.lower() == "completed":
        status_color = "#4CAF50"  # green for Completed
      elif task_status.lower() == "in progress":
        status_color = "#FFA500"  # orange for In Progress
      elif task_status.lower() == "blocked":
        status_color = "#FF5722"  # red for Blocked
      else:
        status_color = "#888888"  # gray for other statuses

      google_sheets_html += f"""
     <li style="font-size: 14px; color: #555555; padding: 10px; background-color: #f9f9f9; margin-bottom: 10px; border-radius: 5px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);">
       <strong><span style="color: black;">Task: {task_name}</span></strong><br>
       <span style="color: #FFA500; font-weight: bold;">Priority: </span>{task_priority}<br>
       <span style="font-weight: bold;">Owner: </span>{task_owner}<br>
       <span style="color: #4CAF50; font-weight: bold;">Start Date: </span>{task_start_date}<br>
       <span style="font-weight: bold;">Status: </span><span style="color: {status_color}; font-weight: bold;">{task_status}</span><br>
       <span style="color: #ff5722; font-weight: bold;">End Date:</span> {task_end_date}
     </li>
     """
      html_text = f"""
      <html>
       <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
        <div style="max-width: 600px; margin: 40px auto; background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); border-top: 4px solid #4CAF50;">
          <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="font-size: 24px; color: #333333; margin-bottom: 5px;">Activity Summary</h1>
            <p style="font-size: 14px; color: #888888; margin: 0;">Your GitHub & Task Management Updates</p>
          </div>

          <div style="margin-bottom: 30px;">
            <h3 style="color: #333; font-size: 18px; margin-bottom: 15px; border-bottom: 2px solid #eeeeee; padding-bottom: 8px;">GitHub Issues</h3>
            <ul style="list-style: none; padding: 0;">
              {github_issues_html}
            </ul>
          </div>

          <div style="margin-bottom: 30px;">
            <h3 style="color: #333; font-size: 18px; margin-bottom: 15px; border-bottom: 2px solid #eeeeee; padding-bottom: 8px;">GitHub Pull Requests</h3>
            <ul style="list-style: none; padding: 0;">
              {github_pulls_html}
            </ul>
          </div>

          <div style="margin-bottom: 30px;">
            <h3 style="color: #333; font-size: 18px; margin-bottom: 15px; border-bottom: 2px solid #eeeeee; padding-bottom: 8px;">Task Management</h3>
            <ul style="list-style: none; padding: 0;">
              {google_sheets_html}
            </ul>
          </div>

          <div style="text-align: center; font-size: 12px; color: #999999;">
            <p style="margin: 0; line-height: 1.5;">You can Add, Remove, and Modify Tasks in Google Sheets.</p>
            <p style="margin: 0; line-height: 1.5;">This is an automated email. Please do not reply.</p>
          </div>
        </div>
       </body>
     </html>
     """

    to_email = os.getenv("To_Email_Address")
    email("Github and Task Management Updates", html_text, to_email)
    print("\n>> Email sent successfully")

logging.basicConfig(level=logging.INFO)

scheduler = BlockingScheduler()
fetch_data_and_start_notifications()

scheduler.add_job(fetch_data_and_start_notifications, 'interval', minutes=1)
scheduler.start() 
