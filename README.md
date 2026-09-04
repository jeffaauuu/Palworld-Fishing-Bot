# Palworld-Fishing-Bot
Built a script to auto-fish in Palworld up to master difficulty with no assistance and grand master level if you have the correct fishing Pals. I got frustrated with the minigame and decided its time to automate it.

# Install Dependencies
Install the required python libraries using the following command in your terminal.
```bash
pip install mss opencv-python pynput numpy pillow
```

# How to use
First, get the screen resolution of your monitor and identify the bar height (I did it using paint manually).
```python
MONITOR = {
    "left":   1920,        # monitor left edge
    "top":    -266 + 415,  # monitor top + our bar y start
    "width":  2560,        # full width
    "height": 25,          # just the bar height!
} 
```
Once done, run the game on your display and start the python script once you are ready. Cast your line into the fishing minigame area and start the minigame. Let the script do its thing and then enjoy the loot.

