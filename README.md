📄 README.md
# 🎂 Birthday Message Automator

A **Python desktop application** that automatically sends personalized birthday messages via **Email** (and optionally WhatsApp if running locally).  
Perfect for personal automation, learning Python scripting, or showcasing automation projects in your portfolio.

---

## 🚀 Features

- ✅ View, add, and delete contacts stored in a CSV file
- ✅ Automatically check for birthdays every day
- ✅ Send personalized birthday messages via Email
- ✅ Optional WhatsApp messages via `pywhatkit` (requires local machine and browser)
- ✅ Test message functionality
- ✅ Menu-driven CLI interface for easy usage
- ✅ Can be packaged as a standalone Windows `.exe`

---

## 💻 Requirements

- Python 3.11+
- Windows OS (for `.exe` version)
- Libraries (install with `pip install -r requirements.txt`):
  - `pywhatkit`
  - `pandas`
  - `python-dotenv`
  - `schedule`
- Gmail or SMTP email account

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/birthday-automator.git
cd birthday-automator
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Configure environment variables

Create a .env file (do not commit this to GitHub) with your email credentials:

EMAIL_ADDRESS=your@email.com
EMAIL_PASSWORD=yourpassword
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

Tip: Push .env.example to GitHub instead, with placeholders for safety.

4️⃣ Prepare contacts

Create a contacts.csv file in the same folder:

NAME,PHONE,EMAIL,DOB
John Doe,+1234567890,john@example.com,1990-01-01
🖥 Usage
Run as Python Script
python main.py

Navigate the menu to:

View/Add/Delete contacts

Test messages

Check today’s birthdays

Start the auto-scheduler

Run as Windows Executable (.exe)

Build .exe using PyInstaller:

python -m PyInstaller --onefile --console main.py

Place main.exe, .env, and contacts.csv in the same folder.

Double-click main.exe to start.

📝 Notes

WhatsApp messages require local browser login via QR code (only works with Python script, not automated on VPS or headless servers).

Email automation works standalone, on any Windows machine.

.exe deployment allows running the app without Python installed.

📂 Folder Structure
BirthdayBot/
├── main.exe          # Optional Windows executable
├── main.py           # Python script
├── contacts.csv      # CSV contact database
├── .env              # Local email credentials (do NOT push)
├── .env.example      # Placeholder for GitHub
├── requirements.txt  # Python dependencies
├── README.md         # Project description
💎 Future Enhancements

GUI interface (Tkinter or PyQt)

WhatsApp Cloud API integration for production-ready messaging

Installer (.msi) with shortcuts

Logging of sent messages

Encryption of contact data

📌 Author

Eugene Yarney – Portfolio Project – Personal Automation


---
