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
RANGE_NAME = "Sheet1!A2:F15" 
# Adjust this for the range you need from the Google Sheet(from A2 cell to F15 cell collect all the data)
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
    m["To"] = ', '.join(to_email)

    html = MIMEText(html_text, "html")
    m.attach(html)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, password)
        server.sendmail(from_email, to_email, m.as_string())

def fetch_data_and_start_notifications():
    github_token = os.getenv("GitHub_Token")
    g = Github(github_token)
    user = g.get_user()
    repo_names = ["order-of-north-platform", "Python-_automation_projects", "python-for-devops", "Auto_GitOps"]
    # to collect issues and pr's from multiple repositories
    github_issues_html = ""
    github_pulls_html = ""

    for repo_name in repo_names:
        repo = user.get_repo(repo_name)
        issues = repo.get_issues()
        filter_issues = [issue for issue in issues if issue.pull_request is None]
        pull_requests = repo.get_pulls()

        for issue in filter_issues:
            issue_state = issue.state.lower()
             # this is a ternary expression or ternary conditional operator
            issue_color = "#078ee0" if issue_state == "open" else "#4CAF50" if issue_state == "closed" else "#888888"

            github_issues_html += f"""
            <li style="font-size: 14px; color: #555555; padding: 10px; background-color: #f9f9f9; margin-bottom: 10px; border-radius: 5px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);">
              <strong>Repository:</strong> <span style="color: Black; font-weight: bold;">"{repo.name}"</span><br>
              <strong>Issue:</strong> <span style="color: #FFA500; font-weight: bold;">"{issue.title}"</span><br>
              <strong>Description:</strong> <span style="color: black; font-weight: bold;">"{issue.body}"</span><br>
              <strong>Issue number:</strong> <span style="color: black; font-weight: bold;">"{issue.number}"</span><br>
              <span style="font-weight: bold;">Opened by:</span> @{issue.user.login}<br>
              <span style="font-weight: bold;">Status:</span> <span style="color: {issue_color}; font-weight: bold;">{issue_state.capitalize()}</span>
            </li>
            """
        for pr in pull_requests:
            pr_state = pr.state.lower()
            pr_color = "#078ee0" if pr_state == "open" else "#4CAF50" if pr_state == "closed" else "#888888"

            github_pulls_html += f"""
            <li style="font-size: 14px; color: #555555; padding: 10px; background-color: #f9f9f9; margin-bottom: 10px; border-radius: 5px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);">
              <strong>Source Repository:</strong> <span style="color: #4c7028; font-weight: bold;">"{pr.head.repo.name}"</span><br>
              <strong>Target Repository:</strong> <span style="color: #132700; font-weight: bold;">"{pr.base.repo.name}"</span><br>
              <strong>Pull Request:</strong> <span style="color: #FFA500; font-weight: bold;">"{pr.title}"</span><br>
              <strong>Description:</strong> <span style="color: black; font-weight: bold;">"{pr.body}"</span><br>
              <strong>Pr number:</strong> <span style="color: black; font-weight: bold;">"{pr.number}"</span><br>
              <span style="font-weight: bold;">Opened by:</span> @{pr.user.login}<br>
              <span style="font-weight: bold;">Status:</span> <span style="color: {pr_color}; font-weight: bold;">{pr_state.capitalize()}</span>
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

            <!-- Task updates and footer -->
        </div>
    </body>
    </html>
    """
    sheet_data = get_data(SPREADSHEET_ID, RANGE_NAME)

    google_sheets_html = ""
    for row in sheet_data:
      task_name = row[0]  
      task_priority = row[1]
      task_assignee = row[2]
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

    # -------Give color to task priority--------
      if task_priority.lower() == "normal":
        priority_color = "#5ead11"
      elif task_priority.lower() == "highest":
        priority_color = "#f3270d"
      elif task_priority.lower() == "high":
        priority_color = "#f5b306"
      elif task_priority.lower() == "low":
        priority_color = "#45aff1"
      elif task_priority.lower() == "lowest":
        priority_color = "#7698ad"
      else:
        priority_color = "#888888"

      google_sheets_html += f"""
     <li style="font-size: 14px; color: #555555; padding: 10px; background-color: #f9f9f9; margin-bottom: 10px; border-radius: 5px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);">
       <strong><span style="color: black;">Task: {task_name}</span></strong><br>
       <span style="color: #813b7d; font-weight: bold;">Priority: </span><span style="color: {priority_color}; font-weight: bold;">{task_priority}</span><br>
       <span style="font-weight: bold;">Assignee: </span>{task_assignee}<br>
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
            <h3 style="color: #333; font-size: 18px; margin-bottom: 15px; border-bottom: 2px solid #eeeeee; padding-bottom: 8px;">Task Updates</h3>
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

    to_email = os.getenv("To_Email_Address").split(',')
    email("Github and Task Management Updates", html_text, to_email)
    print("\n>> Email sent successfully")

logging.basicConfig(level=logging.INFO)

scheduler = BlockingScheduler()
fetch_data_and_start_notifications()
# specify the time when will be the email sent again 
specified_time = 30
# calls the function in specified time intervals
scheduler.add_job(fetch_data_and_start_notifications, 'interval', minutes=specified_time)
scheduler.start() 
