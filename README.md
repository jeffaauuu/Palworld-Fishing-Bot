# Palworld-Fishing-Bot
Built a script to auto-fish in Palworld up to master difficulty with no assistance and grand master level if you have the correct fishing Pals. I got frustrated with the minigame and decided its time to automate it.

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
