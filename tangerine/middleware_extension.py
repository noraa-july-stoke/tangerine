from flask_cors import CORS


def cors_middleware(ctx, next_middleware):
    req = ctx.request
    res = ctx.response

    if req.method == 'OPTIONS':
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        res.headers['Access-Control-Allow-Headers'] = 'content-type'
        # preflight request. reply successfully:
        res.status_code = 200
        res.data = ""
    else:
        # actual request; reply successfully:
        res.headers['Access-Control-Allow-Origin'] = '*'

    next_middleware()  # Call the next middleware
