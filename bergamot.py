# ╔╗ ┌─┐┬─┐┌─┐┌─┐┌┬┐┌─┐┌┬┐
# ╠╩╗├┤ ├┬┘│ ┬├─┤││││ │ │
# ╚═╝└─┘┴└─└─┘┴ ┴┴ ┴└─┘ ┴
# File: bergamot.py
# Description: This file contains the Bergamot class which is used to send emails

import re
import smtplib
import asyncio
from typing import Dict, Optional

class Bergamot:
    """
    The Bergamot class is used for sending emails. It supports various email providers and also allows for custom configuration.

    Attributes:
        email (str): The email address from which to send emails.
        password (str): The password for the provided email address.
        servers (dict): A dictionary of supported email providers and their SMTP server information.

    Methods:
        send_email(recipient: str, message: str): Asynchronously sends an email to the specified recipient with the given message.
        __repr__(): Returns a string representation of the Bergamot object.
    """

    def __init__(self, email: str, password: str, custom_config: Optional[Dict] = None):
        """
        Initializes the Bergamot object with the sender's email and password.

        Args:
            email (str): The sender's email address.
            password (str): The sender's email password.
            custom_config (Optional[Dict], optional): Additional or custom SMTP server configurations. Defaults to None.
        """
        self.email = email
        self.password = password

        self.servers = {
            'gmail': {
                'smtp_server': 'smtp.gmail.com',
                'port': 587
            },
            'yahoo': {
                'smtp_server': 'smtp.mail.yahoo.com',
                'port': 465
            },
            'hotmail': {
                'smtp_server': 'smtp.live.com',
                'port': 587
            },
            'aol': {
                'smtp_server': 'smtp.aol.com',
                'port': 587
            },
            'comcast': {
                'smtp_server': 'smtp.comcast.net',
                'port': 587
            },
            'icloud': {
                'smtp_server': 'smtp.mail.me.com',
                'port': 587
            },
            'outlook': {
                'smtp_server': 'smtp.office365.com',
                'port': 587
            },
            'protonmail': {
                'smtp_server': 'smtp.protonmail.com',
                'port': 587
            },
            'yahoo_uk': {
                'smtp_server': 'smtp.mail.yahoo.co.uk',
                'port': 465
            }
        }

        if custom_config:
            self.servers.update(custom_config)

    async def send_email(self, recipient: str, message: str):
        """
        Asynchronously sends an email to the specified recipient with the given message.

        Args:
            recipient (str): The recipient's email address.
            message (str): The content of the email.

        Raises:
            ValueError: If the recipient's email is invalid or if the email provider is unsupported.
            ValueError: If there is an error while sending the email.

        Returns:
            str: A success message if the email is sent successfully.
        """
        # Use regex to determine the email provider
        match = re.search('@(\w+)', recipient)
        if not match:
            raise ValueError('Invalid recipient email')
        provider = match.group(1)

        # Get the smtp server and port based on the email provider
        if provider in self.servers:
            server_info = self.servers[provider]
            smtp_server = server_info['smtp_server']
            port = server_info['port']
        else:
            raise ValueError('Unsupported email provider')

        # Try to send the email
        try:
            print(smtp_server, port)
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            await server.login(self.email, self.password)

            subject = 'Hello from Bergamot!'
            body = f'This message was sent from Bergamot: {message}'
            message = f'Subject: {subject}\n\n{body}'

            response = await server.sendmail(self.email, recipient, message)
            print(response)

            return f'Email sent to {recipient}!'
        except:
            raise ValueError('Failed to send email')

    def __repr__(self):
        """
        Returns a string representation of the Bergamot object.

        Returns:
            str: A string representation of the Bergamot object.
        """
        return f'<Bergamot client opened for({self.email})>'
