import imaplib
import email
from email.header import decode_header
import os

def cre():
    IMAP_SERVER = "imap.gmail.com"
    EMAIL_USER = "nalajalapinky@gmail.com"
    EMAIL_PASS = "rswo cidh hjti ympk"

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")

    status, messages = mail.search(None, 'ALL')  
    email_ids = messages[0].split()

    emails = []  

    for eid in email_ids:
        status, msg_data = mail.fetch(eid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(msg["Subject"])[0]
        subject = subject.decode(encoding if encoding else "utf-8") if isinstance(subject, bytes) else subject
        sender = msg.get("From")
        body = ""
        filepath = ""

        for part in msg.walk():
            if part.get_content_type() == "text/plain" and not part.get("Content-Disposition"):
                body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
            if "attachment" in str(part.get("Content-Disposition", "")):
                filename = part.get_filename()
                if filename:
                    decoded_filename, enc = decode_header(filename)[0]
                    filename = decoded_filename.decode(enc or "utf-8") if isinstance(decoded_filename, bytes) else decoded_filename
                    filepath = os.path.join("attachments", filename)
                    os.makedirs("attachments", exist_ok=True)
                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(decode=True))

        emails.append((eid.decode(), sender, subject, body, filepath))

    return emails if emails else None
