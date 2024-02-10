import tkinter as tk
from tkinter import messagebox
import pyautogui
import pyperclip
import re
import math
import time
import configparser
import win32con
import win32gui
from pynput import keyboard
import json
from PIL import ImageGrab
import numpy as np
# pyautogui固定停顿
########################################################
# Stash mode:
# 1 ： 手动放到TAB_NUM
# 2: 自动从1开始，满了向后翻页直到10
#******************************************
# 开始时第一个格子的六分仪数量，默认5000,启动时必须更新
# 开始时第一个格子的六分仪数量，默认5000,启动时必须更新
# 开始时第一个格子的六分仪数量，默认5000,启动时必须更新
#******************************************
START_SEXTANT_AMOUNT = 5000
# MOD
STASH_MODE = 2
# 放到几号tab
TAB_NUM = 2
# F4点几个背包的六分
NUM_OF_PACK_PER_TIME = 40 # (60*x 个罗盘)
# 每次F6 移动的物品数量上限
NUM_PER_MOV = 10
# autogui默认停顿时间
pyautogui.PAUSE = 0.07
SLEEPTIME = 0.02
##########################################

import random
def random_sleep(x,y):
    #return SLEEPTIME
    time.sleep(random.uniform(x, y))
    return random.uniform(x, y)

# 返回+-16范围内的随机坐标
def quick_exit():
    pyautogui.press('enter')
    time.sleep(0.5)
    # 输入字符串 "/exit"
    pyautogui.write('/exit')
    time.sleep(0.5)
    pyautogui.press('enter')
def around_pos(pos):
    pos = toIntpos(pos)
    random_x = pos[0] + random.randint(-10, 10)
    random_y = pos[1] + random.randint(-10, 10)
    return [random_x, random_y]
def random_area_click():
    # 1.记录当前位置,
    start_pos = pyautogui.position()
    # 2. 点击随机位置2-4次
    # 保存初始鼠标位置
    clicks = random.randint(2,3)
    for _ in range(clicks):
        # 生成矩形范围内的随机坐标
        x = random.randint(random_clcik_left_up[0], random_clcik_right_down[0])
        y = random.randint(random_clcik_left_up[1], random_clcik_right_down[1])
        # 移动到随机坐标并点击
        move_to_randomly([x,y], steps=5, speed=0.08)
        pyautogui.click(button='left')
    # 移动回初始位置
    move_to_randomly(start_pos, steps=3, speed=0.08)
    # 3.回到原来位置
def move_to_randomly(pos, steps=10, speed=0.1):
    # 获取当前鼠标位置
    start_pos = pyautogui.position()
    pos = toIntpos(pos)
    if speed == 0.1:
        speed = random.uniform(0.1, 0.15)
    if steps == 10:
        steps = int(random.randint(5,10))
    # 计算每一步的移动距离
    step_x = (pos[0] - start_pos[0]) / steps
    step_y = (pos[1] - start_pos[1]) / steps

    for i in range(1, steps + 1):
        # 计算下一个目标点
        target_x = start_pos[0] + step_x * i
        target_y = start_pos[1] + step_y * i

        # 添加随机偏移
        random_x = random.randint(-50, 50)
        random_y = random.randint(-50, 50)

        # 移动鼠标到目标位置，指定移动速度

        pyautogui.moveTo(target_x + random_x, target_y + random_y, duration=speed/10)

    # 最后移动到准确的目标位置
    pyautogui.moveTo(pos, duration=speed)

# 把字符串pos 转换成int pos
def toIntpos(pos):
    return [int(pos[0]), int(pos[1])]
# 获取坐标组
def get_color():
    # 获取鼠标指针的当前位置
    x, y = pyautogui.position()
    # 获取鼠标指针位置处的颜色（RGB值）
    pixel_color = pyautogui.pixel(x, y)
    return pixel_color
    # 打印RGB颜色值
    # print(f"鼠标指针位置 ({x}, {y}) 处的颜色为 RGB: {pixel_color}")

# 注：
# 同一个物品似乎在仓库中有不止一种像素颜色，在小仓库和大仓库的颜色也不相同
def get_filtered_pos():
    # 目标rgb
    # 六分仪独特颜色
    target_color_1 = np.array([44, 23, 28])
    target_color_2 = np.array([232, 62, 62])
    target_color_3 = np.array([228, 26, 20])
    target_color_4 = np.array([224, 49, 32])

    target_color_5 = np.array([190,35,23])
    target_color_6 = np.array([204, 21, 5])
    target_color_7 = np.array([115, 22, 4])
    target_color_8 = np.array([189, 80, 63])
    # target_color = np.array([177, 108, 72])
    # 定义区域的左上角和右下角坐标
    left_top = (tab_left_up[0], tab_left_up[1])
    right_bottom = (tab_right_down[0], tab_right_down[1])
    region = (*left_top, *right_bottom)
    screenshot = pyautogui.screenshot(region=region)
    # screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    screenshot.save("screenshot.png")
    screenshot_array = np.array(screenshot)

    matching_pixels_1 = np.all(screenshot_array == target_color_1, axis=-1)
    matching_pixels_2 = np.all(screenshot_array == target_color_2, axis=-1)
    matching_pixels_3 = np.all(screenshot_array == target_color_3, axis=-1)
    matching_pixels_4 = np.all(screenshot_array == target_color_4, axis=-1)

    matching_pixels_5 = np.all(screenshot_array == target_color_5, axis=-1)
    matching_pixels_6 = np.all(screenshot_array == target_color_6, axis=-1)
    matching_pixels_7 = np.all(screenshot_array == target_color_7, axis=-1)
    matching_pixels_8 = np.all(screenshot_array == target_color_8, axis=-1)

    matching_pixels = np.logical_or(matching_pixels_1, matching_pixels_2)
    matching_pixels = np.logical_or(matching_pixels, matching_pixels_3)
    matching_pixels = np.logical_or(matching_pixels, matching_pixels_4)
    matching_pixels = np.logical_or(matching_pixels, matching_pixels_5)
    matching_pixels = np.logical_or(matching_pixels, matching_pixels_6)
    matching_pixels = np.logical_or(matching_pixels, matching_pixels_7)
    matching_pixels = np.logical_or(matching_pixels, matching_pixels_8)

    y_indexes, x_indexes = np.nonzero(matching_pixels)
    absolute_coordinates = [[x + left_top[0], y + left_top[1]] for x, y in zip(x_indexes, y_indexes)]
    return absolute_coordinates


def move_filtered_compass_to_inv():
    pyautogui.PAUSE = 0.01
    poses = get_filtered_pos()
    count = 0
    for i in poses:
        # pyautogui.moveTo(i, duration=0.1)
        move_to_randomly(i, steps=10, speed=0.08)
        move_item_to_or_from_stash()
        count += 1
        if count >= NUM_PER_MOV:
            break
    pyautogui.PAUSE = 0.07
def load_blacklist(filename):
    with open(filename, 'r') as file:
        blacklist_data = json.load(file)
    return blacklist_data["blacklist"], blacklist_data["whitelist"], blacklist_data["stop_condition"]

# 从获取指针上的物品信息
def get_item_info():
    pyautogui.hotkey('ctrl', 'c')
    # time.sleep(0.2)
    random_sleep(0.2, 0.3)
    info = pyperclip.paste().replace('\r', '')
    random_sleep(0.1, 0.15)
    return info
# 从复制的文本中提取 六分仪第一行词缀
def get_void_stone_suffix(info):
    pattern = r'Item Level: 8[0-9]\n-{8}\n(.+?)\n'
    # pattern 后面第三行就是 六分仪词缀的第一行
    match = re.search(pattern, info)
    if match:
        #first_line = match.group(2)
        return match.group(1)
    else:
        return "not match anything"
#
def isinBlacklist(str):
    # 1. 字符串re匹配所有黑名单中的数字
    # 2.如果存在 return true
    # 3. return false
    return str in blacklist

def is_stop_condition(str):
    return str in stop_condition

# 指针物品是否被屏蔽
def is_item_in_blacklist():
    info = get_item_info()
    suffix = get_void_stone_suffix(info)
    # 如果虚空石头本身词缀，抛出异常停止
    if is_stop_condition(info):
        print("六分仪耗尽")
        quick_exit()
        # 退出游戏
        raise pyautogui.FailSafeException("FailSafe triggered manually.")
    if isinBlacklist(suffix):
        print("yes",suffix)
    else:
        print("no",suffix)
    return isinBlacklist(suffix), suffix

def collect_suffix():
    info = get_item_info()
    suffix = get_void_stone_suffix(info)
    # print("***")
    # print(suffix)
    if isinBlacklist(suffix):
        print("yes",suffix)
    else:
        print("no",suffix)
    # tk.messagebox.showinfo("第一行词缀：", suffix)

def show_alert():
    tk.messagebox.showinfo("提示", "这是一个弹窗提示！")
# 仅作写法参考 不被调用
def base_ref():
    pyautogui.moveTo(pos_void_stone, duration=0.1)
    pyautogui.click(button='right')
    pyautogui.moveTo(pos_void_stone, duration=0.1)
    pyautogui.click()
# 仓库打开时移动到货币tab
def goto_currency_tab():
    #pyautogui.moveTo(Currency_folder, duration=0.1)
    move_to_randomly(Currency_folder, steps=5, speed=0.1)
    pyautogui.click(button='left')
    #pyautogui.moveTo(Currency_tab, duration=0.1)
    move_to_randomly(Currency_tab, steps=5, speed=0.1)
    pyautogui.click(button='left')
# 仓库打开时，移动到特定的compass tab
# index : 1-10
def goto_compass_tab(index):
    #pyautogui.moveTo(Compass_folder, duration=0.1)
    move_to_randomly(Compass_folder, steps=5, speed=0.1)
    pyautogui.click(button='left')
    random_sleep(0.2,0.5)
    # pyautogui.moveTo(list_compass_tab[index-1], duration=0.1)
    move_to_randomly(list_compass_tab[index-1], steps=10, speed=0.1)
    pyautogui.click(button='left')
    random_sleep(0.5, 0.6)
def move_item_to_or_from_stash():
    pyautogui.keyDown('ctrl')
    # 模拟鼠标左键点击（这个点击将会在按下Ctrl键的同时发生）
    pyautogui.click()
    # 松开Ctrl键
    pyautogui.keyUp('ctrl')
    # pyautogui.hotkey('ctrl', 'left')
def stash_mode_roll_sextant(sexntant_count):
    pos_init = pos_inv_1_1
    col = 0
    last_suffix = ""
    repeat_count = 0
    while col < 5:
        index = 0
        while index < 12:
            # print("index =", index)
            # use sextant
            if sexntant_count < START_SEXTANT_AMOUNT:
                # pyautogui.moveTo(pos_sextant, duration=0.05)
                move_to_randomly(around_pos(pos_sextant), steps=5, speed=0.01)
                pyautogui.click(button='right')
                sexntant_count += 1
                # 每1000次随机休息50-200秒
                if (sexntant_count % 1000)==0:
                    random_sleep(50,200)
                print("sexntant_count",sexntant_count)
            # 当六分仪数量大于5000时，点第二个六分仪位置
            elif sexntant_count >=START_SEXTANT_AMOUNT and sexntant_count < 10000:
                # pyautogui.moveTo(pos_sextant_2, duration=0.1)
                move_to_randomly(around_pos(pos_sextant_2), steps=5, speed=0.01)
                pyautogui.click(button='right')
                sexntant_count += 1
                if (sexntant_count%1000)==0:
                    random_sleep(50,200)
                print("sexntant_count", sexntant_count)

            # pyautogui.moveTo(pos_void_stone, duration=0.1)
            move_to_randomly(around_pos(pos_void_stone), steps=5, speed=0.01)
            pyautogui.click(button='left')
            #time.sleep(0.05)
            random_sleep(0.05,0.1)
            is_black, suffix = is_item_in_blacklist()
            if last_suffix == suffix:
                repeat_count += 1
            else:
                repeat_count = 0
            if repeat_count > 3:
                print("六分仪耗尽")
                #退出游戏
                quick_exit()
                raise pyautogui.FailSafeException("FailSafe triggered manually.")


            if not is_black:
                # use compass
                #pyautogui.moveTo(pos_compass, duration=(0.1))
                move_to_randomly(around_pos(pos_compass), steps=3, speed=0.05)
                pyautogui.click(button='right')
                random_sleep(0.05,0.1)
                # time.sleep(0.05)
                #pyautogui.moveTo(pos_void_stone, duration=0.1)
                move_to_randomly(around_pos(pos_void_stone), steps=3, speed=0.05)
                pyautogui.click(button='left')
                random_sleep(0.05, 0.1)
                # time.sleep(0.05)
                # place compass
                place_compass_pos = [pos_init[0]+(delta_slot * index), pos_init[1]]
                #pyautogui.moveTo(place_compass_pos, duration=0.1)
                move_to_randomly(around_pos(place_compass_pos), steps=3, speed=0.05)
                pyautogui.click(button='left')
                # 每完成一次有1/10的概率随机点击
                if random.randint(1, 15) == 1:
                    random_area_click()
                index += 1
            last_suffix = suffix
            # finish
        col += 1
        # print("col =",col)
        # x回到初始值，y + 1 del
        pos_init = [pos_inv_1_1[0], pos_init[1] + delta_slot]
    return sexntant_count

def clear_pack_to_stash():
    # 1
    # goto_compass_tab(TAB_NUM)
    pyautogui.PAUSE = 0.01
    current_pos = pos_inv_1_1
    col = 0
    while col < 5:
        for index in range(12):
            # place compass
            place_compass_pos = [current_pos[0] + (delta_slot * index), current_pos[1]]
            move_to_randomly(around_pos(place_compass_pos), steps=3, speed=0.05)
            #pyautogui.moveTo(around_pos(place_compass_pos), duration=0.06)
            # 移动到仓库
            move_item_to_or_from_stash()
        col += 1
        # print("col =",col)
        # x回到初始值，y + 1 del
        current_pos = [pos_inv_1_1[0], current_pos[1] + delta_slot]
    pyautogui.PAUSE = 0.07
def stash_mode_put_into_tab():
    # 1
    if STASH_MODE == 1:
        goto_compass_tab(TAB_NUM)
        current_pos = pos_inv_1_1
        col = 0
        while col < 5:
            for index in range(12):
                # place compass
                place_compass_pos = [current_pos[0] + (delta_slot * index), current_pos[1]]
                pyautogui.moveTo(place_compass_pos, duration=0.05)
                # 移动到仓库
                move_item_to_or_from_stash()
            col += 1
            # print("col =",col)
            # x回到初始值，y + 1 del
            current_pos = [pos_inv_1_1[0], current_pos[1] + delta_slot]
    elif STASH_MODE == 2:
        # TODO
        # 翻页到tab1
        # 循环放置
        # 每次放置钱获取当前鼠标颜色1
        # 点击后路检测颜色2
        # 如果颜色1 = 颜色2， 说明当前tab已满， index += 1, 如果index > 10 ，抛出异常停止翻到下一页，并重新尝试放置
        #
        tab_num = 1
        goto_compass_tab(tab_num)
        current_pos = pos_inv_1_1
        col = 0
        while col < 5:
            index = 0
            while index < 12:
                # place compass
                place_compass_pos = [current_pos[0] + (delta_slot * index), current_pos[1]]
                #pyautogui.moveTo(place_compass_pos, duration=0)
                move_to_randomly(around_pos(place_compass_pos), steps=4, speed=0.06)
                # 获取颜色1
                isSamecolor = True
                while isSamecolor == True:
                    color_before = get_color()
                    # 移动到仓库
                    move_item_to_or_from_stash()
                    # 获取颜色2
                    random_sleep(0.05,0.1)
                    color_after = get_color()
                    random_sleep(0.05, 0.1)
                    isSamecolor = (color_before == color_after)
                    if isSamecolor:
                        # 翻页
                        tab_num += 1
                        goto_compass_tab(tab_num)
                        # 回到格子坐标
                        move_to_randomly(around_pos(place_compass_pos), steps=4, speed=0.06)
                        #pyautogui.moveTo(place_compass_pos, duration=0.06)
                        # time.sleep(0.1)
                #print(color_before,color_after,type(color_before), color_before== color_after)
                index += 1
            col += 1
            # print("col =",col)
            # x回到初始值，y + 1 del
            current_pos = [pos_inv_1_1[0], current_pos[1] + delta_slot]
        #完成一包六分仪后随机sleep5-10秒
        random_sleep(3,10)
def stash_mode_start():
    print("stash_mode run")
    pyautogui.PAUSE = 0.08
    # 初始化六分仪点击次数
    sexntant_count = 0
    for i in range(NUM_OF_PACK_PER_TIME):
        # init stash tab
        # 1. 打开仓库货币页
        goto_currency_tab()
        # 2. 洗一背包六分仪
        sexntant_count = stash_mode_roll_sextant(sexntant_count)
        # 3. 放入仓库
        stash_mode_put_into_tab()
        print("已经生产",i,"背包")
    pyautogui.PAUSE = 0.01

def inv_mode_start():
    print("stash_mode run")
    col = 0
    init_click_pos = [pos_inv_1_1[0], pos_inv_1_1[1] - delta_slot]
    pyautogui.moveTo(init_click_pos, duration=0.4)
    pyautogui.click(button='left')

    sextant_pos = pos_inv_1_1
    compass_pos = [sextant_pos[0]+(delta_slot * 1), sextant_pos[1]]
    while col < 5:
        for index in range(12):
            # print("index =", index)
            # use sextant
            pyautogui.moveTo(sextant_pos, duration=0.1)
            pyautogui.click(button='right')
            pyautogui.moveTo(pos_void_stone, duration=0.1)
            pyautogui.click(button='left')

            # use compass
            pyautogui.moveTo(compass_pos, duration=0.1)
            pyautogui.click(button='right')
            pyautogui.moveTo(pos_void_stone, duration=0.1)
            pyautogui.click(button='left')

            # place compass
            place_compass_pos = [sextant_pos[0]+(delta_slot * (2 + index)), sextant_pos[1]]
            pyautogui.moveTo(place_compass_pos, duration=0.1)
            pyautogui.click(button='left')
            # finish
        col += 1
        # print("col =",col)
        sextant_pos = [sextant_pos[0], sextant_pos[1] + delta_slot]
        compass_pos = [sextant_pos[0] + (delta_slot * 1), sextant_pos[1]]

if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read('config.ini', encoding='utf-8')

    blacklist_filename = "sextant_blacklist.json"
    blacklist, whitelist, stop_condition = load_blacklist(blacklist_filename)

    pyautogui.FAILSAFE = True
    # 第一个格子位置 [x,y]
    pos_inv_1_1 = conf['coordinate']['InventorySlot_1_1'].split(',')
    pos_inv_1_1 = toIntpos(pos_inv_1_1)
    # 格子间隔
    delta_slot = conf['coordinate']['Delta_Slot']
    delta_slot = int(delta_slot)
    # 虚空石头位置
    pos_void_stone = conf['coordinate']['Down_void_stone'].split(',')
    pos_void_stone = toIntpos(pos_void_stone)

    # pos_sextant
    pos_sextant = conf['coordinate']['Sextant'].split(',')
    pos_sextant_2 = conf['coordinate']['Sextant_2'].split(',')
    # pos_compass
    pos_compass = conf['coordinate']['Compass'].split(',')

    # currency_folder
    Currency_folder = conf['coordinate']['Currency_folder'].split(',')
    Currency_folder = toIntpos(Currency_folder)
    # Currency_tab
    Currency_tab = conf['coordinate']['Currency_tab'].split(',')
    # pos_compass folder
    Compass_folder = conf['coordinate']['Compass_folder'].split(',')
    # 大仓库
    # pos_compass
    list_compass_tab =[]
    Compass_tab_s1 = conf['coordinate']['Compass_tab_s1'].split(',')
    # pos_compass
    list_compass_tab.append(Compass_tab_s1)
    Compass_tab_s2 = conf['coordinate']['Compass_tab_s2'].split(',')
    list_compass_tab.append(Compass_tab_s2)
    # pos_compass
    Compass_tab_s3 = conf['coordinate']['Compass_tab_s3'].split(',')
    list_compass_tab.append(Compass_tab_s3)
    # pos_compass
    Compass_tab_s4 = conf['coordinate']['Compass_tab_s4'].split(',')
    list_compass_tab.append(Compass_tab_s4)
    # pos_compass
    Compass_tab_s5 = conf['coordinate']['Compass_tab_s5'].split(',')
    list_compass_tab.append(Compass_tab_s5)
    # 普通仓库
    # pos_compass
    Compass_tab_1 = conf['coordinate']['Compass_tab_1'].split(',')
    list_compass_tab.append(Compass_tab_1)
    # pos_compass
    Compass_tab_2 = conf['coordinate']['Compass_tab_2'].split(',')
    list_compass_tab.append(Compass_tab_2)
    # pos_compass
    Compass_tab_3 = conf['coordinate']['Compass_tab_3'].split(',')
    list_compass_tab.append(Compass_tab_3)
    # pos_compass
    Compass_tab_4 = conf['coordinate']['Compass_tab_4'].split(',')
    list_compass_tab.append(Compass_tab_4)
    # pos_compass
    Compass_tab_5 = conf['coordinate']['Compass_tab_5'].split(',')
    list_compass_tab.append(Compass_tab_5)
    # 仓库tab 左上和右下坐标
    tab_left_up  = conf['coordinate']['tab_left_up'].split(',')
    tab_left_up = toIntpos(tab_left_up)
    tab_right_down = conf['coordinate']['tab_right_down'].split(',')
    tab_right_down = toIntpos(tab_right_down)

    # 随机点击区域左上和右下坐标
    random_clcik_left_up  = conf['coordinate']['random_clcik_left_up'].split(',')
    random_clcik_left_up = toIntpos(random_clcik_left_up)
    random_clcik_right_down = conf['coordinate']['random_clcik_right_down'].split(',')
    random_clcik_right_down = toIntpos(random_clcik_right_down)


    window = tk.Tk()
    window.title('自动六分仪')
    sw = window.winfo_screenwidth()  # 得到屏幕宽度
    sh = window.winfo_screenheight()  # 得到屏幕高度
    ww = 600
    wh = 400
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    window.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    tk.Label(window, text="""deleted""", bg='yellow', font=('Arial', 10), width=50,
             height=30).pack(side='left')
    Button_Start = tk.Button(window, text="背包模式", font=('Arial', 12), width=10, height=1, command=inv_mode_start). \
        place(x=440, y=200)


    # 增加快捷键
    def on_key_release(key):
        if key == keyboard.Key.f4:
            stash_mode_start()
        if key == keyboard.Key.f6:
            move_filtered_compass_to_inv()
        if key == keyboard.Key.f7:
            clear_pack_to_stash()
        # if key == keyboard.Key.f3:
        #     quick_exit()


    with keyboard.Listener(on_release=on_key_release) as listener:
        listener.join()


    # window.mainloop()

