import smtplib
import os
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def _send_email_now(to_email, subject, html_body):
    """
    Ang totoong pagpapadala ng email (synchronous).
    Tinatawag sa loob ng background thread para hindi
    ma-block ang main request.
    """

    # I-read ang env vars DITO sa loob ng function —
    # hindi sa module level — para masigurado na
    # naka-load na ang Render environment variables
    GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS", "").strip()
    GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "").strip()

    if not to_email or "@" not in to_email:
        print(f"[EMAIL] Invalid email address: {to_email}")
        return False

    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        print("[EMAIL] ERROR: Walang GMAIL_ADDRESS o GMAIL_APP_PASSWORD sa environment")
        print(f"[EMAIL] GMAIL_ADDRESS set: {bool(GMAIL_ADDRESS)}")
        print(f"[EMAIL] GMAIL_APP_PASSWORD set: {bool(GMAIL_APP_PASSWORD)}")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"FCCI Filipino Community Center <{GMAIL_ADDRESS}>"
        msg["To"] = to_email

        html_part = MIMEText(html_body, "html")
        msg.attach(html_part)

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())

        print(f"[EMAIL] ✅ Successfully sent to {to_email}")
        return True

    except smtplib.SMTPAuthenticationError:
        print(f"[EMAIL] ❌ Authentication failed - check App Password in Render env vars")
        return False
    except smtplib.SMTPException as e:
        print(f"[EMAIL] ❌ SMTP error sending to {to_email}: {e}")
        return False
    except Exception as e:
        print(f"[EMAIL] ❌ Unexpected error sending to {to_email}: {e}")
        return False


def send_email(to_email, subject, html_body):
    """
    Magpadala ng email sa background thread —
    hindi nag-block ang main request.
    """
    thread = threading.Thread(
        target=_send_email_now,
        args=(to_email, subject, html_body),
        daemon=True
    )
    thread.start()
    return True


def send_welcome_email(to_email, full_name, member_id):
    """
    Welcome email kapag na-approve ang applicant.
    """
    subject = "🎉 Welcome to FCCI - You are now an Official Member!"

    html_body = f"""
    <div style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto;padding:20px;">
      <div style="background:linear-gradient(135deg,#00562a,#00a85c);padding:30px;border-radius:16px 16px 0 0;text-align:center;">
        <h1 style="color:#ffffff;margin:0;font-size:24px;">Welcome to FCCI!</h1>
      </div>
      <div style="background:#f4fbf7;padding:30px;border-radius:0 0 16px 16px;border:1px solid #e0f0e5;">
        <p style="font-size:15px;color:#0c2418;">Kumusta <b>{full_name}</b>,</p>
        <p style="font-size:14.5px;color:#3a5045;line-height:1.6;">
          Maligayang pagdating sa <b>Filipino Community Center International (FCCI)</b>!
          Ang iyong registration ay na-approve na, at ikaw ay opisyal nang miyembro ng aming komunidad.
        </p>
        <div style="background:#ffffff;border:1px solid #d5ece0;border-radius:12px;padding:16px 20px;margin:20px 0;">
          <p style="margin:0;font-size:12px;color:#5c8270;text-transform:uppercase;letter-spacing:0.5px;">Your Member ID</p>
          <p style="margin:4px 0 0;font-size:20px;font-weight:700;color:#00562a;">{member_id}</p>
        </div>
        <p style="font-size:14.5px;color:#3a5045;line-height:1.6;">
          Maaari ka nang mag-login sa member portal para tingnan ang iyong profile,
          makipag-ugnayan sa community feed, at marami pang iba.
        </p>
        <p style="font-size:13.5px;color:#5c8270;margin-top:24px;">
          United in Faith, Serving with Love.<br>
          — FCCI Team
        </p>
      </div>
    </div>
    """

    return send_email(to_email, subject, html_body)


def send_payment_confirmation_email(
    to_email, full_name, payment_type,
    amount, receipt_no, payment_date
):
    """
    Payment confirmation email kapag may nabayad.
    """
    subject = f"✅ Payment Received - {payment_type}"

    html_body = f"""
    <div style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto;padding:20px;">
      <div style="background:linear-gradient(135deg,#00562a,#00a85c);padding:30px;border-radius:16px 16px 0 0;text-align:center;">
        <h1 style="color:#ffffff;margin:0;font-size:24px;">Payment Confirmed</h1>
      </div>
      <div style="background:#f4fbf7;padding:30px;border-radius:0 0 16px 16px;border:1px solid #e0f0e5;">
        <p style="font-size:15px;color:#0c2418;">Kumusta <b>{full_name}</b>,</p>
        <p style="font-size:14.5px;color:#3a5045;line-height:1.6;">
          Natanggap namin ang iyong bayad. Salamat sa iyong patuloy na suporta sa FCCI!
        </p>
        <div style="background:#ffffff;border:1px solid #d5ece0;border-radius:12px;padding:18px 20px;margin:20px 0;">
          <table style="width:100%;font-size:13.5px;color:#0c2418;">
            <tr><td style="padding:6px 0;color:#5c8270;">Receipt No.</td><td style="padding:6px 0;text-align:right;font-weight:600;">{receipt_no}</td></tr>
            <tr><td style="padding:6px 0;color:#5c8270;">Payment Type</td><td style="padding:6px 0;text-align:right;font-weight:600;">{payment_type}</td></tr>
            <tr><td style="padding:6px 0;color:#5c8270;">Amount</td><td style="padding:6px 0;text-align:right;font-weight:700;color:#00562a;">₩{amount:,}</td></tr>
            <tr><td style="padding:6px 0;color:#5c8270;">Date</td><td style="padding:6px 0;text-align:right;font-weight:600;">{payment_date}</td></tr>
          </table>
        </div>
        <p style="font-size:13.5px;color:#5c8270;margin-top:24px;">
          United in Faith, Serving with Love.<br>
          — FCCI Team
        </p>
      </div>
    </div>
    """

    return send_email(to_email, subject, html_body)
