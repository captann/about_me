from pyautogui import screenshot
import os, time, shutil
if not os.path.isdir("Skreens"):
    os.mkdir("Skreens")
os.chdir(".\Skreens")
count = 0
command = "run"
while command != "stop":
    while os.path.isfile(f"Screen{str(count)}.jpg"):
        count += 1
    screenshot(f"Screen{str(count)}.jpg")
    count = 0
    command = input("Для остановки введите stop... ")
os.chdir('..')
shutil.rmtree(r".\Skreens")
