
### Step 1: Launch an EC2 Instance
1. **Log in to the AWS Management Console** and navigate to the EC2 Dashboard.
2. **Click "Launch Instance"**.
3. **Choose an Amazon Machine Image (AMI)**: Select an Ubuntu Server AMI.
4. **Choose an Instance Type**: Select a t2.micro instance (free tier eligible).
5. **Configure Instance Details**: Default settings are usually fine.
6. **Add Storage**: Default settings are usually fine.
7. **Add Tags**: Optional.
8. **Configure Security Group**:
   - Add a rule to allow HTTP traffic (port 80).
   - Add a rule to allow SSH traffic (port 22).
9. **Review and Launch**: Launch the instance and download the key pair (.pem file).

### Step 2: Connect to Your EC2 Instance
1. **Open your terminal**.
2. **Change the permissions of your key pair file**:
   ```bash
   chmod 400 your-key-pair.pem
   ```
3. **Connect to your instance**:
   ```bash
   ssh -i "your-key-pair.pem" ubuntu@your-ec2-instance-public-dns
   ```

### Step 3: Set Up Your Environment
1. **Update the package list** and install necessary packages:
   ```bash
   sudo apt-get update
   sudo apt-get install python3-pip python3-venv nginx git
   ```

2. **Clone your project repository**:
   ```bash
   git clone your_repository_url
   cd your_project_directory
   ```

3. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Step 4: Set Up Gunicorn
1. **Install Gunicorn**:
   ```bash
   pip install gunicorn
   ```

2. **Create a Gunicorn service file** to run your application:
   ```bash
   sudo nano /etc/systemd/system/your_project.service
   ```

3. **Add the following content** (adjust paths and app module accordingly):
   ```ini
   [Unit]
   Description=Gunicorn instance to serve your_project
   After=network.target

   [Service]
   User=ubuntu
   Group=www-data
   WorkingDirectory=/home/ubuntu/your_project_directory
   Environment="PATH=/home/ubuntu/your_project_directory/venv/bin"
   ExecStart=/home/ubuntu/your_project_directory/venv/bin/gunicorn --workers 3 --bind unix:your_project.sock -m 007 wsgi:app

   [Install]
   WantedBy=multi-user.target
   ```

4. **Start and enable the Gunicorn service**:
   ```bash
   sudo systemctl start your_project
   sudo systemctl enable your_project
   ```

### Step 5: Configure Nginx
1. **Create an Nginx configuration file**:

```bash
Copy code
sudo nano /etc/nginx/sites-available/your_project
```

2. **Add the following content** (replace your_domain_or_public_ip with your domain or public IP):
```nginx
Copy code
server {
    listen 80;
    server_name your_domain_or_public_ip;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/your_project_directory/your_project.sock;
    }
}
```

3. **Enable the Nginx configuration** and restart the service:
   ```bash
   sudo ln -s /etc/nginx/sites-available/your_project /etc/nginx/sites-enabled
   sudo systemctl restart nginx
   ```

### Step 6: Set Up Firewall Rules
1. **Configure the firewall to allow HTTP traffic** (if using `ufw`):
   ```bash
   sudo ufw allow 'Nginx Full'
   sudo ufw enable
   ```

### Step 7: Test Your Application
1. **Visit your EC2 instance’s public IP or domain** in a web browser to see if your application is running.

2. **Check Gunicorn and Nginx logs** if you encounter issues:
   - **Gunicorn logs** (if configured):
     ```bash
     sudo journalctl -u your_project
     ```
   - **Nginx logs**:
     ```bash
     sudo tail -f /var/log/nginx/error.log
     sudo tail -f /var/log/nginx/access.log
     ```

### Summary
- **Launch** an EC2 instance on AWS.
- **Connect** to your instance via SSH.
- **Set up** your Python environment and install dependencies.
- **Configure** Gunicorn to serve your application.
- **Set up** Nginx as a reverse proxy to forward requests to Gunicorn.
- **Adjust** firewall rules and test your application.

This manual approach gives you more control over the deployment process and is useful for learning and troubleshooting.
