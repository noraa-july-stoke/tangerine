

```python
# this is how we define a route with tangerine.
from tangerine import Tangerine, Router
import smtplib

tangerine = Tangerine()
router = Router()

router.post('/send-email', lambda ctx:
    # Try to send an email using the information from the request body
    try:
        message = ctx.req.form.get('message')
        sender = 'youremail@gmail.com'
        password = 'yourpassword'
        recipient = ctx.req.form.get('recipient')

        smtp_server = 'smtp.gmail.com'
        port = 587

        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender, password)

        subject = 'Hello from Tangerine!'
        body = f'This message was sent from Tangerine: {message}'
        message = f'Subject: {subject}\n\n{body}'

        server.sendmail(sender, recipient, message)

        # Set the response text if the email was sent successfully
        ctx.res.status_code = 200
        ctx.res.text = f'Email sent to {recipient}!'
    except:
        # Set the response text if the email failed to send
        ctx.res.status_code = 500
        ctx.res.text = 'Failed to send email'

    # Send the response
    ctx.send()
)

# Use the router with the Tangerine app
tangerine.use(router)

# Start the Tangerine app
if __name__ == '__main__':
    tangerine.start()


```
