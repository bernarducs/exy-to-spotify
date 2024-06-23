# Exy to Spotify

If you follow exystence.net to check new releases, why not add them to your Spotify library without to get there?

### The enviroment

- Clone this repo;

```bash
$ cd exi-to-spotify
$ python -m venv .ve
$ source .ve/bin/activate
(.ve) $ pip install -r requirements.txt
```

- Make a .env file with...
```
CLIENT_ID='your-client-id'
CLIENT_SECRET='your-secret-id'
REDIRECT_URI='the-callback-uri'
USERNAME='your-username'
```

[Check here to see how to get spotify credentials](https://developer.spotify.com/documentation/web-api)

### Running (not implemented)

Let's say you wants add new albums for soul, punk and R&B:

```bash
(.ve) $ python run.py add_new_albums --categories=['soul', 'punk', 'R&B'] --max_entries=20
```

### Steps
- [x] exy module
- [ ] spotify module
- [ ] main file
- [ ] CLI
- [ ] tests