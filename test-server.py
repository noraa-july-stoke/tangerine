from tangerine import Tangerine, Router, Bergamot
print(Bergamot)
app = Tangerine('localhost', 8080)
router = Router()

def hello_get(ctx):
    ctx.send('Hello World!')

router.get('/', hello_get)

router.post('/', lambda ctx: ctx.send('Hello World!'))
router.put('/', lambda ctx: ctx.send('Hello World!'))
router.delete('/', lambda ctx: ctx.send('Hello World!'))
app.start()
