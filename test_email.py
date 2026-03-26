#!/usr/bin/env python
"""
Test script to verify email functionality
"""

from dotenv import load_dotenv
import os

def test_email():
    """Test email sending functionality"""
    print("=" * 50)
    print("Email Functionality Test")
    print("=" * 50)

    # Load environment variables
    load_dotenv()

    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    recipient_email = os.getenv('RECIPIENT_EMAIL')
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = os.getenv('SMTP_PORT', '587')

    print(f"Sender Email: {sender_email}")
    print(f"Recipient Email: {recipient_email}")
    print(f"SMTP Server: {smtp_server}:{smtp_port}")

    if not all([sender_email, sender_password, recipient_email]):
        print("\n❌ Missing email configuration in .env file")
        print("Please set: SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL")
        return False

    # Test email send
    try:
        from news_fetcher import send_news_email
        test_content = "This is a test email from Financial News Agent.\n\nIf you receive this, email functionality is working!"
        result = send_news_email(test_content, recipient_email)

        if result:
            print("\n✅ Test email sent successfully!")
            print(f"Check your inbox at {recipient_email}")
            return True
        else:
            print("\n❌ Failed to send test email")
            return False

    except Exception as e:
        print(f"\n❌ Error testing email: {e}")
        return False

if __name__ == '__main__':
    test_email()