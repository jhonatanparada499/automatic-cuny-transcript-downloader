# get_transcript.py

import keyring, pyotp, time
from pathlib import Path
from playwright.sync_api import sync_playwright
from datetime import datetime

stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUT = Path.home() / "Downloads" / f"cuny_transcript_{stamp}.pdf"

user = keyring.get_password("cuny", "username")
pw = keyring.get_password("cuny", "password")
totp = pyotp.TOTP(keyring.get_password("cuny", "totp_secret"))

college = "John Jay College of Criminal"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    ctx = browser.new_context(accept_downloads=True)
    page = ctx.new_page()
    page.goto("https://home.cunyfirst.cuny.edu")

    # --- Login (only runs if the session expired) ---
    if page.locator("input[autocomplete=username]").count():
        page.get_by_role("textbox", name="CUNY Login").fill(user)   # user
        page.get_by_role("textbox", name="Password").fill(pw)       # password
        page.get_by_role("button", name="Log in").click()           # submit

        # avoid submitting a code that's about to expire
        if totp.interval - (time.time() % totp.interval) < 3:
            time.sleep(4)

        # redirection to TOTP
        page.get_by_role("textbox", name="Enter TOTP from the").fill(totp.now())
        page.get_by_role("button", name="Verify").click()

    # Student Center -> Academics -> View Unofficial Transcript
    page.get_by_role("link", name="Student Center").click()
    page.get_by_role("link", name="Graduation and Transcript").click()
    page.get_by_role("link", name=college).click()

    # Submit transcript request triggers new window popup
    with page.expect_popup() as page1_info:
        page.get_by_role("button", name="Submit").click()
    page1 = page1_info.value
    page1.wait_for_load_state()

    # Implement manual download and naming

    # ctx.close()
    # browser.close()
