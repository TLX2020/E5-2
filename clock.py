# 导入turtle和time模块
import turtle
import time

# 定义专注时钟的类
class FocusClock:
    # 初始化方法，设置属性和画布
    def __init__(self, focus_time=25, break_time=5):
        # 专注时间和休息时间，单位为分钟
        self.focus_time = focus_time
        self.break_time = break_time
        # 创建画布和画笔
        self.screen = turtle.Screen()
        self.screen.title("专注时钟")
        self.screen.bgcolor("white")
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.pensize(3)
        # 创建声音对象，用于播放提示音
        self.sound = turtle.Turtle()
        self.sound.hideturtle()
    
    # 绘制圆形表盘，显示刻度和数字
    def draw_clock(self):
        # 移动到圆心位置
        self.pen.penup()
        self.pen.goto(0, -200)
        self.pen.pendown()
        # 画出圆形表盘，填充颜色
        self.pen.fillcolor("lightblue")
        self.pen.begin_fill()
        self.pen.circle(200)
        self.pen.end_fill()
        # 移动到刻度起点位置
        self.pen.penup()
        self.pen.goto(0, 0)
        self.pen.setheading(90)
        # 画出60个刻度，每6度一个，每5个刻度加粗，并写上数字
        for i in range(60):
            if i % 5 == 0:
                self.pen.forward(180)
                self.pen.pendown()
                self.pen.forward(20)
                self.pen.penup()
                # 写上数字，注意调整位置和方向
                self.pen.forward(25)
                self.pen.write(str(i//5), align="center", font=("Arial", 18, "bold"))
                self.pen.backward(25)
            else:
                self.pen.forward(190)
                self.pen.pendown()
                self.pen.forward(10)
                self.pen.penup()
            # 回到圆心，右转6度，准备下一个刻度
            self.pen.goto(0, 0)
            self.pen.right(6)

    # 绘制指针，根据当前时间显示角度
    def draw_hand(self):
        # 获取当前时间，转换为秒数
        now = time.localtime()
        hour = now.tm_hour % 12 # 转换为12小时制
        minute = now.tm_min
        second = now.tm_sec
        total_seconds = hour * 3600 + minute * 60 + second
        # 计算指针的角度，注意调整方向和范围
        hand_angle = - (total_seconds / (self.focus_time * 60)) * 360 + 90 
        hand_angle %= 360 # 保证在0到360之间
        # 移动到圆心位置，设置朝向和颜色
        self.pen.goto(0, 0)
        self.pen.setheading(hand_angle)
        self.pen.pencolor("red")
        # 画出指针，长度为150像素
        self.pen.pendown()
        self.pen.forward(150)
    
    # 显示当前状态，是专注还是休息，以及剩余时间
    def show_status(self):
        # 获取当前时间，转换为秒数
        now = time.localtime()
        hour = now.tm_hour % 12 # 转换为12小时制
        minute = now.tm_min
        second = now.tm_sec
        total_seconds = hour * 3600 + minute * 60 + second
        # 计算剩余时间，单位为秒
        remain_seconds = (self.focus_time * 60) - (total_seconds % (self.focus_time * 60))
        # 判断当前状态，是专注还是休息
        if remain_seconds > self.break_time * 60:
            status = "专注"
        else:
            status = "休息"
        # 转换剩余时间为分钟和秒数
        remain_minute = remain_seconds // 60
        remain_second = remain_seconds % 60
        # 格式化剩余时间为字符串，如01:23
        remain_time = "{:02d}:{:02d}".format(remain_minute, remain_second)
        # 移动到状态显示位置，清除原来的内容，写上新的内容
        self.pen.penup()
        self.pen.goto(0, -250)
        self.pen.pencolor("black")
        self.pen.setheading(0)
        self.pen.fillcolor("white")
        self.pen.begin_fill()
        for _ in range(2):
            self.pen.forward(200)
            self.pen.left(90)
            self.pen.forward(50)
            self.pen.left(90)
        self.pen.end_fill()
        self.pen.goto(0, -250)
        self.pen.write(status + " " + remain_time, align="center", font=("Arial", 36, "bold"))
    
    # 播放提示音，根据当前状态选择不同的音效
    def play_sound(self):
        # 获取当前时间，转换为秒数
        now = time.localtime()
        hour = now.tm_hour % 12 # 转换为12小时制
        minute = now.tm_min
        second = now.tm_sec
        total_seconds = hour * 3600 + minute * 60 + second
        # 计算剩余时间，单位为秒
        remain_seconds = (self.focus_time * 60) - (total_seconds % (self.focus_time * 60))
        # 判断当前状态，是专注还是休息
        if remain_seconds > self.break_time * 60:
            status = "专注"
        else:
            status = "休息"
        # 如果剩余时间为0，播放提示音
        if remain_seconds == 0:
            if status == "专注":
                # 播放专注结束的提示音，这里用的是Windows的系统提示音，你可以换成自己喜欢的音效文件
                self.sound.getscreen().getcanvas().bell()
            else:
                # 播放休息结束的提示音，这里用的是Windows的警告提示音，你可以换成自己喜欢的音效文件
                self.sound.getscreen().getcanvas().bell()
    
    # 更新画面，每秒调用一次
    def update(self):
        # 清除画笔的轨迹，保留表盘和状态显示
        self.pen.clear()
        # 绘制指针
        self.draw_hand()
        # 显示状态和剩余时间
        self.show_status()
        # 播放提示音
        self.play_sound()
        # 每隔一秒调用一次自身，实现循环更新
        turtle.ontimer(self.update, 1000)

    # 启动专注时钟，显示画面并进入主循环
    def start(self):
        # 绘制表盘
        self.draw_clock()
        # 更新画面
        self.update()
        # 进入主循环，等待用户操作
        turtle.mainloop()

# 创建专注时钟对象，可以自定义专注时间和休息时间，单位为分钟，默认为25和5
clock = FocusClock(focus_time=25, break_time=5)
# 启动专注时钟
clock.start()