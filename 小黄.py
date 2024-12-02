
import random
from math import sin, cos, pi, log
from tkinter import *

# 画布尺寸和中心点
CANVAS_WIDTH = 980
CANVAS_HEIGHT = 720
CANVAS_CENTER_X = CANVAS_WIDTH / 2
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2
IMAGE_ENLARGE = 11

# 爱心颜色列表
HEART_COLOR_LIST = [
    "#d974ff", "#be77fa", "#a478f3", "#8b78ea", "#7377e0",
    "#4871c6", "#5c74d3", "#fa6ea9", "#dc6db1", "#ec2c2c",
    "#e91e41", "#8b4593", "#2bd3ec", "#00be93", "#2bec62"
]

# 爱心形状的参数方程
def heart_function(t, shrink_ratio=IMAGE_ENLARGE):
    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))
    x *= shrink_ratio
    y *= shrink_ratio
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y
    return int(x), int(y)

# 随机内部扩散
def scatter_inside(x, y, beta=1.15):
    ratio_x = -beta * log(random.random())
    ratio_y = -beta * log(random.random())
    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy

# 收缩
def shrink(x, y, ratio):
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy

# 调整心跳周期
def curve(p):
    return 2 * (2 * sin(4 * p)) / (2 * pi)

# 爱心类
class Heart:
    def __init__(self, generate_frame=20):
        self._points = set()
        self._edge_diffusion_points = set()
        self._center_diffusion_points = set()
        self.all_points = {}
        self.build(2000)
        self.random_halo = 1000
        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t)
            self._points.add((x, y))
        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))
        point_list = list(self._points)
        for _ in range(6000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.17)
            self._center_diffusion_points.add((x, y))

    @staticmethod
    def calc_position(x, y, ratio):
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520)
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)
        return x - dx, y - dy

    def calc(self, generate_frame):
        ratio = 10 * curve(generate_frame / 10 * pi)
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = int(3000 + 6000 * abs(curve(generate_frame / 10 * pi) ** 2))
        all_points = []
        for _ in range(halo_number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t, shrink_ratio=11.6)
            x, y = shrink(x, y, halo_radius)
            size = random.choice((1, 2, 2))
            all_points.append((x, y, size))
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
        self.all_points[generate_frame] = all_points

    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=random.choice(HEART_COLOR_LIST))

# 星星场类
class StarField:
    def __init__(self):
        self.stars = []

    def add_star(self, x, y):
        self.stars.append((x, y))

    def update(self):
        for i, (x, y) in enumerate(self.stars):
            if y > CANVAS_HEIGHT:
                self.stars.pop(i)
            else:
                self.stars[i] = (x, y + 1)  # Stars fall down

    def render(self, canvas):
        for x, y in self.stars:
            canvas.create_oval(x, y, x + 2, y + 2, fill=random.choice(HEART_COLOR_LIST))

# 绘制函数
def draw(main, canvas, heart, star_field, render_frame=0):
    canvas.delete('all')
    star_field.update()
    for _ in range(10):  # 控制星星的生成速度
        t = random.uniform(0, 2 * pi)
        x, y = heart_function(t, shrink_ratio=11.6)
        star_field.add_star(x, CANVAS_HEIGHT)
    star_field.render(canvas)
    heart.render(canvas, render_frame)
    main.after(50, draw, main, canvas, heart, star_field, render_frame + 1)

# 主程序入口
if __name__ == '__main__':
    root = Tk()
    canvas = Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()
    heart = Heart()
    star_field = StarField()
    draw(root, canvas, heart, star_field)
    text1 = Label(root, text=" ᏊˊꈊˋᏊ", font=("Helvetica", 18), fg="#c12bec", bg="black")
    text1.place(x=650, y=500)
    text2 = Label(root, text="小黄最可爱", font=("Helvetica", 16), fg="#c12bec", bg="black")
    text2.place(x=400, y=350)
    root.mainloop()