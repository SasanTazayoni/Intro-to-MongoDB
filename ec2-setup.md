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

A key pair is used to securely SSH into your instance. For a deeper explanation of how SSH keys work, see the [DataCamp SSH Keys tutorial](https://www.datacamp.com/tutorial/ssh-keys). In the left-hand menu, navigate to **Network & Security → Key Pairs**.

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

Scroll down to **Instance Type** and select **t3.micro**.

---

## 5. Configure Network Settings

Scroll down to **Network Settings** and click **Edit**. Give the security group a descriptive name.

![Edit Network Settings](images/edit-network-settings.png)

![Security Group Name](images/security-group-name.png)

Click **Add Security Group Rule** and configure it as follows:

- **Port range:** 80
- **Source:** 0.0.0.0/0 *(allows public HTTP access — for this project only)*

![Security Group Rules](images/security-group-rules.png)

> **What is a security group?**
> A security group is a virtual firewall that controls what traffic is allowed in and out of your EC2 instance. By default, all inbound traffic is blocked — you have to explicitly open ports.
>
> **What is port 80?**
> Port 80 is the standard port for HTTP (unencrypted web traffic). When you visit `http://some-ip-address` in a browser, your browser sends the request to port 80 on that server.
>
> **What does `0.0.0.0/0` mean?**
> This is CIDR notation meaning "any IP address anywhere on the internet". Combined with port 80, this rule says: *allow any browser from anywhere to make an HTTP request to this server*. For a production app you would typically restrict this further, but for this project it is fine.
>
> The existing **SSH rule (port 22)** was added automatically when you created the instance. It allows you to connect to the server remotely from your terminal using your key pair.

---

## 6. Storage and Advanced Details

Scroll down to **Configure Storage** — leave the defaults as they are.

Scroll down to **Advanced Details** — leave everything blank.

---

## 7. Select Key Pair and Launch

Scroll down to **Key Pair (login)** and select the key pair you created earlier.

![Appropriate Key Pair](images/appropriate-key-pair.png)

Review the summary on the right, then click **Launch Instance**.

![Preview](images/preview.png)

Once created, click the link in the success message to go to the instance dashboard.

![Create Instance Success](images/create-instance-success.png)

---

## 8. Connect via SSH

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

> **Why `chmod 400`?**
> `chmod` changes file permissions. `400` means the file is readable only by you, and no one else can touch it. SSH is strict about this — it will refuse to use a private key that is readable by other users because a world-readable key is considered insecure. You only need to run this once.

Then connect to your instance using the SSH command shown on the instructions page:

```bash
ssh -i "your-key-pair-name.pem" ubuntu@<your-public-ip>
```

> **Breaking down the SSH command:**
> - `ssh` — the Secure Shell program, which opens an encrypted remote terminal session.
> - `-i "your-key-pair-name.pem"` — tells SSH which private key to use for authentication. The server holds the matching public key (AWS put it there when you launched the instance), so only someone with this `.pem` file can log in.
> - `ubuntu` — the default username on Ubuntu EC2 instances.
> - `@<your-public-ip>` — the IP address of your server.

When prompted with a host authenticity warning, type `yes` and press Enter to authorise the login.

> This warning appears the first time you connect. SSH is telling you it has never seen this server before and is asking you to confirm you trust it. Once you say yes, the server's fingerprint is saved locally so you are not prompted again.

Verify the connection with:

```bash
whoami
```

You should see `ubuntu` printed in the console.

---

## 9. Install and Verify Nginx

> **What is Nginx?**
> Nginx (pronounced "engine-x") is a web server — a program that runs on your EC2 instance and listens for incoming HTTP requests. When a browser navigates to your server's IP address, it sends an HTTP request to port 80. Nginx receives that request and sends back a response (an HTML page, a file, a forwarded API call, etc.).
>
> Nginx is extremely common in production because it is fast, handles many simultaneous connections efficiently, and can also act as a **reverse proxy** (sitting in front of an app like a Node.js server and forwarding requests to it).

Run the following commands in sequence:

```bash
sudo apt update -y       # refreshes the package list from Ubuntu's repositories
sudo apt upgrade -y      # upgrades all installed packages to their latest versions
sudo apt install nginx -y  # installs the Nginx web server
sudo systemctl status nginx  # confirms Nginx is active and running
```

> **What each command does:**
> - `sudo` — runs the command as a superuser (administrator). Most system-level changes require this.
> - `apt update` — syncs your local list of available packages with Ubuntu's remote repositories. This does not install anything — it just updates what your system knows is available.
> - `apt upgrade` — installs the latest versions of all already-installed packages. Good practice before adding new software.
> - `apt install nginx` — downloads and installs Nginx. After installation, Ubuntu automatically starts it and configures it to start on every reboot.
> - `systemctl status nginx` — queries **systemd** (Ubuntu's service manager) for the current status of Nginx. You want to see `active (running)`.
>
> **How the full picture works:**
> 1. Your browser sends an HTTP request to `http://<your-public-ip>` (port 80).
> 2. The EC2 security group rule you created allows that traffic through.
> 3. The request reaches the instance and is received by Nginx.
> 4. Nginx serves back a response — at this point, the default welcome page.
>
> Later, you would configure Nginx to serve your actual application instead of the default page (by editing files in `/etc/nginx/`), or set it up as a reverse proxy that forwards requests to a Node/Python/other backend running on a different port.

You should see the Nginx service reported as **active (running)**.

![Running](images/running.png)

Return to the instance dashboard and copy the **Public IPv4 address**. Paste it into your browser — make sure the URL starts with `http://` not `https://` (some browsers add the `s` automatically).

> If your browser silently upgrades to `https://`, the request will fail because you have not configured an SSL certificate. Either force `http://` in the address bar, or temporarily try a different browser.

You should see the default Nginx welcome page, confirming the server is live.

![Nginx](images/nginx.png)
