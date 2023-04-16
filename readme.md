# Tangerine


I hate flask so I've decided to make a new python framework with better route creation syntax and
am hoping to tackle some problems such as running database migrations in a better fashion (because
ewwww migrations in python frameworks.... javascript frameworks currently handle this so much better).
Looking into the "click" library to make a CLI tool for this.

This is brand new, so still making skeletons/experimenting with the basic architecture and modules that I want to use.
I am working out some kinks in the Tangerine class before I fixup Request, Response,and Ctx and then start to add in
more functionality. Current setup work is under branch architecture-setup.


# Some initial basics...
I am implementing a route creation syntax that I believe is a lot cleaner. It utilizes a lambda function and an endpoint
that get taken in and appended to the router, which can then be passed into the server. I think this could be easier for
javascript developers coming into the python scene.

i decided to use an optional lambda function that gets passed into the router
i was thinking about maybe wrapping the lambdas in a named func under the hood for debugging purposes
and then it would also open the door for allowing an mvc system so you could pick and choose your architecture pattern.
if you pass a lambda in it gets wrapped with a name. if you pass a named function in it gets no wrapper.
so you can do it like this to implement mvc:

```python


from tangerine import Tangerine, Router

def hello_world(ctx):
    ctx.send(200, "Hello, world!")

tangerine = Tangerine()
router = Router()
router.get(Router('/', 'GET', hello_world))

tangerine.use(router.routes())
tangerine.start()

# and using lambda

from tangerine import Tangerine, Router
tangerine = Tangerine()
router = Router()

router.get(Router('/', 'GET', lambda ctx: ctx.send(200, "Hello, world!")))

tangerine.use(router.routes())
tangerine.start()
```

Here is an example implementation of how in intend users be able to start the Tangerine server and begin creating routes. This
example route sends an email with Tangerine framework:

```python
from tangerine import Tangerine, Router
import smtplib

tangerine = Tangerine()
router = Router()


# I think this syntax is cleaner and easier to work with for developers coming in from javascript
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
        ctx.body = f'Email sent to {recipient}!'
        ctx.send(200)
    except:
        # Set the response text if the email failed to send
        body = 'Failed to send email'
        ctx.send(200, body)

    # Send the response
)

# Use the router with the Tangerine app
tangerine.use(router)

# Start the Tangerine app
if __name__ == '__main__':
    tangerine.start()
```


## This readme is a work in progress so keep an eye out for more documentation/outlines of the project.
