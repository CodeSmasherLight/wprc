# WhatsApp Product Review System

This README explains, step by step, how to run and verify the complete project exactly the way it was built by me, keeping the setup process as clear and practical as possible. It follows the same sequence you would use on a fresh machine.

dont mind any typo.

---

## Architecture overview
<img width="4976" height="2364" alt="Untitled-2025-11-17-0116" src="https://github.com/user-attachments/assets/c1367dd0-271b-47a2-bf86-a56769db55ea" />

WhatsApp → Twilio → Ngrok → FastAPI → PostgreSQL → React UI

The system uses Twilio as a webhook relay, meaning no Twilio credentials are used in code. Twilio simply forwards messages to our backend and delivers responses back to the user.

# Backend Setup

## 1. Get backend code

Clone or download the repository and navigate into the backend folder, i would advise to open VSCode inside the backend folder, not the whole project as it was causing some issues with environment detection.

```bash
cd backend
```

---

## 2. Create virtual environment

Inside the backend folder, create a virtual environment:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

You should now see `(venv)` in your terminal.

---

## 3. Install requirements

Install all Python dependencies:

```bash
pip install -r requirements.txt
```

---

## 4. Database: Setup local PostgreSQL using pgAdmin4

1. Install PostgreSQL and pgAdmin4.
2. Open pgAdmin4.
3. Create a new database (example name: `wprc_db`).
4. Right click the database → Properties → copy connection details.

Your database URL will look like:

```
postgresql://postgres:YOUR_PASSWORD@localhost:5432/wprc_db
```

Add this value into `.env` file inside backend folder:

```
DATABASE_HOSTNAME=localhost 
DATABASE_PORT=5432
DATABASE_PASSWORD=your_password_here       
DATABASE_NAME=wprc_db           
DATABASE_USERNAME=postgres
```

---

## 5. Redis Setup (using WSL as i found it easier)

### Install WSL

Open PowerShell as Administrator and run:

```bash
wsl --install
```

Restart the system. Open Ubuntu and create username & password.

Update packages:

```bash
sudo apt update && sudo apt upgrade -y
```

### Install Redis

```bash
sudo apt install redis-server -y
sudo service redis-server start
```

Test Redis:

```bash
redis-cli ping
```

Response should be:

```
PONG
```

Add Redis URL to `.env` file:

```
redis_url=redis://localhost:6379/0
```

---

## 6. Ngrok Setup

1. Install ngrok from Microsoft Store.
2. Create an ngrok account and copy your auth token.

Run in PowerShell:

```bash
ngrok config add-authtoken YOUR_NGROK_TOKEN
```

Then start tunnel:

```bash
ngrok http 8000
```

You will see output similar to:

```
Forwarding https://abcd-1234.ngrok-free.app -> http://localhost:8000
```

copy HTTPS URL shown after "Forwarding", it will be used in Twilio setup.

![alt text](<Screenshot 2025-11-20 212636.png>)

---

## 7. Twilio WhatsApp Setup

1. Sign in to Twilio dashboard.
2. Navigate to:
   Messaging → Try it out → Send a WhatsApp message
3. Scan QR code and send join message from WhatsApp to connect sandbox.

Now go to:
Sandbox Settings

In "When a message comes in", paste your ngrok URL with `/webhook` endpoint:

```
https://YOUR-NGROK-URL/webhook
```

Set Method: POST

Leave "Status Callback URL" unchanged.

Click Save.

Now from WhatsApp, start messaging:

```
Hi
```

Follow the conversation flow as guided by the bot.

![alt text](<Screenshot 2025-11-20 213548.png>)

---

## 8. Start backend server

Run:

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```
http://localhost:8000
```

---

# Frontend Setup

## 1. Get frontend code

Navigate to frontend folder:

```bash
cd frontend
```

---

## 2. Install requirements

```bash
npm install
```

---

## 3. Run frontend

```bash
npm run dev
```

Open in browser:

```
http://localhost:5173
```

---

## Using the UI

1. Click "Fetch Reviews" to load reviews.
2. Click "Clear" to clear the UI.
3. Reviews appear only when requested, making the UI efficient and controlled.

![alt text](image.png)

---

# Demo Flow

1. Send "Hi" on WhatsApp
2. Provide product name
3. Provide user name
4. Provide review
5. Confirmation message received
6. Open frontend and see the review listed