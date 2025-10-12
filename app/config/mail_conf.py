from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
from pathlib import Path
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parents[2] / ".env"
print("🧩 env_path:", env_path.exists())  # 파일 있는지
load_dotenv(dotenv_path=env_path)

print("🔑 SENDGRID_API_KEY:", os.getenv("SENDGRID_API_KEY"))
print("📧 SENDER_EMAIL:", os.getenv("SENDER_EMAIL"))


# ✅ .env 파일 경로 지정 (루트에 있을 경우)
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

class MailConfig:
    def __init__(self):
        self.api_key = os.getenv("SENDGRID_API_KEY")
        self.from_email = os.getenv("SENDER_EMAIL")

    def send_mail(self, to_email: str, subject: str, body: str):
        """단순한 메일 발송 메서드"""
        sg = SendGridAPIClient(api_key=self.api_key)
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=subject,
            html_content=body
        )
        try:
            response = sg.send(message)
            print(f"✅ 메일 전송 성공 ({response.status_code})")
            return True, None
        except Exception as e:
            print(f"❌ 메일 전송 실패: {e}")
            return False, str(e)