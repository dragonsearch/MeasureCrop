# MeasureCrop
Useful linux-only python tool I developed to gather data for my end of degree project.

It takes measures of a selected box using mouse position.

Takes a single filename as the first argument, then appends to it the selected area height and width along with a prompted word/line to describe it.

It can use a wordlist for the area names as second argument. (This wordlist will be formatted, you can (should) put sentences).

You may need to use 'xhost +' command for it to work (pyautogui errors).
