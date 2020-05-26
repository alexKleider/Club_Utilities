#!/usr/bin/env python3

# File Bashmail/send.py

"""
Used to send an email from bash by calling the subprocess module
to call msmtp or mutt (depending if attachments need to be sent.)

Provides send() when imported as a module.
Provides same "send()" functionality as that found in Pymail.send
"""

import time
import subprocess

# Note: the 'To' header is NOT included in the following:
header_keys = ("From", "Sender", "Reply-To",
                 "Cc", "Bcc", "Subject", )

def smtp_send(email, mta):
    """
    WARNING: Can not accommodate attachments!
    First parameter is a dict with keys and values
    specifying an email.  If there are attachments
    a warning is printed and they are NOT sent.
    <mta> specifies which Mail Transfer Agent to use.
    """
    cmd_args = ["msmtp", "-a", mta, "--read-recipients" "--"]
    message = []
    included_keys = email.keys()
    for key in header_keys:
        if key in included_keys:
            message.append("{}: {}".format(key, email[key])
    if message:
        message.append('')
        message = '\n'.join(message)
        message = message + email['body']
    else:
        message = email['body']
    if "attachments" in email and email["attachments"]:
        print("Not configured to send attachments:")
            for attachment in attachments:
                print ("Attachment '{}' is NOT being included."
                    .format(attachment))
    for recipient in email['To:']:
        cmd_args.append(recipient)
    p = subprocess.run(cmd_args, stdout=subprocess.PIPE, 
        input=message, encoding='utf-8')
    if p.returncode:
        print("Error: {} ({})".format(
            p.stdout, recipient))


def mutt_send(email, mta)
    """
    Choose mutt to send email if there are attachments.
    """
    cmd_args = [ "mutt", "-F",
        os.path.expanduser("~/.mutt{}".format(mta)), ]
    cmd_args.extend(["-s", "{}".format(email["subject"])])
    if email["attachments"]:
        list2attach = ['-a']
        for path2attach in email["attachments"]:
            list2attach.append(path2attach)
        cmd_args.extend(list2attach)
        cmd_args.appand("--")
    if type(email['To'])==str:
        cmd_args.append(email['To'])
    else:
        cmd_args.extend(email['To'])
    p = subprocess.run(cmd_args, stdout=subprocess.PIPE, 
        input=body, encoding='utf-8')
    if p.returncode:
        print("Error: {} ({})".format(
            p.stdout, email['To']))

def send_email(email, mta):
    if 'attachments' in email.keys()  # key is there ..
    and email['attachments']:         # and has a value.
        mutt_send(email, mta)
    else:                         # no attachment to include
        msmtp_send(email, mta)


def send(emails, mta, report_progress=True,
                            include_wait=True):
    """
    Sends emails using msmtp.
    <email> is a dict representing an email to be sent.
    Keys, some optional, can be as follows:
    'body': a (possibly empty) string. (optional)
    'attachments': a list (possible empty) of file names. (optional)
    'From', 'Reply-To', 'To', 'Subject', ...
    ...and possibly other commonly used fields defined by rfc5322.
    ...Values are either strings or lists of strings;
    in the latter case the values are converted into a single
    comma separated string.
    """
    ret = []
    counter = 0
    for email in emails:
        if 'attachments' in emails:
            # use mutt:
            pass
        else:
            # use msmtp:
            pass
        recipients = [
            recipient for recipient in email['To'].split(',')]
        keys = [key for key in email.keys()]
        for key in header_keys:
            if key in keys:
                ret.append("{}: {}".format(key, email[key]))
        ret.append('')
        ret.append(email['body']
        if 'attachments' in keys:
            print( "Unable to send attachments by this mechanism.")
            for attachment in email['attachments']:
                print("Attachment '{}' has not been sent to {}."
                    .format(email.attachment, email['To']))
        counter += 1
        print("Sending email #{} to {}."
            .format(counter, ", ".join(email['To'])))
        smtp_send(recipients, '\n'.join(ret))
        if include_wait:
            time.sleep(random.randint(MIN_TIME_TO_SLEEP,
                                    MAX_TIME_TO_SLEEP))

NOTES = """
man msmtp...
MSMTP(1)                                                                      General Commands Manual                                                                     MSMTP(1)

NAME
       msmtp - An SMTP client

SYNOPSIS
       Sendmail mode (default):
              msmtp [option...] [--] recipient...
              msmtp [option...] -t [--] [recipient...]

       Configuration mode:
              msmtp --configure <mailaddress>

       Server information mode:
              msmtp [option...] --serverinfo

       Remote Message Queue Starting mode:
              msmtp [option...] --rmqs=host|@domain|#queue

DESCRIPTION
       In the default sendmail mode, msmtp reads a mail from standard input and sends it to an SMTP server for delivery.
       In server information mode, msmtp prints information about an SMTP server.
       In Remote Message Queue Starting mode, msmtp sends a Remote Message Queue Starting request for a host, domain, or queue to an SMTP server.

EXIT STATUS
       The standard sendmail exit status codes are used, as defined in sysexits.h.

OPTIONS
       Options override configuration file settings.
       They are compatible with sendmail where appropriate.

       General options

              --version
                     Print version information, including information about the libraries used.

              --help Print help.

              -P, --pretend
                     Print the configuration settings that would be used, but do not take further action.  An asterisk (`*') will be printed instead of your password.

              -v, -d, --debug
                     Print  lots  of debugging information, including the whole conversation with the SMTP server. Be careful with this option: the (potentially dangerous) output
                     will not be sanitized, and your password may get printed in an easily decodable format!

       Changing the mode of operation

              --configure=mailaddress
                     Generate a configuration for the given mail address and print it. This can be modified or copied unchanged to the configuration file.  Note  that  this  only
                     works for mail domains that publish appropriate SRV records; see RFC 8314.

              -S, --serverinfo
                     Print  information  about  the  SMTP server and exit. This includes information about supported features (mail size limit, authentication, TLS, DSN, ...) and
                     about the TLS certificate (if TLS is active).

              --rmqs=(host|@domain|#queue)
                     Send a Remote Message Queue Starting request for the given host, domain, or queue to the SMTP server and exit.

       Configuration options

              -C, --file=filename
                     Use the given file instead of ~/.msmtprc or $XDG_CONFIG_HOME/msmtp/config as the user configuration file.

              -a, --account=account_name
                     Use the given account instead of the account named "default". The settings of this account may be changed with command line options. This  option  cannot  be
                     used together with the --host option.

              --host=hostname
                     Use  this SMTP server with settings from the command line; do not use any configuration file data. This option cannot be used together with the --account op‐
                     tion.

              --port=number
                     Set the port number to connect to. See the port command.

              --source-ip=[IP]
                     Set or unset an IP address to bind the socket to. See the source_ip command.

              --proxy-host=[IP|hostname]
                     Set or unset a SOCKS proxy to use. See the proxy_host command.

              --proxy-port=[number]
                     Set or unset a port number for the proxy host. See the proxy_port command.

              --timeout=(off|seconds)
                     Set or unset a network timeout, in seconds. See the timeout command.

              --protocol=(smtp|lmtp)
                     Set the protocol. See the protocol command.

              --domain=[string]
                     Set the argument of the SMTP EHLO (or LMTP LHLO) command. See the domain command.

              --auth[=(on|off|method)]
                     Enable or disable authentication and optionally choose the method.  See the auth command.

              --user=[username]
                     Set or unset the user name for authentication. See the user command.

              --passwordeval=[eval]
                     Evaluate password for authentication. See the passwordeval command.

              --tls[=(on|off)]
                     Enable or disable TLS/SSL. See the tls command.

              --tls-starttls[=(on|off)]
                     Enable or disable STARTTLS for TLS. See the tls_starttls command.

              --tls-trust-file=[file]
                     Set or unset a trust file for TLS. See the tls_trust_file command.

              --tls-crl-file=[file]
                     Set or unset a certificate revocation list (CRL) file for TLS. See the tls_crl_file command.

              --tls-fingerprint=[fingerprint]
                     Set or unset the fingerprint of a trusted TLS certificate. See the tls_fingerprint command.

              --tls-key-file=[file]
                     Set or unset a key file for TLS. See the tls_key_file command.

              --tls-cert-file=[file]
                     Set or unset a cert file for TLS. See the tls_cert_file command.

              --tls-certcheck[=(on|off)]
                     Enable or disable server certificate checks for TLS. See the tls_certcheck command.

              --tls-min-dh-prime-bits=[bits]
                     Set or unset minimum bit size of the Diffie-Hellman (DH) prime. See the tls_min_dh_prime_bits command.

              --tls-priorities=[priorities]
                     Set or unset TLS priorities. See the tls_priorities command.

       Options specific to sendmail mode

              -f, --from=address
                     Set the envelope-from address. It is only used when auto_from is off.
                     If no account was chosen yet (with --account or --host), this option will choose the first account that has the given envelope-from  address  (set  with  the
                     from command). If no such account is found, "default" is used.

              --auto-from[=(on|off)]
                     Enable or disable automatic envelope-from addresses. The default is off.  See the auto_from command.

              --maildomain=[domain]
                     Set the domain part for the --auto-from address. See the maildomain command.

              -N, --dsn-notify=(off|cond)
                     Set or unset DSN notification conditions. See the dsn_notify command.

              -R, --dsn-return=(off|ret)
                     Set or unset the DSN notification amount. See the dsn_return command.  Note that hdrs is accepted as an alias for headers to be compatible with sendmail.

              --add-missing-from-header[=(on|off)]
                     Enable or disable the addition of a missing From header. See the add_missing_from_header command.

              --add-missing-date-header[=(on|off)]
                     Enable or disable the addition of a missing Date header. See the add_missing_date_header command.

              --remove-bcc-headers[=(on|off)]
                     Enable or disable the removal of Bcc headers. See the remove_bcc_headers command.

              -X, --logfile=[file]
                     Set or unset the log file. See the logfile command.

              --logfile-time-format=[fmt]
                     Set or unset the log file time format. See the logfile_time_format command.

              --syslog[=(on|off|facility)]
                     Enable or disable syslog logging. See the syslog command.

              -t, --read-recipients
                     Read  recipient  addresses  from the To, Cc, and Bcc headers of the mail in addition to the recipients given on the command line.  If any Resent- headers are
                     present, then the addresses from any Resent-To, Resent-Cc, and Resent-Bcc headers in the first block of Resent- headers are used instead.

              --read-envelope-from
                     Read the envelope from address from the From header of the mail.  Currently this header must be on a single line for this option to work correctly.

              --aliases=[file]
                     Set or unset an aliases file. See the aliases command.

              -Fname Msmtp adds a From header to mails that lack it, using the envelope from address. This option allows one to set a full name to be used in that header.

              --     This marks the end of options. All following arguments will be treated as recipient addresses, even if they start with a `-'.

       The following options are accepted but ignored for sendmail compatibility:
       -Btype, -bm, -G, -hN, -i, -L tag, -m, -n, -O option=value, -ox value

USAGE
       A suggestion for a suitable configuration file can be generated using the --configure option.  Normally, a system wide configuration file and/or a user configuration  file
       contain information about which SMTP server to use and how to use it, but all settings can also be configured on the command line.
       The information about SMTP servers is organized in accounts. Each account describes one SMTP server: host name, authentication settings, TLS settings, and so on. Each con‐
       figuration file can define multiple accounts.

       The user can choose which account to use in one of three ways:

       --account=id
              Use the given account. Command line settings override configuration file settings.

       --host=hostname
              Use only the settings from the command line; do not use any configuration file data.

       --from=address or --read-envelope-from
              Choose the first account from the system or user configuration file that has a matching envelope-from address as specified by a from command. This works  only  when
              neither --account nor --host is used.

       If none of the above options is used (or if no account has a matching from command), then the account "default" is used.

       Msmtp transmits mails unaltered to the SMTP server, with the following exceptions:
       - The Bcc header(s) will be removed. This behavior can be changed with the remove_bcc_headers command and --remove-bcc-headers option.
       - A From header will be added if the mail does not have one. This can be changed with the add_missing_from_header command and --add-missing-from-header option.  The header
       will use the envelope from address and optionally a full name set with the -F option.
       - A Date header will be added if the mail does not have one. This can be changed with the add_missing_date_header command and --add-missing-date-header option.

       Skip to the EXAMPLES section for a quick start.

CONFIGURATION FILES
       If it exists and is readable, a system wide configuration file SYSCONFDIR/msmtprc will be loaded, where SYSCONFDIR depends on your platform.  Use  --version  to  find  out
       which directory is used.
       If it exists and is readable, a user configuration file will be loaded (~/.msmtprc will be tried first followed by $XDG_CONFIG_HOME/msmtp/config by default, but see --ver‐
       sion). Accounts defined in the user configuration file override accounts from the system configuration file.
       Configuration data from either file can be changed by command line options.

       A configuration file is a simple text file.  Empty lines and comment lines (whose first non-blank character is `#') are ignored.
       Every other line must contain a command and may contain an argument to that command.
       The argument may be enclosed in double quotes ("), for example if its first or last character is a blank.
       If a file name starts with the tilde (~), this tilde will be replaced by $HOME.  If a command accepts the argument on, it also accepts an empty argument and treats that as
       if it was on.
       Commands are organized in accounts. Each account starts with the account command and defines the settings for one SMTP account.

       Skip to the EXAMPLES section for a quick start.

       Commands are as follows:

       defaults
              Set defaults. The following configuration commands will set default values for all following account definitions in the current configuration file.

       account name [:account[,...]]
              Start a new account definition with the given name. The current default values are filled in.
              If  a colon and a list of previously defined accounts is given after the account name, the new account, with the filled in default values, will inherit all settings
              from the accounts in the list.

       host hostname
              The SMTP server to send the mail to.  The argument may be a host name or a network address.  Every account definition must contain this command.

       port number
              The port that the SMTP server listens on.  The default is 25 ("smtp"), unless TLS without STARTTLS is used, in which case it is 465 ("smtps").

       source_ip [IP]
              Set a source IP address to bind the outgoing connection to. Useful only in special cases on multi-home systems. An empty argument disables this.

       proxy_host [IP|hostname]
              Use a SOCKS proxy. All network traffic will go through this proxy host, including DNS queries, except for a DNS query that might be necessary to resolve  the  proxy
              host  name  itself  (this  can be avoided by using an IP address as proxy host name). An empty hostname argument disables proxy usage.  The supported SOCKS protocol
              version is 5. If you want to use this with Tor, see also "Using msmtp with Tor" below.

       proxy_port [number]
              Set the port number for the proxy host. An empty number argument resets this to the default port.

       timeout (off|seconds)
              Set or unset a network timeout, in seconds. The argument off means that no timeout will be set, which means that the operating system default will be used.

       protocol (smtp|lmtp)
              Set the protocol to use. Currently only SMTP and LMTP are supported. SMTP is the default. See the port command above for default ports.

       domain argument
              Use this command to set the argument of the SMTP EHLO (or LMTP LHLO) command.  The default is localhost, which is stupid but usually works. Try to  change  the  de‐
              fault  if mails get rejected due to anti-SPAM measures. Possible choices are the domain part of your mail address (provider.example for joe@provider.example) or the
              fully qualified domain name of your host (if available).

       auth [(on|off|method)]
              Enable or disable authentication and optionally choose a method to use. The argument on chooses a method automatically.
              Usually a user name and a password are used for authentication. The user name is specified in the configuration file with the user command. There are five different
              methods to specify the password:
              1.  Add  the password to the system key ring.  Currently supported key rings are the Gnome key ring and the Mac OS X Keychain.  For the Gnome key ring, use the com‐
              mand secret-tool (part of Gnome's libsecret) to store passwords: secret-tool store --label=msmtp host mail.freemail.example service smtp user joe.smith.  On Mac  OS
              X, use the following command: security add-internet-password -s mail.freemail.example -r smtp -a joe.smith -w.  In both examples, replace mail.freemail.example with
              the SMTP server name, and joe.smith with your user name.
              2. Store the password in an encrypted files, and use passwordeval to specify a command to decrypt that file, e.g. using GnuPG. See EXAMPLES.
              3. Store the password in the configuration file using the password command.  (Usually it is not considered a good idea to store passwords in plain text  files.   If
              you do it anyway, you must make sure that the file can only be read by yourself.)
              4. Store the password in ~/.netrc. This method is probably obsolete.
              5. Type the password into the terminal when it is required.
              It is recommended to use method 1 or 2.
              Multiple  authentication  methods exist. Most servers support only some of them.  Historically, sophisticated methods were developed to protect passwords from being
              sent unencrypted to the server, but nowadays everybody needs TLS anyway, so the simple methods suffice since the whole session is protected. A suitable  authentica‐
              tion method is chosen automatically, and when TLS is disabled for some reason, only methods that avoid sending clear text passwords are considered.
              The  following  user  /  password  methods  are supported: plain (a simple plain text method, with base64 encoding, supported by almost all servers), scram-sha-1 (a
              method that avoids clear-text passwords), cram-md5 (an obsolete method that avoids clear-text passwords, but is not considered secure anymore), digest-md5 (an over‐
              complicated  obsolete  method  that avoids clear-text passwords, but is not considered secure anymore), login (a non-standard clear-text method similar to but worse
              than the plain method), ntlm (an obscure non-standard method that is now considered broken; it sometimes requires a special domain parameter passed via ntlmdomain).
              There are currently two authentication methods that are not based on user / password information and have to be chosen manually: external (the  authentication  hap‐
              pens  outside  of  the  protocol, typically by sending a TLS client certificate, and the method merely confirms that this authentication succeeded), and gssapi (the
              Kerberos framework takes care of secure authentication, only a user name is required).
              It depends on the underlying authentication library and its version whether a particular method is supported or not. Use --version to find  out  which  methods  are
              supported.

       user login
              Set the user name for authentication. An empty argument unsets the user name.

       password secret
              Set the password for authentication. An empty argument unsets the password.  Consider using the passwordeval command or a key ring instead of this command, to avoid
              storing plain text passwords in the configuration file.

       passwordeval [eval]
              Set the password for authentication to the output (stdout) of the command eval.  This can be used e.g. to decrypt password files on the fly or to query  key  rings,
              and thus to avoid storing plain text passwords.

       ntlmdomain [domain]
              Set a domain for the ntlm authentication method. This is obsolete.

       tls [(on|off)]
              Enable or disable TLS (also known as SSL) for secured connections.
              Transport  Layer Security (TLS) "... provides communications privacy over the Internet.  The protocol allows client/server applications to communicate in a way that
              is designed to prevent eavesdropping, tampering, or message forgery" (quote from RFC2246).
              A server can use TLS in one of two modes: via a STARTTLS command (the session starts with the normal protocol initialization, and TLS is then started using the pro‐
              tocol's  STARTTLS  command), or immediately (TLS is initialized before the normal protocol initialization; this requires a separate port). The first mode is the de‐
              fault, but you can switch to the second mode by disabling tls_starttls.
              When TLS is started, the server sends a certificate to identify itself. To verify the server identity, a client program is expected to check that the certificate is
              formally correct and that it was issued by a Certificate Authority (CA) that the user trusts. (There can also be certificate chains with intermediate CAs.)
              The  list of trusted CAs is specified using the tls_trust_file command.  The default value ist "system" and chooses the system-wide default, but you can also choose
              the trusted CAs yourself.
              One practical problem with this approach is that the client program should also check if the server certificate has been revoked for some reason, using  a  Certifi‐
              cate  Revocation  List  (CRL).  A  CRL  file  can be specified using the tls_crl_file command, but getting the relevant CRL files and keeping them up to date is not
              straightforward. You are basically on your own.
              A much more serious and fundamental problem is is that you need to trust CAs.  Like any other organization, a CA can be incompetent,  malicious,  subverted  by  bad
              people,  or  forced by government agencies to compromise end users without telling them. All of these things happened and continue to happen worldwide.  The idea to
              have central organizations that have to be trusted for your communication to be secure is fundamentally broken.
              Instead of putting trust in a CA, you can choose to trust only a single certificate for the server you want to connect to. For that purpose, specify the certificate
              fingerprint with tls_fingerprint. This makes sure that no man-in-the-middle can fake the identity of the server by presenting you a fraudulent certificate issued by
              some CA that happens to be in your trust list.  However, you have to update the fingerprint whenever the server certificate changes, and you have to make sure  that
              the change is legitimate each time, e.g. when the old certificate expired. This is inconvenient, but it's the price to pay.
              Information about a server certificate can be obtained with --serverinfo --tls --tls-certcheck=off. This includes the issuer CA of the certificate (so you can trust
              that CA via tls_trust_file), and the fingerprint of the certificate (so you can trust that particular certificate via tls_fingerprint).
              TLS also allows the server to verify the identity of the client. For this purpose, the client has to present a certificate issued by a CA that the server trusts. To
              present  that  certificate, the client also needs the matching key file. You can set the certificate and key files using tls_cert_file and tls_key_file. This mecha‐
              nism can also be used to authenticate users, so that traditional user / password authentication is not necessary anymore. See the external mechanism in auth.

       tls_starttls [(on|off)]
              Choose the TLS variant: start TLS from within the session (on, default), or tunnel the session through TLS (off).

       tls_trust_file file
              Activate server certificate verification using a list of trusted Certification Authorities (CAs). The default is the special value "system", which selects the  sys‐
              tem default. An empty argument disables trust in CAs.  If you select a file, it must be in PEM format, and you should also use tls_crl_file.

       tls_crl_file [file]
              Set a certificate revocation list (CRL) file for TLS, to check for revoked certificates. An empty argument disables this.

       tls_fingerprint [fingerprint]
              Set  the  fingerprint  of  a single certificate to accept for TLS. This certificate will be trusted regardless of its contents (this overrides tls_trust_file).  The
              fingerprint should be of type SHA256, but can for backwards compatibility also be of type SHA1 or MD5 (please avoid this).  The format  should  be  01:23:45:67:....
              Use --serverinfo --tls --tls-certcheck=off --tls-fingerprint= to get the server certificate fingerprint.

       tls_key_file file
              Send a client certificate to the server (use this together with tls_cert_file}).  The file must contain the private key of a certificate in PEM format. An empty ar‐
              gument disables this feature.

       tls_cert_file file
              Send a client certificate to the server (use this together with tls_key_file).  The file must contain a certificate in PEM format. An empty argument  disables  this
              feature.

       tls_certcheck [(on|off)]
              Enable  or  disable  checks of the server certificate. They are enabled by default.  Disabling them will override tls_trust_file and tls_fingerprint.  WARNING: When
              the checks are disabled, TLS sessions will not be secure!

       tls_min_dh_prime_bits [bits]
              Set or unset the minimum number of Diffie-Hellman (DH) prime bits that mpop will accept for TLS sessions.  The default is set by the TLS library and can be selected
              by using an empty argument to this command.  Only lower the default (for example to 512 bits) if there is no other way to make TLS work with the remote server.

       tls_priorities [priorities]
              Set  the priorities for TLS sessions. The default is set by the TLS library and can be selected by using an empty argument to this command.  See the GnuTLS documen‐
              tation of the gnutls_priority_init function for a description of the priorities string.

       from envelope_from
              Set the envelope-from address. This address will only be used when auto_from is off.

       auto_from [(on|off)]
              Enable or disable automatic envelope-from addresses. The default is off.  When enabled, an envelope-from address of the form user@domain will be generated.  The lo‐
              cal part will be set to USER or, if that fails, to LOGNAME or, if that fails, to the login name of the current user.  The domain part can be set with the maildomain
              command.  If the maildomain is empty, the envelope-from address will only consist of the user name and not have a domain part. When auto_from is disabled, the enve‐
              lope-from address must be set explicitly.

       maildomain [domain]
              Set a domain part for the generation of an envelope-from address. This is only used when auto_from is on. The domain may be empty.

       dsn_notify (off|condition)
              This  command  sets the condition(s) under which the mail system should send DSN (Delivery Status Notification) messages. The argument off disables explicit DSN re‐
              quests, which means the mail system decides when to send DSN messages. This is the default.  The condition must be never, to never request notification, or a  comma
              separated list (no spaces!) of one or more of the following: failure, to request notification on transmission failure, delay, to be notified of message delays, suc‐
              cess, to be notified of successful transmission. The SMTP server must support the DSN extension.

       dsn_return (off|amount)
              This command controls how much of a mail should be returned in DSN (Delivery Status Notification) messages. The argument off disables explicit DSN  requests,  which
              means  the  mail system decides how much of a mail it returns in DSN messages. This is the default.  The amount must be headers, to just return the message headers,
              or full, to return the full mail.  The SMTP server must support the DSN extension.

       add_missing_from_header [(on|off)]
              This command controls whether to add a From header if the mail does not have one.  The default is to add it.

       add_missing_date_header [(on|off)]
              This command controls whether to add a Date header if the mail does not have one.  The default is to add it.

       remove_bcc_headers [(on|off)]
              This command controls whether to remove Bcc headers. The default is to remove them.

       logfile [file]
              An empty argument disables logging (this is the default).
              When logging is enabled by choosing a log file, msmtp will append one line to the log file for each mail it tries to send via the account that  this  log  file  was
              chosen for.
              The  line  will include the following information: date and time in the format specified by logfile_time_format, host name of the SMTP server, whether TLS was used,
              whether authentication was used, authentication user name (only if authentication is used), envelope-from address, recipient addresses, size of the mail  as  trans‐
              ferred  to the server (only if the delivery succeeded), SMTP status code and SMTP error message (only in case of failure and only if available), error message (only
              in case of failure and only if available), exit code (from sysexits.h; EX_OK indicates success).
              If the filename is a dash (-), msmtp prints the log line to the standard output.

       logfile_time_format [fmt]
              Set or unset the log file time format. This will be used as the format string for the strftime() function. An empty argument chooses the default ("%b %d %H:%M:%S").

       syslog [(on|off|facility)]
              Enable or disable syslog logging. The facility can be one of LOG_USER, LOG_MAIL, LOG_LOCAL0, ..., LOG_LOCAL7. The default is LOG_USER.
              Each time msmtp tries to send a mail via the account that contains this syslog command, it will log one entry to the syslog service with the chosen facility.
              The line will include the following information: host name of the SMTP server, whether TLS was used, whether authentication was used, envelope-from address, recipi‐
              ent  addresses, size of the mail as transferred to the server (only if the delivery succeeded), SMTP status code and SMTP error message (only in case of failure and
              only if available), error message (only in case of failure and only if available), exit code (from sysexits.h; EX_OK indicates success).

       aliases [file]
              Replace local recipients with addresses in the aliases file.  The aliases file is a plain text file containing mappings between a local address and a list of domain
              addresses.  A local address is defined as one without an `@' character and a domain address is one with an `@' character.  The mappings are of the form:
                  local: someone@example.com, person@domain.example
              Multiple domain addresses are separated with commas.  Comments start with `#' and continue to the end of the line.
              The local address default has special significance and is matched if the local address is not found in the aliases file.  If no default alias is found, then the lo‐
              cal address is left as is.
              An empty argument to the aliases command disables the replacement of local addresses.  This is the default.

EXAMPLES
       Configuration file

       # Example for a user configuration file ~/.msmtprc
       #
       # This file focusses on TLS and authentication. Features not used here include
       # logging, timeouts, SOCKS proxies, TLS parameters, Delivery Status Notification
       # (DSN) settings, and more.

       # Set default values for all following accounts.
       defaults

       # Use the mail submission port 587 instead of the SMTP port 25.
       port 587

       # Always use TLS.
       tls on

       # Set a list of trusted CAs for TLS. The default is to use system settings, but
       # you can select your own file.
       #tls_trust_file /etc/ssl/certs/ca-certificates.crt

       # If you select your own file, you should also use the tls_crl_file command to
       # check for revoked certificates, but unfortunately getting revocation lists and
       # keeping them up to date is not straightforward.
       #tls_crl_file ~/.tls-crls

       # A freemail service
       account freemail

       # Host name of the SMTP server
       host smtp.freemail.example

       # As an alternative to tls_trust_file/tls_crl_file, you can use tls_fingerprint
       # to pin a single certificate. You have to update the fingerprint when the
       # server certificate changes, but an attacker cannot trick you into accepting
       # a fraudulent certificate. Get the fingerprint with
       # $ msmtp --serverinfo --tls --tls-certcheck=off --host=smtp.freemail.example
       #tls_fingerprint 00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF:00:11:22:33

       # Envelope-from address
       from joe_smith@freemail.example

       # Authentication. The password is given using one of five methods, see below.
       auth on
       user joe.smith

       # Password method 1: Add the password to the system keyring, and let msmtp get
       # it automatically. To set the keyring password using Gnome's libsecret:
       # $ secret-tool store --label=msmtp \
       #   host smtp.freemail.example \
       #   service smtp \
       #   user joe.smith

       # Password method 2: Store the password in an encrypted file, and tell msmtp
       # which command to use to decrypt it. This is usually used with GnuPG, as in
       # this example. Usually gpg-agent will ask once for the decryption password.
       passwordeval gpg2 --no-tty -q -d ~/.msmtp-password.gpg

       # Password method 3: Store the password directly in this file. Usually it is not
       # a good idea to store passwords in plain text files. If you do it anyway, at
       # least make sure that this file can only be read by yourself.
       #password secret123

       # Password method 4: Store the password in ~/.netrc. This method is probably not
       # relevant anymore.

       # Password method 5: Do not specify a password. Msmtp will then prompt you for
       # it. This means you need to be able to type into a terminal when msmtp runs.

       # A second mail address at the same freemail service
       account freemail2 : freemail
       from joey@freemail.example

       # The SMTP server of your ISP
       account isp
       host mail.isp.example
       from smithjoe@isp.example
       auth on
       user 12345

       # Set a default account
       account default : freemail

       Using msmtp with Mutt

       Create a configuration file for msmtp and add the following lines to your Mutt configuration file:
       set sendmail="/path/to/msmtp"
       set use_from=yes
       set realname="Your Name"
       set from=you@example.com
       set envelope_from=yes
       The envelope_from=yes option lets Mutt use the -f option of msmtp. Therefore msmtp chooses the first account that matches the from address you@example.com.
       Alternatively, you can use the -a option:
       set sendmail="/path/to/msmtp -a my-account"
       Or set everything from the command line (but note that you cannot set a password this way):
       set sendmail="/path/to/msmtp --host=mailhub -f me@example.com --tls --tls-trust-file=trust.crt"

       If you have multiple mail accounts in your msmtp configuration file and let Mutt use the -f option to choose the right one, you can easily switch accounts in Mutt with the
       following Mutt configuration lines:
       macro generic "<esc>1" ":set from=you@example.com"
       macro generic "<esc>2" ":set from=you@your-employer.example"
       macro generic "<esc>3" ":set from=you@some-other-provider.example"

       Using msmtp with mail

       Define a default account, and put the following in your ~/.mailrc:
       set sendmail="/path/to/msmtp"

       Using msmtp with Tor

       Use the following settings:
       proxy_host 127.0.0.1
       proxy_port 9050
       tls on
       Use an IP address as proxy host name, so that msmtp does not leak a DNS query when resolving it.
       TLS is required to prevent exit hosts from reading your SMTP session.
       Do not set domain to something that you do not want to reveal (do not set it at all if possible).

       Aliases file

       # Example aliases file

       # Send root to Joe and Jane
       root: joe_smith@example.com, jane_chang@example.com

       # Send cron to Mark
       cron: mark_jones@example.com

       # Send everything else to admin
       default: admin@domain.example

FILES
       SYSCONFDIR/msmtprc
              System configuration file. Use --version to find out what SYSCONFDIR is on your platform.

       ~/.msmtprc or $XDG_CONFIG_HOME/msmtp/config
              User configuration file.

       ~/.netrc and SYSCONFDIR/netrc
              The netrc file contains login information. Before prompting for a password, msmtp will search it in ~/.netrc and SYSCONFDIR/netrc.

ENVIRONMENT
       USER, LOGNAME
              These variables override the user's login name when constructing an envelope-from address. LOGNAME is only used if USER is unset.

       TMPDIR Directory to create temporary files in. If this is unset, a system specific default directory is used.
              A  temporary file is only created when the -t/--read-recipients or --read-envelope-from option is used. The file is then used to buffer the headers of the mail (but
              not the body, so the file won't get very large).

       EMAIL, SMTPSERVER
              These environment variables are used only if neither --host nor --account is used and there is no default account defined in the configuration files. In this  case,
              the host name is taken from SMTPSERVER, and the envelope from address is taken from EMAIL, unless overridden by --from or --read-envelope-from. Currently SMTPSERVER
              must contain a plain host name (no URL), and EMAIL must contain a plain address (no names or additional information).

AUTHORS
       msmtp was written by Martin Lambers <marlam@marlam.de>.
       Other authors are listed in the AUTHORS file in the source distribution.

SEE ALSO
       sendmail(8), netrc(5) or ftp(1)

                                                                                      2019-01                                                                             MSMTP(1)
man mutt
mutt(1)                                                                            User Manuals                                                                            mutt(1)

NAME
       mutt - The Mutt Mail User Agent

SYNOPSIS
       mutt [-nRyzZ] [-e cmd] [-F file] [-m type] [-f file]

       mutt [-Enx] [-e cmd] [-F file] [-H file] [-i file] [-s subj] [-b addr] [-c addr] [-a file [...] --] addr|mailto_url [...]

       mutt [-nx] [-e cmd] [-F file] [-s subj] [-b addr] [-c addr] [-a file [...] --] addr|mailto_url [...]  < message

       mutt [-n] [-e cmd] [-F file] -p

       mutt [-n] [-e cmd] [-F file] -A alias

       mutt [-n] [-e cmd] [-F file] -Q query

       mutt -v[v]

       mutt -D

DESCRIPTION
       Mutt  is  a  small  but very powerful text based program for reading and sending electronic mail under unix operating systems, including support for color terminals, MIME,
       OpenPGP, and a threaded sorting mode.

       Note: This manual page gives a brief overview of mutt's command line options. You should find a copy of the full manual in /usr/share/doc/mutt, in text, HTML,  and/or  PDF
       format.

OPTIONS
       -A alias
              An expanded version of the given alias is passed to stdout.

       -a file [...]
              Attach  a  file to your message using MIME.  When attaching single or multiple files, separating filenames and recipient addresses with "--" is mandatory, e.g. mutt
              -a image.jpg -- addr1 or mutt -a img.jpg *.png -- addr1 addr2.  The -a option must be placed at the end of command line options.

       -b address
              Specify a blind-carbon-copy (BCC) recipient

       -c address
              Specify a carbon-copy (CC) recipient

       -d level
              If mutt was compiled with +DEBUG log debugging output to ~/.muttdebug0.  Level can range from 1-5 and effects verbosity. A value of 2 is recommended.

       -D     Print the value of all configuration options to stdout.

       -E     Causes the draft file specified by -H or include file specified by -i to be edited during message composition.

       -e command
              Specify a configuration command to be run after processing of initialization files.

       -f mailbox
              Specify which mailbox to load.

       -F muttrc
              Specify an initialization file to read instead of ~/.muttrc

       -h     Display help.

       -H draft
              Specify a draft file which contains header and body to use to send a message.

       -i include
              Specify a file to include into the body of a message.

       -m type
              specify a default mailbox type for newly created folders.

       -n     Causes Mutt to bypass the system configuration file.

       -p     Resume a postponed message.

       -Q query
              Query a configuration variables value.  The query is executed after all configuration files have been parsed, and any commands given on the command line  have  been
              executed.

       -R     Open a mailbox in read-only mode.

       -s subject
              Specify the subject of the message.

       -v     Display the Mutt version number and compile-time definitions.

       -vv    Display license and copyright information.

       -x     Emulate the mailx compose mode.

       -y     Start Mutt with a listing of all mailboxes specified by the mailboxes command.

       -z     When used with -f, causes Mutt not to start if there are no messages in the mailbox.

       -Z     Causes Mutt to open the first mailbox specified by the mailboxes command which contains new mail.

       --     Treat remaining arguments as addr even if they start with a dash.  See also "-a" above.

ENVIRONMENT
       EDITOR Specifies the editor to use if VISUAL is unset.

       EMAIL  The user's e-mail address.

       HOME   Full path of the user's home directory.

       MAIL   Full path of the user's spool mailbox.

       MAILDIR
              Full path of the user's spool mailbox if MAIL is unset.  Commonly used when the spool mailbox is a maildir (5) folder.

       MAILCAPS
              Path to search for mailcap files.

       MM_NOASK
              If this variable is set, mailcap are always used without prompting first.

       PGPPATH
              Directory in which the user's PGP public keyring can be found.  When used with the original PGP program, mutt and pgpring (1) rely on this being set.

       TMPDIR Directory in which temporary files are created.

       REPLYTO
              Default Reply-To address.

       VISUAL Specifies the editor to use when composing messages.

FILES
       ~/.muttrc or ~/.mutt/muttrc
              User configuration file.

       /etc/Muttrc
              System-wide configuration file.

       /tmp/muttXXXXXX
              Temporary files created by Mutt.

       ~/.mailcap
              User definition for handling non-text MIME types.

       /etc/mailcap
              System definition for handling non-text MIME types.

       ~/.mime.types
              User's personal mapping between MIME types and file extensions.

       /etc/mime.types
              System mapping between MIME types and file extensions.

       /usr/bin/mutt_dotlock
              The privileged dotlocking program.

       /usr/share/doc/mutt/manual.txt.gz
              The Mutt manual.

BUGS
       None.  Mutts have fleas, not bugs.

FLEAS
       Suspend/resume  while  editing  a file with an external editor does not work under SunOS 4.x if you use the curses lib in /usr/5lib.  It does work with the S-Lang library,
       however.

       Resizing the screen while using an external pager causes Mutt to go haywire on some systems.

       Suspend/resume does not work under Ultrix.

       The help line for the index menu is not updated if you change the bindings for one of the functions listed while Mutt is running.

       For a more up-to-date list of bugs, errm, fleas, please visit the mutt project's bug tracking system under https://gitlab.com/muttmua/mutt/issues.

NO WARRANTIES
       This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A  PARTICULAR
       PURPOSE.  See the GNU General Public License for more details.

SEE ALSO
       curses(3), mailcap(5), maildir(5), mbox(5), mutt_dotlock(1), muttrc(5), ncurses(3), sendmail(1), smail(1).

       Mutt Home Page: http://www.mutt.org/

       The Mutt manual

AUTHOR
       Michael Elkins, and others.  Use <mutt-dev@mutt.org> to contact the developers.

Unix                                                                               January 2009                                                                            mutt(1)
""""
