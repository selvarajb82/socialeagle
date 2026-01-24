import pyautogui
import time


def focus_browser():
    w, h = pyautogui.size()
    pyautogui.click(w//2, h//2)
    time.sleep(0.5)


def focus_page_body():
    # Scroll down to force page focus
    pyautogui.scroll(-300)
    time.sleep(0.3)

    # Click LOWER part of page (safe zone)
    w, h = pyautogui.size()
    pyautogui.click(w//2, int(h*0.7))
    time.sleep(0.5)


# res = pyautogui.locateOnScreen("edit.png", confidence=0.8)

# print(res)

# center_of_res = pyautogui.center(res)

# print(center_of_res)

# # =np.int64 --- appears like this because numpy was installed.. it is valid. to convert to integer.. refer below

# x = int(center_of_res.x)

# y = int(center_of_res.y)

# print(f"{x} , {y}")


# res2 = pyautogui.locateCenterOnScreen("edit.png", confidence=0.8)

# print(res2)

# pyautogui.moveTo(res2)

'''
1.open a new Tab in web browser
2.search for youtube.com
3.search for the channel you want to subscribe
4.click on the channel
5.click on the subscription

'''
channel_name = pyautogui.prompt(text="", title="enter the channel name")
print(channel_name)

focus_browser()

pyautogui.sleep(3)

# Focus browser address bar
pyautogui.hotkey("ctrl", "l")
time.sleep(0.5)

# open new tab in web browser
pyautogui.hotkey("ctrl", "t")

pyautogui.sleep(3)

pyautogui.write("https://www.youtube.com/")
pyautogui.hotkey("enter")

pyautogui.sleep(5)

# search2 = pyautogui.locateCenterOnScreen("youtube_search.png")

# print(search2)

# pyautogui.moveTo(search2, 1)
# pyautogui.click()


# Use YouTube's keyboard shortcut to focus search box (much more reliable!)
pyautogui.press("/")  # YouTube shortcut to focus search
time.sleep(0.5)

pyautogui.write(channel_name)
time.sleep(0.5)

# Press Enter to search
pyautogui.hotkey("enter")


time.sleep(3)

focus_browser()

#  x, y = pyautogui.locateCenterOnScreen("Thiru_with_AI.png", confidence=0.9)

# print(search2)

channel = pyautogui.locateCenterOnScreen("Thiru_with_AI.png", confidence=0.5)

if channel:
    pyautogui.moveTo(channel, duration=1)
    pyautogui.click()
else:
    print("Channel image not found")

    # pyautogui.moveTo(channel, duration=1)
    # pyautogui.click()


time.sleep(2)

focus_browser()

time.sleep(2)

# focus_page_body()

# Scroll up to ensure Subscribe button is visible
pyautogui.scroll(500)
time.sleep(1)

# Try to find the button
subscribe2 = pyautogui.locateCenterOnScreen(
    "Subscribe2.png", confidence=0.7, grayscale=True)

if subscribe2:
    print(f"Found Subscribe button at: {subscribe2}")
    pyautogui.moveTo(subscribe2, duration=1)
    pyautogui.click()
else:
    print("Subscribe button not found - trying alternative method")
    # Alternative: Use Tab key to navigate to Subscribe button
    pyautogui.press('tab', presses=5, interval=0.3)
    time.sleep(0.5)
    pyautogui.press('enter')


# subscribe2 = pyautogui.locateCenterOnScreen("Subscribe2.png", confidence=0.5)

# if subscribe2:
#     pyautogui.moveTo(subscribe2, duration=1)
#     pyautogui.click()
# else:
#     print("Subscribe button not found")

# if x is None:
#     print("Channel logo not found 😭")
#     exit()

# pyautogui.moveTo(channel, duration=1)
# pyautogui.click()

# pyautogui.moveTo(x, y, 1)
# pyautogui.click()

time.sleep(1)


# x, y = pyautogui.locateCenterOnScreen("Subscribe.png", confidence=0.9)

# # print(search2)

# pyautogui.moveTo(x, y, 1)
# pyautogui.click()
