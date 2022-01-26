"""

Simple program to take measures of a selected box using mouse position

It takes a single filename as the first argument, then appends to it the selected area height and width along with a prompted word/line to describe it.

It can use a wordlist for the area names as second argument. (This wordlist will be formatted, you can even put sentences).

You may need to use 'xhost +' command for it to work (pyautogui errors).

"""

import pyautogui
from PIL import Image
import pyscreenshot as img
import sys
import keyboard
import re
from os import path

filename = sys.argv[1] if len(sys.argv) > 1 else exit()
use_wordlist = True if len(sys.argv) > 2 else False

file_wordlist = sys.argv[2] if use_wordlist else "dummy.txt"

if use_wordlist:
    with open(file_wordlist,"r") as wl:
        wordlistaux = wl.read().splitlines()
        wordlist = []
        for line in wordlistaux:
            extended_line = re.sub(r"[\-\/!?¿¡;,:.·\"\'()&%$€ºª=]","",line).split(" ", 1)    #.split()[1:]
            # I could use unicodedata to transliterate to closest ascii but it can fail on some characters so I prefered not to.
            # Looping through the characters in order to change accents
            # This is thought for a spanish text so you can do whatever you want here to handle accents for other languages.
            formatted_line = ""
            for char in extended_line[1]:
                if char in ('é','í','ó','ú'):
                    formatted_line+=chr(ord(char)-132)
                elif char == 'á':
                    formatted_line+='a'
                elif char == 'ü':
                    formatted_line+='u'
                else:
                    formatted_line+=char
            #extended_line = extended_line.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ü","u")
            wordlist.extend(formatted_line.split())
    nextword = 0
    if path.isfile('lastwordindex.txt'):
        with open('lastwordindex.txt') as lwi:
            nextword = int(lwi.readline().split()[0])        


while True:
    with open(f"{filename}","a+") as output:
        try:
             # START CAPTURING WITH C
            while True:
                if keyboard.read_key() == "c":
                    break;
            first = pyautogui.position()
            # FINISH CAPTURING WITH X
            while True:
                if keyboard.read_key() == "x":
                    break;
            second = pyautogui.position()
            #GRAB THE AREA OF THE SCREEN 
            image = img.grab(bbox=(first[0],first[1],second[0],second[1]))
            image.save('temp.png')
            Image.open('temp.png').show()
            
	    # PROMPT OF CONFIRMATION FOR THE SCREENSHOT

            print("Do you like it? Type y or n: ")
            confirm = True
            while True:
                yes_no = input()
                if yes_no == "y":
                    break;
                if yes_no == "n":
                    confirm = False
                    break;
	    # RETURN TO SELECTION
            if not confirm: continue
            
            #PROMP OF CONFIRMATION FOR NAME
            unliked = False
            confirm = False
            while not confirm:
                if use_wordlist:
                    if unliked: print("Type a name for the area:")
                    boxname = wordlist[nextword] if not unliked else input()
                else:
                    print("Type a name for the area:")
                    boxname = input()


                print(f"Box name: {boxname} ")

                print("Do you like it? Press y or n")
                while True:
                    yes_no = input()
                    if yes_no == "y":
                            confirm = True
                            break;
                    if yes_no == "n":
                            unliked = True
                            break;


            word = boxname
            height = abs(first[1]-second[1])
            width = abs(first[0]-second[0])


            print(f"Height: {height} Width: {width}")

            output.write(f"{word} {height} {width} \n") # Bbox = {first[0]},{first[1]} | {second[0]},{second[1]} \n")
            with open('lastwordindex.txt', 'w+') as lwi:
                lwi.write(str(nextword+1) + ' ' + wordlist[nextword])
            if use_wordlist: nextword += 1
            
        except BaseException as e:
            print("Exception, remember to take areas from upper-left to bottom-right corners \n To exit use CTRL+Z\n")
            print(str(e))












