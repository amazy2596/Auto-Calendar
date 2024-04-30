from pynput import mouse, keyboard
import os

# 全局变量记录Ctrl键是否按下
ctrl_pressed = False
num = 0  # 记录符合条件的点击次数
mouse_position = []  # 用于存储符合条件的鼠标位置

# 当键盘按键被按下时触发
def on_press(key):
    global ctrl_pressed
    # 检查是否按下了左侧或右侧的Ctrl键
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = True  # 如果是，设置ctrl_pressed为True

# 当键盘按键被释放时触发
def on_release(key):
    global ctrl_pressed
    # 检查被释放的是否是Ctrl键
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = False  # 如果是，设置ctrl_pressed为False

# 当鼠标按钮被点击时触发
def on_click(x, y, button, pressed):
    global ctrl_pressed
    global num
    # 检查是否是鼠标左键被按下且Ctrl键当前被按下
    if button == mouse.Button.left and pressed and ctrl_pressed:
        num += 1  # 增加点击计数
        print(f'第{num}次点击')
        print(f'鼠标位置: {x}, {y}')
        mouse_position.append((x, y))  # 记录当前鼠标位置
        # 如果达到10次点击，执行写文件操作
        if num == 10:
            write_position()
            # 停止键盘和鼠标监听器
            k_listener.stop()
            m_listener.stop()

# 将记录的鼠标位置写入文件
def write_position():
    dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本的目录
    data_dir = os.path.join(dir, '..', 'data')  # 设置数据目录的路径
    os.makedirs(data_dir, exist_ok=True)  # 确保数据目录存在
    file_path = os.path.join(data_dir, 'position.txt')  # 设置文件路径
    with open(file_path, 'w') as file:  # 打开文件准备写入
        for position in mouse_position:  # 遍历所有记录的位置
            file.write(f'{position[0]}, {position[1]}\n')  # 写入每个位置

# 启动键盘和鼠标监听器
with keyboard.Listener(on_press=on_press, on_release=on_release) as k_listener, \
    mouse.Listener(on_click=on_click) as m_listener:
        k_listener.join()  # 阻塞当前线程，直到键盘监听器停止
        m_listener.join()  # 阻塞当前线程，直到鼠标监听器停止
