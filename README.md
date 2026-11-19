# CUNY Transcript Downloader

Python env setup: https://www.w3schools.com/python/python_virtualenv.asp  

## Activate Environment
```
# source myvenv/bin/activate

```

## Credentials setup
import keyring
keyring.set_password("cuny", "username", "your.name@login.cuny.edu")  
keyring.set_password("cuny", "password", "YOUR_PASSWORD")  
keyring.set_password("cuny", "totp_secret", "YOUR_BASE32_SECRET")  

## Future features
- Add docker container for app
