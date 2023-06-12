import pyautogui
import win32gui
import random
import time
import os
import pyperclip 

DIV2CHAOS = 180
DIV2SIXTANT = 55

sixtant_value = dict()
pos_sixtant = dict()

watchstone_click_pos = (995,942)
sixtant_click_pos = (433,430)
ware_pos = (898,419)


def r():
    return random.uniform(0.1, 0.2)

def r_pos(pos, range=1):
    print(pos)
    return (pos[0]+random.randint(-range,range),pos[1]+random.randint(-range,range))

bag_start_pos = (1279, 593)
bag_end_pos = (1899, 844)
avr_x = (bag_end_pos[0] - bag_start_pos[0])/12
avr_y = (bag_end_pos[1] - bag_start_pos[1])/5
bag_pos_list = []
pos_x, pos_y = bag_start_pos[0] + avr_x/2, bag_start_pos[1] + avr_y/2
while pos_x < bag_end_pos[0]:
    while pos_y < bag_end_pos[1]:
        bag_pos_list.append(r_pos((pos_x, pos_y), range=3))
        pos_y = pos_y + avr_y
    pos_y = bag_start_pos[1] + avr_y/2
    pos_x = pos_x + avr_x

file_path = os.path.abspath(__file__)
file_root = os.path.dirname(file_path)
os.chdir(file_root)
have_sixtant = set()
with open('sixtant_value.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if not ':' in line:
            continue
        sixtant = line.split(':')[0]
        value = line.split(':')[1]
        sixtant_value[sixtant] = int(value)
    for line in f:
        if ':' not in line:
            continue
        sixtant = line.split(':')[0]
        have_sixtant.add(sixtant)
    
with open('pos_sixtant.txt', 'r', encoding='utf-8') as f:
    for line in f:
        pos = line.split(':')[0]
        sixtant = line.split(':')[1]
        pos_sixtant[pos] = sixtant

def cal_profit():
    value = 0
    
def click_sixtant():
    time.sleep(r())
    pyautogui.press('space')
    pyautogui.moveTo(r_pos(ware_pos), duration=r())
    pyautogui.click(button='left')
    time.sleep(r())
    pyautogui.moveTo(sixtant_click_pos, duration=r())
    pyautogui.keyDown('shift')
    time.sleep(r())
    pyautogui.click(button='right')
    pyautogui.press('g')
    pyautogui.moveTo(watchstone_click_pos, duration=r())
    time.sleep(r())    
    
def safe_click(button='left'):
    os.system('echo off | clip')
    time.sleep(0.5+r())
    while True:
        pyautogui.click(button=button)
        flag = 0
        while (not len(pyperclip.paste()) and flag < 2):
            pyautogui.hotkey('ctrl', 'c', interval=r())
            flag = flag + 1
        if not len(pyperclip.paste()):
            continue
        return pyperclip.paste()
    
def get_sixtant(info):
    # print(info.split('\n'))
    sixtant = info.split('\n')[6]
    return sixtant

def use_compass(compass_pos, bag_pos):
    itempos = r_pos(pyautogui.position())
    pyautogui.keyUp('shift')
    time.sleep(r())
    pyautogui.press('i')
    pyautogui.moveTo(r_pos(compass_pos), duration=r())
    pyautogui.click(button='right')
    time.sleep(r())
    pyautogui.moveTo(r_pos(itempos), duration=r())
    time.sleep(r())
    pyautogui.click(button='left')
    time.sleep(r())
    pyautogui.moveTo(bag_pos, duration=r())
    time.sleep(r())
    pyautogui.click(button='left')
    pyautogui.press('i')
    return r_pos(bag_pos)
             
def auto_sixtant(times=10, ignore= 0):
    sixtants = []
    compass_pos_list = [(1171,611)]
    click_sixtant()
    for i in range(times):
        info = safe_click()
        if not info:
            continue
        sixtant = get_sixtant(info)
        # if sixtant_value[sixtant] < ignore:
        #     continue
        sixtants.append(sixtant)
        item_pos = bag_pos_list.pop()
        use_compass(compass_pos_list[0] , r_pos(item_pos))
        time.sleep(r())
        click_sixtant()

    pyautogui.keyUp('shift')
    
    with open('sixtant_value.txt', 'a', encoding='utf-8') as f:
        for sixtant in sixtants:
            if sixtant not in have_sixtant:
                have_sixtant.add(sixtant)
                f.write(sixtant + '\n')
        
    return sixtants


if __name__ == '__main__':
    hld = win32gui.FindWindow(None,u"Path of Exile")
    win32gui.SetForegroundWindow(hld)
    time.sleep(1)
    auto_sixtant()
    pyautogui.keyUp('shift')