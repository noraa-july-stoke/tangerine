
```text
🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊
     ████████╗ █████╗ ███╗   ██╗ ██████╗ ███████╗██████╗ ██╗███╗   ██╗███████╗
     ╚══██╔══╝██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔══██╗██║████╗  ██║██╔════╝
        ██║   ███████║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝██║██╔██╗ ██║█████╗
        ██║   ██╔══██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗██║██║╚██╗██║██╔══╝
        ██║   ██║  ██║██║ ╚████║╚██████╔╝███████╗██║  ██║██║██║ ╚████║███████╗
        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝
🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊
```
Thanks for checking out Tangerine! This is a new python framework that I am working on. I hope
it will be a lot more intuitive and easier to use than flask. I am currently working on the
architecture and basic functionality. I am hoping to have a working full version of the framework
up and running some time soon.


I am also working on a CLI tool for database migrations.
I aim to make the newframework with better route creation syntax thank flask and
am hoping to tackle some problems such as running database migrations in a better fashion (because
ewwww migrations in python frameworks.... javascript frameworks currently handle this so much better).

This is brand new, so still making skeletons/experimenting with the basic architecture and modules that I want to use.
I am working out some kinks in the Tangerine class before I fixup Request, Response,and Ctx and then start to add in
more functionality. Current setup work is under branch architecture-setup. There are other repos associated with this:
Bergamot, Buddha's Hand, and Key Limes.

# Commit message keys:
```

# anything provided after <relevant comment>: is optional but highly encouraged for tracing.

# for updating any readmes or roadmaps
📖 - <filepath/filename>: <relevant comment>:

# for new features
🚀  - <filepath/filename>: <relevant comment>:

# for debug commits.
🪳👟 - <filepath/filename>: <relevant comment>:

# for refactoring
🧠 - <filepath/filename>: <relevant comment>:

# for documentation
🪷 - <filepath/filename>: <relevant comment>:

# branch initialization commit
🌱 - <filepath/filename>: <relevant comment>

# standard merge message
🔀 - <branch name>: <feature filepath>: <relevant comment>

```



So far, this is what you can do with tangerine...app = Tangerine('localhost', 8000, debug_level=2)

# Create main and API routers with debugging enabled
main_router = Router(prefix='/api/main', debug=True)
api_router = Router(prefix='/api', debug=True)

# Serve static files
app.static('^/(?!api).*$', 'public')

# Main router routes
def hello_world_main(ctx: Ctx) -> None:
    ctx.body = 'Hello, world! Main Router'
    ctx.send(200)


main_router.get('/hello', hello_world_main)

# API router routes
def api_hello_world(ctx: Ctx) -> None:
    ctx.body = json.dumps({"message": "Hello from API!"})
    ctx.send(200, content_type='application/json')

api_router.get('/hello', api_hello_world)

# Middleware
def hello_middle(ctx: Ctx) -> None:
    print("Hello from middleware!!!")

app.use(hello_middle)

# Another middleware
def api_version(ctx: Ctx) -> None:
    ctx.set_res_header("X-API-Version", "1.0")

app.use(api_version)

# Use the main and API routers
app.use_router(main_router)
app.use_router(api_router)

# Start the server
app.start()


```

## More Details TBD


## This readme is a work in progress so keep an eye out for more documentation/outlines of the project.
