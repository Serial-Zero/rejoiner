# Rejoiner

Simple Roblox rejoiner that monitors the Roblox client process and relaunches the game when it closes.

## Requirements
- Windows
- Python 3.9+
- Google Chrome

Dependencies are auto-installed on first run:
- `selenium`
- `webdriver-manager`

## Usage
```powershell
python Rejoiner.py
```

When prompted, enter a Roblox GameID (numbers only) or a VIP server link. A Chrome window will open, click Play, then close once Roblox starts. The script will rejoin automatically when the game closes.

## Notes
- Login is stored in `chrome_profile/` so you only need to log in once.
- If the script says you are not logged in, sign in in the opened Chrome window, then rerun.

## Files
- `Rejoiner.py`
- `.gitignore`
