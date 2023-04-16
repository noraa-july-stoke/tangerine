
```python
from os.environ import get as get_env_key
from tangerine import Tangerine, Keychain, Auth, Router, Ctx, TangerineError
from key_limes import KeyLimes
from buddhas_hand import BuddhasHand

const db = BuddhasHand({
    host: get_env_key("DB_HOST"),
    conn_string: get_env_key("DB_CONN_STRING"),
})

app = Tangerine()

keychain = KeyLimes({
    google_cloud: get_env_key("GOOGLE_CLOUD_CREDENTIAL"),
    secret_keys: [get_env_key("SECRET_KEY_1"), get_env_key("SECRET_KEY_2")],
    db_host: get_env_key("DB_HOST"),
    db_conn_string: get_env_key("DB_CONN_STRING"),
})


tangerine.keychain = Keychain()

# assigning tangerine.auth to the Auth class will automatically
# create a
tangerine.auth =

app.start()
```
