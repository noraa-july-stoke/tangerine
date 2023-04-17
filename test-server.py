from tangerine import Tangerine, Router
app = Tangerine('localhost', 8081)
router = Router()
router.get('/', lambda ctx: ctx.send('Hello World!'))
router.post('/', lambda ctx: ctx.send('Hello World!'))
router.put('/', lambda ctx: ctx.send('Hello World!'))
router.delete('/', lambda ctx: ctx.send('Hello World!'))
app.start()
