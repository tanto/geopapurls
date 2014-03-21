import smtplib
from django.core.mail.backends.smtp import EmailBackend,DNS_NAME

class SSLSMTPEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            # Nothing to do if the connection is already open.
            return False
        try:
            # If local_hostname is not specified, socket.getfqdn() gets used.
            # For performance, we use the cached FQDN for local_hostname.
            self.connection = smtplib.SMTP_SSL(self.host, self.port)
            if self.use_tls:
                self.connection.ehlo()
                self.connection.starttls()
                self.connection.ehlo()
            self.connection.login(self.username, self.password)
            return True
        except:
            if not self.fail_silently:
                raise
        else:
            return super(SSLSMTPEmailBackend,self).open()