import math as m
import random as r
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import font as tkfont
from geometry import *
import fuzzysystem as fuzzy
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.patches import Rectangle
import time


class myFrame():
    def __init__(self, tk):
        self.root = tk
        self.root.config(bg="white")
        self.root.resizable(width=False, height=False)
        self.root.title('FuzzySystem 111522086')
        self.root.geometry('700x480')

        initFrame(self.root)


class initFrame():
    def __init__(self, master):
        master.config(bg='white')
        global mm
        mm = master

        self.initface_frmae = tk.Frame(master,)

        global left_sensor, front_sensor, right_sensor, var3, xy
        left_sensor = tk.Label(root, text='', font=(
            "Arial", 14, "bold"), fg="gray")
        left_sensor.place(x=570, y=300, anchor="center")
        front_sensor = tk.Label(root, text='', font=(
            "Arial", 14, "bold"), fg="gray")
        front_sensor.place(x=570, y=360, anchor="center")
        right_sensor = tk.Label(root, text='', font=(
            "Arial", 14, "bold"), fg="gray")
        right_sensor.place(x=570, y=420, anchor="center")

        run_example()


def myCanvas(rt, x, y, state):
    fig = Figure(figsize=(4, 5), dpi=120)
    pltfig = fig.add_subplot(111)

    canvas = FigureCanvasTkAgg(fig, rt)
    canvas.get_tk_widget().pack(side=LEFT)
    plt.ion()  # turn on interactive mode

    coord = [[-6, -3], [-6, 22], [18, 22], [18, 50],
             [30, 50], [30, 10], [6, 10], [6, -3], [-6, -3]]
    coord_x, coord_y = zip(*coord)  # create lists of x and y values

    pltfig.add_patch(Rectangle((-6, -0.2), 12, 0.4))  # starting line
    pltfig.add_patch(Rectangle((18, 37), 12, 3))  # finish line
    pltfig.plot(coord_x, coord_y)

    centerx = 0.0
    centery = 0.0
    theta = np.arange(0, 2*np.pi, 0.01)  # arange(start, stop, step)
    radius = 3
    a = centerx + radius * np.cos(theta)
    b = centery + radius * np.sin(theta)
    circle1, = pltfig.plot(a, b)
    tx = [0]
    ty = [0]

    for i in range(len(x)):
        circle1.remove()

        s = "left : " + str(round(float(state[i][2]), 6)) + "      "
        left_sensor.config(text=s)
        s = "front : " + str(round(float(state[i][0]), 6)) + "      "
        front_sensor.config(text=s)
        s = "right : " + str(round(float(state[i][1]), 6)) + "      "
        right_sensor.config(text=s)

        centerx = x[i]
        centery = y[i]

        # car
        circle1 = plt.Circle((centerx, centery), 3, fill=False)
        pltfig.add_patch(circle1)

        # track
        tx.append(centerx)
        ty.append(centery)
        pltfig.plot(tx, ty)

        canvas.draw()
        canvas.flush_events()
        time.sleep(0.03)
    return canvas, pltfig


class Car():
    def __init__(self) -> None:
        self.radius = 6
        self.angle_min = -90
        self.angle_max = 270
        self.wheel_min = -40
        self.wheel_max = 40

        self.reset()

    @property
    def diameter(self):
        return self.radius/2

    def reset(self):
        self.angle = 90
        self.wheel_angle = 0

        
        self.xpos = 0
        self.ypos = 0

    def setWheelAngle(self, angle):
        self.wheel_angle = angle if self.wheel_min <= angle <= self.wheel_max else (
            self.wheel_min if angle <= self.wheel_min else self.wheel_max)

    def setPosition(self, newPosition: Point2D):
        self.xpos = newPosition.x
        self.ypos = newPosition.y

    def getPosition(self, point='center') -> Point2D:
        if point == 'right':
            right_angle = self.angle - 45
            right_point = Point2D(self.radius/2, 0).rorate(right_angle)
            return Point2D(self.xpos, self.ypos) + right_point

        elif point == 'left':
            left_angle = self.angle + 45
            left_point = Point2D(self.radius/2, 0).rorate(left_angle)
            return Point2D(self.xpos, self.ypos) + left_point

        elif point == 'front':
            fx = m.cos(self.angle/180*m.pi)*self.radius/2+self.xpos
            fy = m.sin(self.angle/180*m.pi)*self.radius/2+self.ypos
            return Point2D(fx, fy)
        else:
            return Point2D(self.xpos, self.ypos)

    def getWheelPosPoint(self):
        wx = m.cos((-self.wheel_angle+self.angle)/180*m.pi) * \
            self.radius/2+self.xpos
        wy = m.sin((-self.wheel_angle+self.angle)/180*m.pi) * \
            self.radius/2+self.ypos
        return Point2D(wx, wy)

    def setAngle(self, new_angle):
        new_angle %= 360
        if new_angle > self.angle_max:
            new_angle -= self.angle_max - self.angle_min
        self.angle = new_angle

    def tick(self):  # set the car state from t to t+1
        car_angle = self.angle/180*m.pi
        wheel_angle = self.wheel_angle/180*m.pi
        new_x = self.xpos + m.cos(car_angle+wheel_angle) + \
            m.sin(wheel_angle)*m.sin(car_angle)

        new_y = self.ypos + m.sin(car_angle+wheel_angle) - \
            m.sin(wheel_angle)*m.cos(car_angle)
        new_angle = (car_angle - m.asin(2*m.sin(wheel_angle) /
                     (self.radius))) / m.pi * 180

        new_angle %= 360
        if new_angle > self.angle_max:
            new_angle -= self.angle_max - self.angle_min

        self.xpos = new_x
        self.ypos = new_y
        self.setAngle(new_angle)


class Playground():
    def __init__(self):
        self._setDefaultLine()
        self.car = Car()
        self.reset()

    def _setDefaultLine(self):
        print('use default lines')
        self.destination_line = Line2D(18, 40, 30, 37)  # finish line

        self.lines = [
            Line2D(-6, -3, 6, -3),
            Line2D(6, -3, 6, 10),
            Line2D(6, 10, 30, 10),
            Line2D(30, 10, 30, 50),
            Line2D(30, 50, 18, 50),
            Line2D(18, 50, 18, 22),
            Line2D(18, 22, -6, 22),
            Line2D(-6, 22, -6, -3)
        ]

        self.car_init_pos = None
        self.car_init_angle = None

    @property  # Only-Read
    def n_actions(self):  # action = [0~num_angles-1]
        return (self.car.wheel_max - self.car.wheel_min)

    @property
    def observation_shape(self):
        return (len(self.state),)

    @ property
    def state(self):
        front_dist = - 1 if len(self.front_intersects) == 0 else self.car.getPosition(
        ).distToPoint2D(self.front_intersects[0])
        right_dist = - 1 if len(self.right_intersects) == 0 else self.car.getPosition(
        ).distToPoint2D(self.right_intersects[0])
        left_dist = - 1 if len(self.left_intersects) == 0 else self.car.getPosition(
        ).distToPoint2D(self.left_intersects[0])

        return [front_dist, right_dist, left_dist]

    def _checkDoneIntersects(self):
        if self.done:
            return self.done

        cpos = self.car.getPosition('center')     # center point of the car
        cfront_pos = self.car.getPosition('front')
        cright_pos = self.car.getPosition('right')
        cleft_pos = self.car.getPosition('left')
        self.car.getWheelPosPoint()
        diameter = self.car.diameter

        isAtDestination = cpos.isInRect(    # arrive finish line or not
            self.destination_line.p1, self.destination_line.p2
        )
        done = False if not isAtDestination else True

        front_intersections, find_front_inter = [], True
        right_intersections, find_right_inter = [], True
        left_intersections, find_left_inter = [], True
        for wall in self.lines:  # chack every line in play ground
            dToLine = cpos.distToLine2D(wall)  # distance of car's center to wall
            p1, p2 = wall.p1, wall.p2 
            dp1, dp2 = (cpos-p1).length, (cpos-p2).length  # distance of car's center to p1/p2
            wall_len = wall.length  # wall length

            # touch conditions
            p1_touch = (dp1 < diameter) 
            p2_touch = (dp2 < diameter) 
            body_touch = (  # whether car touch the wall
                dToLine < diameter and (dp1 < wall_len and dp2 < wall_len)
            )
            '''
            回傳兩線是否相交(bool)和相交的點(float)
            若相交會有兩點: _t, _u
            一個由車行進方向計算，另一個由牆的端點計算
            '''
            front_touch, front_t, front_u = Line2D(
                cpos, cfront_pos).lineOverlap(wall)
            right_touch, right_t, right_u = Line2D(
                cpos, cright_pos).lineOverlap(wall)
            left_touch, left_t, left_u = Line2D(
                cpos, cleft_pos).lineOverlap(wall)

            if p1_touch or p2_touch or body_touch or front_touch:
                if not done:
                    done = True

            # find all intersections
            if find_front_inter and front_u and 0 <= front_u <= 1:
                front_inter_point = (p2 - p1)*front_u+p1
                if front_t:
                    if front_t > 1:  # select only point in front of the car
                        front_intersections.append(front_inter_point)
                    elif front_touch:  # if overlapped, don't select any point
                        front_intersections = []
                        find_front_inter = False

            if find_right_inter and right_u and 0 <= right_u <= 1:
                right_inter_point = (p2 - p1)*right_u+p1
                if right_t:
                    if right_t > 1:  # select only point in front of the car
                        right_intersections.append(right_inter_point)
                    elif right_touch:  # if overlapped, don't select any point
                        right_intersections = []
                        find_right_inter = False

            if find_left_inter and left_u and 0 <= left_u <= 1:
                left_inter_point = (p2 - p1)*left_u+p1
                if left_t:
                    if left_t > 1:  # select only point in front of the car
                        left_intersections.append(left_inter_point)
                    elif left_touch:  # if overlapped, don't select any point
                        left_intersections = []
                        find_left_inter = False

        self._setIntersections(front_intersections,
                               left_intersections,
                               right_intersections)

        self.done = done
        return done

    def _setIntersections(self, front_inters, left_inters, right_inters):
        self.front_intersects = sorted(front_inters, key=lambda p: p.distToPoint2D(
            self.car.getPosition('front')))
        self.right_intersects = sorted(right_inters, key=lambda p: p.distToPoint2D(
            self.car.getPosition('right')))
        self.left_intersects = sorted(left_inters, key=lambda p: p.distToPoint2D(
            self.car.getPosition('left')))

    def reset(self):
        self.done = False
        self.car.reset()

        if self.car_init_angle and self.car_init_pos:
            self.setCarPosAndAngle(self.car_init_pos, self.car_init_angle)

        self._checkDoneIntersects()
        return self.state

    def setCarPosAndAngle(self, position: Point2D = None, angle=None):
        if position:
            self.car.setPosition(position)
        if angle:
            self.car.setAngle(angle)

        self._checkDoneIntersects()

    def step(self, action=None):
        self.car.setWheelAngle(action)

        if not self.done:
            self.car.tick()

            self._checkDoneIntersects()
            return self.state
        else:
            return self.state


def run_example():
    p = Playground()
    FS = fuzzy.FuzzySystem()
    trackline_x = []
    trackline_y = []
    trackstate = []
    xy = [0, 0]

    state = p.reset()

    while not p.done:
        track_x = p.car.xpos
        track_y = p.car.ypos
        xy = []
        xy.append(track_x)
        xy.append(track_y)
        trackline_x.append(track_x)
        trackline_y.append(track_y)
        trackstate.append(state)

        action = FS.get_theta(state[0], state[1], state[2])  # f -> r -> l
        state = p.step(action)
    canvas, pltfig = myCanvas(mm, trackline_x, trackline_y, trackstate)


if __name__ == "__main__":
    root = tk.Tk()
    myFrame(root)
    root.mainloop()
