import os
import re
import subprocess
import sys
import time


def ensure_deps() -> None:
    try:
        import selenium  # noqa: F401
        import webdriver_manager  # noqa: F401
        return
    except Exception:
        pass

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "selenium", "webdriver-manager"]
    )


def build_driver(profile_dir: str):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager

    options = Options()
    options.add_argument(f"--user-data-dir={profile_dir}")
    options.add_argument("--profile-directory=Default")

    service = webdriver.chrome.service.Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def is_roblox_running() -> bool:
    result = subprocess.run(
        'tasklist /FI "IMAGENAME eq RobloxPlayerBeta.exe"',
        capture_output=True,
        text=True,
        shell=True,
    )
    return "RobloxPlayerBeta.exe" in result.stdout


def click_play(driver, url: str) -> None:
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    driver.get(url)

    # If login is required, Roblox shows a Log In button in the top nav.
    try:
        login_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "navbar-login-button"))
        )
    except TimeoutException:
        login_button = None

    if login_button is not None:
        raise RuntimeError("Not logged in. Please log in in the opened Chrome window.")

    button_candidates = [
        (By.ID, "game-join-btn"),
        (By.CSS_SELECTOR, 'button[data-testid="play-button"]'),
        (By.CSS_SELECTOR, 'button[data-testid="play-button__play"]'),
        (By.CSS_SELECTOR, 'button#game-join-btn'),
    ]

    for by, selector in button_candidates:
        try:
            button = WebDriverWait(driver, 12).until(
                EC.element_to_be_clickable((by, selector))
            )
            button.click()
            return
        except TimeoutException:
            continue

    raise RuntimeError("Could not find the Play button on the Roblox page.")


def main() -> int:
    prompt = "Enter roblox GameID or VIP server link: "
    user_input = input(prompt).strip()
    if not user_input:
        print("No input provided.")
        return 1

    if re.fullmatch(r"\d+", user_input):
        url = f"https://www.roblox.com/games/{user_input}"
    else:
        url = user_input

    ensure_deps()
    profile_dir = os.path.join(os.getcwd(), "chrome_profile")
    os.makedirs(profile_dir, exist_ok=True)
    print("Watching Roblox process. It will rejoin when it closes.")

    while True:
        driver = build_driver(profile_dir)
        try:
            click_play(driver, url)
        except Exception as exc:
            print(f"Failed to launch Roblox: {exc}")
            print("Make sure you're logged in on the opened Chrome window.")
            driver.quit()
            time.sleep(5)
            continue

        # Wait for Roblox to start, then wait for it to exit.
        while not is_roblox_running():
            time.sleep(1)

        driver.quit()

        while is_roblox_running():
            time.sleep(3)

        time.sleep(5)


if __name__ == "__main__":
    raise SystemExit(main())
