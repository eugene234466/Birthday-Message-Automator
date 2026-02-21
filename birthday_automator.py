# ============================================================
# BIRTHDAY MESSAGE AUTOMATOR

# ============================================================

import pywhatkit
import smtplib
import schedule
import time
import pandas as pd
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import sys

# ── 1. LOAD ENVIRONMENT VARIABLES ───────────────────────────
load_dotenv()

SENDER_EMAIL    = os.getenv("EMAIL_ADDRESS")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER     = os.getenv("SMTP_SERVER")

try:
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
except ValueError:
    SMTP_PORT = 587

if not all([SENDER_EMAIL, SENDER_PASSWORD, SMTP_SERVER]):
    print("❌ Missing environment variables. Check your .env file.")
    sys.exit(1)

# ── 2. LOAD CONTACTS ────────────────────────────────────────
try:
    contacts = pd.read_csv("contacts.csv")
except FileNotFoundError:
    print("❌ contacts.csv not found.")
    sys.exit(1)

contacts.columns = contacts.columns.str.strip()

required_cols = {"NAME", "PHONE", "EMAIL", "DOB"}
if not required_cols.issubset(set(contacts.columns)):
    print("❌ contacts.csv is missing required columns.")
    sys.exit(1)

contacts["DOB"] = pd.to_datetime(contacts["DOB"], errors="coerce")

# ── 3. MESSAGE TEMPLATE ─────────────────────────────────────
def birthday_message(name):
    return (f"""{name}, today we celebrate YOU. 🎉
Thank you for being an amazing part of my life. I pray this new age brings clarity,
peace, bigger wins, and everything your heart truly desires. 💙""")


# ── 4. SEND WHATSAPP ────────────────────────────────────────
def send_whatsapp(name, phone):
    try:
        if pd.isna(phone) or not str(phone).strip():
            print(f"[WhatsApp] ❌ No phone number for {name}")
            return

        message = birthday_message(name)
        now = datetime.now()
        hour = now.hour
        minute = now.minute + 2

        # Fix minute overflow
        if minute >= 60:
            minute -= 60
            hour += 1

        # Fix hour overflow
        if hour >= 24:
            hour = 0

        pywhatkit.sendwhatmsg(str(phone), message, hour, minute)
        print(f"[WhatsApp] ✅ Sent to {name} ({phone})")

    except Exception as e:
        print(f"[WhatsApp] ❌ Failed for {name}: {e}")


# ── 5. SEND EMAIL ───────────────────────────────────────────
def send_email(name, recipient_email):
    try:
        if pd.isna(recipient_email) or not str(recipient_email).strip():
            print(f"[Email] ❌ No email for {name}")
            return

        message = birthday_message(name)
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient_email
        msg["Subject"] = f"🎂 Happy Birthday {name}!"
        msg.attach(MIMEText(message, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())

        print(f"[Email] ✅ Sent to {name} ({recipient_email})")

    except Exception as e:
        print(f"[Email] ❌ Failed for {name}: {e}")


# ── 6. CHECK BIRTHDAYS ──────────────────────────────────────
def check_birthday():
    today = datetime.now().strftime("%m-%d")
    print("🔍 Checking for birthdays...")

    for _, row in contacts.iterrows():
        if pd.notna(row["DOB"]) and row["DOB"].strftime("%m-%d") == today:
            name  = row["NAME"]
            phone = row["PHONE"]
            email = row["EMAIL"]

            send_whatsapp(name, phone)
            send_email(name, email)

    print("✅ Birthday check completed")


# ── 7. VIEW CONTACTS ────────────────────────────────────────
def view_contacts():
    print("\n📋 All Contacts:")
    print(contacts.to_string(index=False))
    input("\nPress Enter to return to menu...")


# ── 8. ADD CONTACT ──────────────────────────────────────────
def add_contact():
    print("\n➕ Add New Contact:")
    name  = input("Name: ").strip()
    phone = input("Phone (e.g. +1234567890): ").strip()
    email = input("Email: ").strip()
    dob   = input("Date of Birth (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(dob, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        return

    new_row = f"\n{name},{phone},{email},{dob}"

    try:
        with open("contacts.csv", "a") as f:
            f.write(new_row)
    except Exception as e:
        print(f"❌ Failed to write contact: {e}")
        return

    global contacts
    contacts = pd.read_csv("contacts.csv")
    contacts.columns = contacts.columns.str.strip()
    contacts["DOB"] = pd.to_datetime(contacts["DOB"], errors="coerce")

    print(f"✅ {name} added successfully!")
    input("\nPress Enter to return to menu...")


# ── 9. DELETE CONTACT ───────────────────────────────────────
def delete_contact():
    print("\n🗑️ Delete Contact:")
    view_contacts()
    name = input("Enter the name to delete: ").strip()

    global contacts

    if name in contacts["NAME"].values:
        contacts = contacts[contacts["NAME"] != name]
        contacts.to_csv("contacts.csv", index=False)
        print(f"✅ {name} deleted successfully!")
    else:
        print(f"❌ Contact '{name}' not found.")

    input("\nPress Enter to return to menu...")


# ── 10. TEST MESSAGE ────────────────────────────────────────
def test_message():
    print("\n📤 Send Test Message:")
    view_contacts()
    name = input("Enter contact name to test: ").strip()

    row = contacts[contacts["NAME"] == name]
    if row.empty:
        print(f"❌ Contact '{name}' not found.")
        return

    phone = row.iloc[0]["PHONE"]
    email = row.iloc[0]["EMAIL"]

    print("\nSend via:")
    print("  1. WhatsApp")
    print("  2. Email")
    print("  3. Both")
    method = input("Choice (1-3): ").strip()

    if method == "1":
        send_whatsapp(name, phone)
    elif method == "2":
        send_email(name, email)
    elif method == "3":
        send_whatsapp(name, phone)
        send_email(name, email)
    else:
        print("❌ Invalid choice.")

    input("\nPress Enter to return to menu...")


# ── 11. SCHEDULER ───────────────────────────────────────────
def start_scheduler():
    print("\n⏰ Starting Auto Scheduler...")
    print("🔍 Will check birthdays daily at 09:00 AM")
    print("Press Ctrl+C to stop.\n")

    schedule.every().day.at("09:00").do(check_birthday)

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n⛔ Scheduler stopped. Returning to menu...")


# ── 12. MENU ────────────────────────────────────────────────
def display_menu():
    print("""
    ╔══════════════════════════════════╗
    ║   🎂 BIRTHDAY AUTOMATOR MENU    ║
    ╠══════════════════════════════════╣
    ║  1. View All Contacts            ║
    ║  2. Add New Contact              ║
    ║  3. Delete Contact               ║
    ║  4. Check Today's Birthdays      ║
    ║  5. Send Test Message            ║
    ║  6. Start Auto Scheduler         ║
    ║  7. Exit                         ║
    ╚══════════════════════════════════╝
    """)

def run_menu():
    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            view_contacts()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            delete_contact()
        elif choice == "4":
            check_birthday()
        elif choice == "5":
            test_message()
        elif choice == "6":
            start_scheduler()
        elif choice == "7":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-7.")


# ── ENTRY POINT ─────────────────────────────────────────────
if __name__ == "__main__":
    run_menu()