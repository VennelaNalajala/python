from extraction import cre
from attachment import upload_to_s3
from connection import sqlserver

emails = cre()
if emails:
    conn = sqlserver()
    cursor = conn.cursor()

    for eid, sender, subject, body, filepath in emails:
        s3url = upload_to_s3(filepath, "gmailstorage") if filepath else ""
        cursor.execute("""
            INSERT INTO gmailcontent (eid, sender, subject, body, attachments)
            VALUES (?, ?, ?, ?, ?)
        """, (eid, sender, subject, body, s3url))
        print(f" Inserted email {eid}")
    
    conn.commit()
    conn.close()
else:
    print(" No emails found")
