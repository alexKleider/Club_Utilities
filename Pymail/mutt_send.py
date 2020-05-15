#!/usr/bin/env python3

# File: Pymail/mutt_send.py


def mutt_send(muttrc, recipient, subject, body,
                            attachments=None):
    """
    Does the mass e-mailings with an attachment (if provided.)
    'muttrc' Specify an initialization file to read
    (instead of ~/.muttrc.)
    """
    cmd_args = [ "mutt", "-F", muttrc, ]
    cmd_args.extend(["-s", "{}".format(subject)])
    if attachments:
        list2attach = ['-a']
        if type(attachments) == str:
            list2attach.append(attachments)
        else:
            for path2attach in attachments:
                list2attach.append(path2attach)
        cmd_args.extend(list2attach)
    cmd_args.extend([ "--", recipient])
    p = subprocess.run(cmd_args, stdout=subprocess.PIPE, 
        input=body, encoding='utf-8')
    if p.returncode:
        print("Error: {} ({})".format(
            p.stdout, recipient))

