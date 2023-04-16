
```python
from os import environ
from tangerine import Tangerine, Keychain, Router, Ctx, TangerineError
# keylimes is a keychain that holds your environment variables
from key_limes import KeyLimes
# buddhas hand is a database wrapper
from buddhas_hand import BuddhasHand
# yuzu is an authentication wrapper that draws on AuthLib
from yuzu import Yuzu


db = BuddhasHand(
    host=environ.get("DB_HOST"),
    conn_string=environ.get("DB_CONN_STRING")
)

tangerine = Tangerine()

keychain = KeyLimes(
    google_cloud=environ.get("GOOGLE_CLOUD_CREDENTIAL"),
    secret_keys=[environ.get("SECRET_KEY_1"), environ.get("SECRET_KEY_2")],
    db_host=environ.get("DB_HOST"),
    db_conn_string=environ.get("DB_CONN_STRING")
)

yuzu = Yuzu(
    strategies={"providers": ["google", "facebook", "twitter"], "local": True},
    keychain=keychain
)

# assigning tangerine.keychain to the keychain instance will allow you to use the
# keychain and bypass the yuzu setup
tangerine.keychain = keychain

# assigning tangerine.auth to the yuzu instance will allow you to use the yuzu auth
# middlewares in your routes. yuzu will look through the keychain for the required keys
# for anything it needs for the required strategies and then append the keychain to
# tangerine so that you can use it in your routes
tangerine.auth = yuzu


tangerine.start()

```




```python
from os import environ
from tangerine import Tangerine, Keychain, Router, Ctx, TangerineError
from key_limes import KeyLimes
from buddhas_hand import BuddhasHand
from yuzu import Yuzu

db = BuddhasHand(
    host=environ.get("DB_HOST"),
    conn_string=environ.get("DB_CONN_STRING")
)

tangerine = Tangerine()
keychain = KeyLimes(
    google_cloud=environ.get("GOOGLE_CLOUD_CREDENTIAL"),
    secret_keys=[environ.get("SECRET_KEY_1"), environ.get("SECRET_KEY_2")],
    db_host=environ.get("DB_HOST"),
    db_conn_string=environ.get("DB_CONN_STRING")
)

yuzu = Yuzu(
    strategies={"providers": ["google", "facebook", "twitter"], "local": True},
    keychain=keychain
)

tangerine.keychain = keychain
tangerine.auth = yuzu

tangerine.start()

```



const User = require('../models/User');
const passport = require('koa-passport');
const bcrypt = require('bcryptjs');
const { countDocuments } = require('../models/User');


//!@#$ auth info here;
// logs in user
const login = async (ctx) => {
   return await passport.authenticate('local', (err, user, info, status) => {
        if (user) {
            ctx.login(user);
            ctx.redirect('/api/auth/status');
            ctx.body = ctx.cookies;
        } else {
            ctx.status = 400;
            ctx.body = {status: "error"}
        }
    })(ctx);
}
