import logging
from data.config import smtpPort, smtpServer
import smtplib
import os
from random import choice
from datetime import datetime

import mimetypes
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(addr_to, msg_subj, msg_text, files, user):
    addr_from = user[0]
    password = user[1]

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = msg_subj

    body = msg_text
    msg.attach(MIMEText(body, 'plain'))

    process_attachement(msg, files)

    # ======== This block is configured for each mail provider separately
    server = smtplib.SMTP_SSL(smtpServer, smtpPort)
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()
    logging.info(f'Successfully send mail from {addr_from} to {addr_to}')
    # ==========================================================================================================================


def process_attachement(msg, files):  # Function for processing the list of files added to the message
    for f in files:
        if os.path.isfile(f):
            attach_file(msg, f)
        elif os.path.exists(f):
            dirs = os.listdir(f)
            for file in dirs:
                attach_file(msg, f + "/" + file)


def attach_file(msg, filepath):  # Function for adding a specific file to a message
    filename = os.path.basename(filepath)
    ctype, encoding = mimetypes.guess_type(filepath)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    with open(filepath, 'rb') as fp:
        file = MIMEBase(maintype, subtype)
        file.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(file)
    file.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(file)


def send_code_confirmation(addr_to, user):
    chars = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-!?'
    code = ''.join([choice(chars) for _ in range(6)])

    now = datetime.now()
    time = "{}.{}.{}  {}:{}".format(str(now.day).rjust(2, '0'),
                                    str(now.month).rjust(2, '0'),
                                    now.year, str(now.hour).rjust(2, '0'),
                                    str(now.minute).rjust(2, '0'))

    send_email(addr_to,
               f'Tg-bot confirmation code {time}',
               f"Your confirmation code: {code}. DON'T TELL IT TO ANYONE",
               [],
               user)
    return code
