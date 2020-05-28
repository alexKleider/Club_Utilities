"""
This code comes from vijay.anand and can be found here:
https://stackoverflow.com/questions/52292971/sending-single-email-with-3-different-attachments-python-3
"""
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import ntpath

sender_address = 'vijay.anand@xxxx.com'
default_subject = 'Test email from {}'.format(sender_address)
smtp_server_address = '10.111.41.25'
smtp_port_number = 25

default_message = message = """<html>
<body>
Attached is the Louisiana Contractors Spreadsheet.
<br><br>

Let me know if you have any questions

</body>
</html>
"""


def send_by_smtp(to=None, cc=None, bcc=None, subject=None, attachments=None, attachment_type='plain'):
    """
        Snippet to send an email to multiple people along with multiple attachments.
        :param to: list of emails
        :param cc: list of emails
        :param bcc: list of emails
        :param subject: Email Subject
        :param attachments: list of file paths
        :param attachment_type: 'plain' or 'html'
        :return: None
    """
    email_from = sender_address
    email_to = list()
    files_to_send = attachments
    msg = MIMEMultipart()
    msg["From"] = email_from
    if to:
        to = list(set(to))
        email_to += to
        msg["To"] = ', '.join(to)
    if cc:
        cc = list(set(cc))
        email_to += cc
        msg["Cc"] = ', '.join(cc)
    if bcc:
        bcc = list(set(bcc))
        email_to += bcc
        msg["Bcc"] = ', '.join(bcc)
    if subject:
        msg["Subject"] = subject
        msg.preamble = subject
    else:
        msg["Subject"] = default_subject
        msg.preamble = default_subject

    body = default_message
    msg.attach(MIMEText(body, attachment_type))

    if files_to_send:
        for file_to_send in files_to_send:
            content_type, encoding = mimetypes.guess_type(file_to_send)
            if content_type is None or encoding is not None:
                content_type = "application/octet-stream"
            maintype, subtype = content_type.split("/", 1)
            if maintype == "text":
                with open(file_to_send) as fp:
                    # Note: we should handle calculating the charset
                    attachment = MIMEText(fp.read(), _subtype=subtype)
            elif maintype == "image":
                with open(file_to_send, "rb") as fp:
                    attachment = MIMEImage(fp.read(), _subtype=subtype)
            elif maintype == "audio":
                with open(file_to_send, "rb")as fp:
                    attachment = MIMEAudio(fp.read(), _subtype=subtype)
            else:
                with open(file_to_send, "rb") as fp:
                    attachment = MIMEBase(maintype, subtype)
                    attachment.set_payload(fp.read())
                encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=ntpath.basename(file_to_send))
            msg.attach(attachment)

    try:
        smtp_obj = smtplib.SMTP(host=smtp_server_address, port=smtp_port_number, timeout=300)
        smtp_obj.sendmail(from_addr=email_from, to_addrs=list(set([email_from] + email_to)), msg=msg.as_string())
        print("Successfully sent email to {}".format(str(email_to)))
        smtp_obj.quit()
        return True
    except smtplib.SMTPException:
        print("Error: unable to send email")
        return False


if __name__ == '__main__':
    print('Send an email using Python')
    result = send_by_smtp(to=['vijay@xxxx.com', 'tha@xxx.com'],
                          cc=['anandp@xxxx.com', 'nitha@xxxx.com'],
                          bcc=['vij@xxxx.com', 'Sun@xxxx.com'],
                          subject='Louisiana Contractors List',
                          attachments=['test.txt', '1.JPG', '2.PNG', '3.PNG', '4.PNG'],
                          attachment_type='html')
    if result:
        print('Email Sent Successfully')
    else:
        print('Email Sending Failed')

