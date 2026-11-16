# CUNY Transcript Downloader

Python env setup: https://www.w3schools.com/python/python_virtualenv.asp

Activate Environment
```
# source myvenv/bin/activate

```

Credentials setup
import keyring
keyring.set_password("cuny", "username", "your.name@login.cuny.edu")
keyring.set_password("cuny", "password", "YOUR_PASSWORD")
keyring.set_password("cuny", "totp_secret", "YOUR_BASE32_SECRET")

pip install playwright pyotp keyring
playwright install chromium

page.goto("https://home.cunyfirst.cuny.edu/psc/cnyihprd/EMPLOYEE/EMPL/c/NUI_FRAMEWORK.PT_LANDINGPAGE.GBL?&")
page.get_by_role("link", name="Student Center").click()
page.get_by_role("link", name="Graduation and Transcript").click()
page.get_by_role("link", name="John Jay College of Criminal").click()
with page.expect_popup() as page1_info:
    page.get_by_role("button", name="Submit").click()
page1 = page1_info.value
page1.locator("html > body > iframe").last.content_frame.get_by_role("button", name="Download").click()
with page1.expect_download() as download1_info:
    page1.locator("html > body > iframe").last.content_frame.get_by_role("button", name="Download").press("Escape")
download1 = download1_info.value
page1.locator("html > body > iframe").last.content_frame.get_by_role("button", name="Download").click()
page1.locator("html > body > iframe").last.content_frame.get_by_role("button", name="Download").press("Escape")

## Future features
- Add docker container for app
