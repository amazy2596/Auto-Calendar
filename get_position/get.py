from pynput import mouse, keyboard
import os

# 全局变量记录Ctrl键是否按下
ctrl_pressed = False
num = 0
mouse_position = []

def on_press(key):
    global ctrl_pressed
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = True

def on_release(key):
    global ctrl_pressed
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = False

def on_click(x, y, button, pressed):
    global ctrl_pressed
    global num
    # 检查是否是鼠标左键点击并且Ctrl键被按下
    if button == mouse.Button.left and pressed and ctrl_pressed:
        num += 1
        print(f'第{num}次点击')
        print(f'鼠标位置: {x}, {y}')
        mouse_position.append((x, y))
        if num == 10:
            write_position()
            # 停止监听器
            k_listener.stop()
            m_listener.stop()

def write_position():
    dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir, 'position.txt')
    with open (file_path, 'w') as file:
        for position in mouse_position:
            file.write(f'{position[0]}, {position[1]}\n')

# 启动键盘和鼠标监听器
with keyboard.Listener(on_press=on_press, on_release=on_release) as k_listener, \
     mouse.Listener(on_click=on_click) as m_listener:
    k_listener.join()
    m_listener.join()
