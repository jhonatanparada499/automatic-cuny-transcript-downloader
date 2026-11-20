# CUNY Transcript Downloader

## Quick Start
### Ubuntu/Debian
Run following assuming keyring credentials have been setup and an there is an virtual environment called "venv" with the required dependencies.  
```
$ bash run_get_transcript.sh
```

## Credentials setup
```python
import keyring
keyring.set_password("cuny", "username", "your.name@login.cuny.edu")  
keyring.set_password("cuny", "password", "YOUR_PASSWORD")  
keyring.set_password("cuny", "totp_secret", "YOUR_BASE32_SECRET")  
```

## Future features
- Add docker container for app

## References
- https://www.w3schools.com/python/python_virtualenv.asp  
