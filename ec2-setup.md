# Setting Up an EC2 Instance on AWS

Amazon EC2 (Elastic Compute Cloud) lets you rent virtual servers in the cloud. This guide walks through launching an Ubuntu instance and serving a web page via Nginx.

---

## 1. Sign In

Sign in to the AWS Management Console with your credentials.

![Sign In](images/sign-in.png)

---

## 2. Select a Region

Once signed in, select the appropriate regional server from the top-right dropdown. Choose the region closest to your users for the best performance.

![Choose Server](images/choose-server.png)

---

## 3. Create a Key Pair

A key pair is used to securely SSH into your instance. In the left-hand menu, navigate to **Network & Security → Key Pairs**.

![Key Pairs Menu](images/key-pairs-menu.png)

Click **Create Key Pair**.

![Create Key Pair Button](images/create-key-pair-button.png)

Give the key pair a name and leave the default settings, then click **Create**.

![Key Pair Settings](images/key-pair-settings.png)

![Created Key Pair](images/created-key-pair.png)

The `.pem` file will download automatically. Move it to your `.ssh` folder:

```
C:\Users\[your_username]\.ssh\
```

If the `.ssh` folder does not exist, create it manually, then move the `.pem` file into it.

---

## 4. Launch an Instance

In the left-hand menu, navigate to **Instances**.

![New Instance Menu](images/new-instance-menu.png)

Click **Launch Instances**.

![Launch New Instance](images/launch-new-instance.png)

Give your server a name.

![Server Name](images/server-name.png)

Scroll down to **Application and OS Images**, select **Ubuntu**, then change the version to **24.04** from the dropdown and confirm when prompted.

![Ubuntu](images/ubuntu.png)

![Confirm Changes](images/confirm-changes.png)

---

## 5. Configure Network Settings

Scroll down to **Network Settings** and click **Edit**. Give the security group a descriptive name.

![Edit Network Settings](images/edit-network-settings.png)

![Security Group Name](images/security-group-name.png)

Click **Add Security Group Rule** and configure it as follows:

- **Port range:** 80
- **Source:** 0.0.0.0/0 *(allows public HTTP access — for this project only)*

![Security Group Rules](images/security-group-rules.png)

---

## 6. Select Key Pair and Launch

Scroll down to **Key Pair (login)** and select the key pair you created earlier.

![Appropriate Key Pair](images/appropriate-key-pair.png)

Review the summary on the right, then click **Launch Instance**.

![Preview](images/preview.png)

Once created, click the link in the success message to go to the instance dashboard.

![Create Instance Success](images/create-instance-success.png)

---

## 7. Connect via SSH

On the instance dashboard, click the **Connect** button at the top.

![Dashboard](images/dashboard.png)

This opens a connection instructions page. Switch to the **SSH client** tab and keep it open for reference.

![SSH Instructions](images/ssh-instructions.png)

Open **Git Bash** (Windows) and navigate to your `.ssh` folder:

```bash
cd C:/Users/[your_username]/.ssh
```

Confirm your `.pem` file is present:

```bash
ls -a
```

Set the correct permissions on your key file:

```bash
chmod 400 "your-key-pair-name.pem"
```

Then connect to your instance using the SSH command shown on the instructions page:

```bash
ssh -i "your-key-pair-name.pem" ubuntu@<your-public-ip>
```

Verify the connection with:

```bash
whoami
```

You should see `ubuntu` printed in the console.

---

## 8. Install and Verify Nginx

Run the following commands in sequence:

```bash
sudo apt update -y       # refreshes the package list from Ubuntu's repositories
sudo apt upgrade -y      # upgrades all installed packages to their latest versions
sudo apt install nginx -y  # installs the Nginx web server
sudo systemctl status nginx  # confirms Nginx is active and running
```

You should see the Nginx service reported as **active (running)**.

![Running](images/running.png)

Return to the instance dashboard and copy the **Public IPv4 address**. Paste it into your browser — make sure the URL starts with `http://` not `https://` (some browsers add the `s` automatically).

You should see the default Nginx welcome page, confirming the server is live.

![Nginx](images/nginx.png)
