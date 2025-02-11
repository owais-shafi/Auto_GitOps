A step-by-step guide to setting up your Python script as a service using `systemd`.
This for **Linux/Unix based systems**

### 1. **Create the Service File**
First, you'll create a new `systemd` service file that tells the system how to manage your Python script.

1. Open a terminal and create the service file in the `/etc/systemd/system/` directory:
   ```bash
   sudo nano /etc/systemd/system/auto_gitops.service
   ```

2. In the file, add the following configuration:
   ```ini
   [Unit]
   Description=Auto GitOps Script
   After=network.target

   [Service]
   ExecStart=/usr/bin/python3 /path/to/your_script.py
   WorkingDirectory=/path/to/your_project_directory
   StandardOutput=append:/path/to/logs/auto_gitops.log
   StandardError=append:/path/to/logs/auto_gitops_error.log
   Restart=always
   User=your_username

   [Install]
   WantedBy=multi-user.target
   ```

   - **ExecStart**: This is the full path to your Python interpreter and the script you want to run. Replace `/path/to/your_script.py` with the actual path.
   - **WorkingDirectory**: Set this to the directory where your script resides.
   - **StandardOutput** and **StandardError**: These specify where the logs will be written.
   - **Restart=always**: This ensures that the service will automatically restart if it crashes.
   - **User**: Your Linux username under which the service should run.

### 2. **Reload `systemd` to Apply the Changes**
After creating the service file, reload `systemd` so that it recognizes the new service:
```bash
sudo systemctl daemon-reload
```

### 3. **Start the Service**
Now, you can start your Python script as a background service:
```bash
sudo systemctl start auto_gitops.service
```

### 4. **Enable the Service to Start on Boot**
To ensure that the script starts automatically on system startup:
```bash
sudo systemctl enable auto_gitops.service
```

### 5. **Check the Status of the Service**
You can check whether the service is running correctly with:
```bash
sudo systemctl status auto_gitops.service
```

This will show the service's current status, logs, and any potential errors.

### 6. **Check Logs**
To view the logs created by your script, you can check the log files specified in the service file:
```bash
cat /path/to/logs/auto_gitops.log
cat /path/to/logs/auto_gitops_error.log
```

With this setup, your script will run in the background as a systemd service and restart automatically if it stops or if the machine is rebooted. 


## To **stop**, **disable**, or **remove** it entirely, do this:

### 1. **Stop the Service**
If you want to stop the service from running, use the following command:
```bash
sudo systemctl stop auto_gitops.service
```
This will stop the service, but it will still start again on the next boot unless disabled.

### 2. **Disable the Service**
If you want to prevent the service from starting on boot but keep the service file in place, use:
```bash
sudo systemctl disable auto_gitops.service
```
This disables the service, so it won’t run automatically on system startup.

### 3. **Remove the Service Completely**
If you want to completely remove the service, follow these steps:

1. **Stop the service first** (if it's running):
   ```bash
   sudo systemctl stop auto_gitops.service
   ```

2. **Disable the service** (to ensure it doesn't start on boot):
   ```bash
   sudo systemctl disable auto_gitops.service
   ```

3. **Remove the service file**:
   Delete the service file you created:
   ```bash
   sudo rm /etc/systemd/system/auto_gitops.service
   ```

4. **Reload `systemd`** to apply changes:
   After removing the service file, reload `systemd` to ensure it no longer looks for the removed service:
   ```bash
   sudo systemctl daemon-reload
   ```

5. **Check if the service is gone**:
   Finally, verify that the service has been fully removed:
   ```bash
   systemctl list-units --type=service | grep auto_gitops
   ```
   This should return nothing if the service has been completely removed.

Following these steps will allow you to manage the service effectively.