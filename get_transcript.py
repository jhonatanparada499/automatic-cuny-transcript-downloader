# get_transcript.py

import keyring, pyotp
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path.home() / "Downloads" / "jjay_transcript.pdf"

user = keyring.get_password("cuny", "username")
pw = keyring.get_password("cuny", "password")
totp = pyotp.TOTP(keyring.get_password("cuny", "totp_secret"))

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    ctx = p.chromium.launch_persistent_context(accept_downloads=True)
    page = ctx.new_page()
    page.goto("https://home.cunyfirst.cuny.edu")

    # --- Login (only runs if the session expired) ---
    if page.locator("input[autocomplete=username]").count():
        page.get_by_role("textbox", name="CUNY Login").fill(user)   # user
        page.get_by_role("textbox", name="Password").fill(pw)       # password
        page.get_by_role("button", name="Log in").click()           # submit

        # redirection to TOTP
        page.get_by_role("textbox", name="Enter TOTP from the").fill(totp.now())
        page.get_by_role("button", name="Verify").click()

        page.fill("input[name=otc]", totp.now())  # selector may differ
        page.click("input[type=submit]")
        # "Stay signed in?" prompt: say yes so the session persists
        try:
            page.click("input[type=submit]", timeout=5000)
        except Exception:
            pass

    # --- Navigate: Student Center -> Academics -> View Unofficial Transcript ---
    # Use `playwright codegen` to record the exact clicks (see below)

    # --- Capture the PDF ---
    with page.expect_popup() as popup_info:
        pass  # replace with the click that triggers "Go" on the transcript request
    popup = popup_info.value
    popup.wait_for_load_state()
    # Either it triggers a download, or it opens a PDF viewer URL:
    pdf = ctx.request.get(popup.url)
    OUT.write_bytes(pdf.body())
    print(f"Saved to {OUT}")
    ctx.close()
