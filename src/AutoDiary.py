import os
import pyautogui
import win32gui
import pyperclip
import random
import time
key_value = { '区域内残骸数量提高': 40,
              '爆炸范围扩大': 40,
              '爆炸物数量提高': 50,
              '发掘的箱子有' : 25,
              '残骸有': 40,
              '炸药放置范围扩大': 40,
              '区域内怪物之印的数量提高': 50,
              '区域内符纹怪物之印的数量提高': 40,
              '区域内额外有': 16,
              '怪物掉落的神器数量提高': 40}

key_weights = {'区域内残骸数量提高': 1,
               '爆炸范围扩大': 1,
               '爆炸物数量提高': 1.3,
               '发掘的箱子有' : 2,
               '残骸有': 1.1,
               '炸药放置范围扩大': 0.8,
               '区域内怪物之印的数量提高': 1.5,
               '区域内符纹怪物之印的数量提高': 1.2,
               '区域内额外有': 2.2,
               '怪物掉落的神器数量提高': 1.2}

no_wants = ('药剂','冷却','元素伤害','总回复速度')

def r():
    return random.uniform(0.01, 0.03)

def get_pos():
    item_pos = []
    start_pos = (1273,589)
    end_pos = (1903,847)
    avr_x = (end_pos[0]-start_pos[0])/12
    avr_y = (end_pos[1]-start_pos[1])/5
    posx, posy = 1294, 612
    while posx < end_pos[0]:
        while posy < end_pos[1]:
            item_pos.append((posx + random.randint(-2,2), posy + random.randint(-2,2)))
            posy += avr_y
        posx += avr_x
        posy = 612
    return item_pos
    
def get_info(item_pos):
    ans = []
    for pos in item_pos:
        pyautogui.moveTo(pos,duration=r())  
        os.system('echo off | clip')
        pyautogui.hotkey('ctrl','c',interval=r())
        flag = 0
        while not len(pyperclip.paste()) and flag < 5:
            flag += 1
            pyautogui.hotkey('ctrl','c',interval=r())
            time.sleep(r())
        if not len(pyperclip.paste()):
            continue
        info = pyperclip.paste()
        if check(info):
            ans.append(pos)
    return ans
    
def check(info):
    text = info.split('-')
    for area in text:
            if len(area) and '黑镰' in area:
                line = area.split('\n')
                area_value = 0
                for needline in line:
                    if '%' in needline:
                        line_type = needline.split(' ')[0]
                        area_value += key_value[line_type] * key_weights[line_type]
                now_value = 0  
                for needline in line:
                    if '%' in needline:
                        line_type = needline.split(' ')[0]
                        line_value = int(needline.split(' ')[1].strip('%'))
                        now_value += line_value * key_weights[line_type]
                with open('AutoDiary.txt','a',encoding='utf-8') as f:
                    f.write(info)
                    f.write(f'now_value is {now_value}  need value is {area_value*0.75}')
                    f.write('\n-------------------------------------------\n')
                # print (f'now_value is {now_value}  need value is {area_value*0.75}')
                if now_value >= area_value*0.8:
                    return True
    return False

if __name__ == '__main__':
    # with open ('eg.txt','r',encoding='utf-8') as f:
    #     info = f.read()
    #     if check(info):
    #         print ('True')
    #     else: print(False)
    hld = win32gui.FindWindow(None,u"Path of Exile")
    win32gui.SetForegroundWindow(hld)
    
    item_pos = get_pos()
    get_info(item_pos)
    # ans = get_info(item_pos)
    # pyautogui.keyDown('ctrl')
    # pyautogui.keyDown('shift')
    # for pos in ans:
    #     pyautogui.moveTo(pos,duration=r())
    #     time.sleep(0.2+r())
    #     pyautogui.click(button='left')
        