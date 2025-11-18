import resend
from config import settings

resend.api_key = settings.RESEND_KEY

def send_2fa_email(to: str, code: str) -> bool:
    params: resend.Emails.SendParams = {
    "from": "SecureBanking <securebankingAAU@mail.aau-projekt.dk>",
    "to": to,
    "subject": "2FA code - SecureBanking AAU",
    "html": f"<h1> SecureBanking AAU</h1> <p>Your 2FA code is: {code}</p>"
    }
    try:
        resend.Emails.send(params)
        return True
    except:
        return False