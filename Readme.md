# **Auto GitOps**

## 📜 **Introduction**

Welcome to **Auto GitOps**! If you're tired of constantly switching between GitHub and your task management tools, trying to stay on top of issues, pull requests, and tasks, this is the project for you! **Auto GitOps** automates your workflow, keeping you updated on GitHub activities and task progress in a streamlined, efficient manner. 

With this project, you’ll receive real-time email notifications about task updates, GitHub issues, and pull requests. Plus, all task data can be managed easily via a **Google Sheets** file — no complex configuration needed.

## 💡 **What Does It Do?**

- **Automated Task Tracking**: Get notifications about your tasks, whether they are in progress, completed, or blocked. The system keeps track of task statuses and sends you email updates whenever there’s a change.
  
- **GitHub Issue & Pull Request Management**: It fetches data from your GitHub repositories, keeping you informed about the status of open issues and pull requests. Never miss an update or forget to handle a task!

- **Customizable Task Management via Google Sheets**: The configuration is simple! You just use a Google Sheets file to define tasks, their priorities, owners, statuses, and other information. You won’t need to write any code to adjust your task system.

- **Real-Time Email Notifications**: Receive email alerts that summarize your GitHub activities and task statuses. All notifications are delivered straight to your inbox, so you don’t have to check multiple tools to stay up-to-date.

## ⚙️ **Tech Stack**

Here's a quick overview of the technologies that power Auto GitOps:

- **Python**: Used for the backend automation of fetching GitHub issues/pull requests and managing task notifications.
- **GitHub API**: To fetch GitHub issues and pull requests, automate label management, and track the status of PRs.
- **Google Sheets API**: For managing tasks and their associated data (priority, owner, status, etc.).
- **SMTP/Email Services**: For sending email notifications when tasks are updated or when there’s activity on your GitHub repo.
- **Environment Variables**: For securely storing sensitive information such as your email credentials, GitHub token, and Google Sheets credentials.

## 📝 **How It Works**

### **1. Fetch GitHub Data**  
The program fetches data from your GitHub repository using the GitHub API. It retrieves the list of open issues and pull requests, their statuses, and any associated labels.

### **2. Fetch Google Sheets Data**  
It pulls the task data from a predefined Google Sheets file. Each task in the sheet has a name, priority, owner, status (e.g., "Completed," "In Progress," "Blocked"), and start/end dates. The data is displayed in a clean, readable format for you to track.

### **3. Send Email Notifications**  
Once the GitHub and Google Sheets data is fetched, it’s formatted into an email-friendly HTML format. This email is then sent to your specified email address, summarizing all the relevant information. Every time a task status or GitHub activity changes, you get notified!

### **4. Automatic Scheduling**  
The script runs periodically (every minute) and automatically checks for updates. If there’s a change in GitHub issues or pull requests, or if a task status changes in Google Sheets, you will receive a fresh notification.

## 📥 **Requirements**

Before running Auto GitOps, make sure you have the following installed:

- Python 3.x
- Google Sheets API credentials (Service Account file)
- GitHub personal access token (for API access)
- SMTP email credentials (for sending email notifications)

### **Install Dependencies**  
You can easily install the necessary dependencies with pip by running:

```bash
pip install -r requirements.txt
```

Make sure to create a `.env` file to securely store your sensitive information like your Google Sheets credentials, GitHub token, and email settings. Here's an example of the structure:

```env
Service_Account_File=path/to/your/service/account/file.json
Spreadsheet_Id=your_google_sheet_id
GitHub_Token=your_github_personal_access_token
Email_Address=your_email@gmail.com
generated_app_password_gmail=your_gmail_app_password
To_Email_Address=email_to_receive_notifications@example.com
```

## 🚀 **Getting Started**

### 1. **Set Up Your Google Sheets**
- Create a Google Sheet with the following columns:
  - Task Name
  - Priority
  - Task Owner
  - Task Status (e.g., "In Progress," "Completed," "Blocked")
  - Start Date
  - End Date
- Share the Google Sheet with the service account email listed in your `Service_Account_File`.

### 2. **Set Up Your GitHub Repository**
- Create a personal access token for GitHub with permissions to access your repositories (issues and pull requests).
- Replace `your_github_personal_access_token` with the actual token in your `.env` file.

### 3. **Run the Script**
To start the process, run the script by executing:

```bash
python your_script_name.py
```

The program will begin fetching data, processing it, and sending you email notifications.

### 4. **Schedule It to Run Automatically**
You can use a task scheduler like **cron** (Linux/Mac) or **Task Scheduler** (Windows) to run the script at intervals (every minute, for example).

Alternatively, if you're on Linux or macOS, you can use **systemd** to run the script as a service in the background.

## 📧 **Notification Example**

When you run the program, you will receive an email with the following summary:

- **GitHub Issues**: A list of open issues and pull requests.
- **Task Management**: Your current task statuses, priorities, and other details.

The email will look something like this:

---

**Subject:** GitHub and Task Management Updates

**Body:**  
**GitHub Issues**  
- Issue 1: "Task A" - Open, Assigned to @developer  
- Issue 2: "Bug Fix" - Closed, Resolved by @developer

**Task Management**  
- Task A: Priority: High, Status: In Progress, Owner: @developer

---

## 🔧 **Customizing the Workflow**

You can easily customize the workflow by editing the **Google Sheets** to update task data, or modify the GitHub repository to add new issues/PRs. You can even change the email content in the script to match your needs.

## 📝 **Conclusion**

**Auto GitOps** is here to simplify task tracking and GitHub management. Whether you're working solo or collaborating with a team, it keeps you updated without the extra manual work. If you want a more efficient and automated way to stay on top of your tasks and GitHub activities, give this project a try!

Feel free to fork this project, modify it, or contribute. If you have any questions or suggestions, don’t hesitate to reach out!
