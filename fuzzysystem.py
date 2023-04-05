from geometry import *
import numpy as np


class FuzzySystem:
    SMALL = 0
    MEDIUM = 1
    LARGE = 2
    def get_theta(self, df, dr, dl):
        alpha = []  # 9 starting strengths
        alpha.append(min(self.fs_dlr(dl, dr, self.LARGE), self.fs_df(df, self.LARGE)))
        alpha.append(min(self.fs_dlr(dl, dr, self.LARGE), self.fs_df(df, self.MEDIUM)))
        alpha.append(min(self.fs_dlr(dl, dr, self.LARGE), self.fs_df(df, self.SMALL)))
        alpha.append(min(self.fs_dlr(dl, dr, self.MEDIUM), self.fs_df(df, self.LARGE)))
        alpha.append(min(self.fs_dlr(dl, dr, self.MEDIUM), self.fs_df(df, self.MEDIUM)))
        alpha.append(min(self.fs_dlr(dl, dr, self.MEDIUM), self.fs_df(df, self.SMALL)))
        alpha.append(min(self.fs_dlr(dl, dr, self.SMALL), self.fs_df(df, self.LARGE)))
        alpha.append(min(self.fs_dlr(dl, dr, self.SMALL), self.fs_df(df, self.MEDIUM)))
        alpha.append(min(self.fs_dlr(dl, dr, self.SMALL), self.fs_df(df, self.SMALL)))
        alpha_left = max(alpha[0], alpha[1], alpha[2])
        alpha_front = max(alpha[3], alpha[4], alpha[5])
        alpha_right = max(alpha[6], alpha[7], alpha[8])
        return self.defuzzificate(alpha_left, alpha_front, alpha_right)


    def defuzzificate(self, alpha_left, alpha_front, alpha_right):
        up = 0.0
        down = 0.0

        for x in range(-60, -29):
            if((x+60)/30 >= alpha_left):
                up += x*alpha_left
                down += alpha_left


        for x in range(-29, 0):
            left_up = front_up = 0.0
            left_down = front_down = 0.0
            if((-x)/30 >= alpha_left):
                left_up = x*alpha_left
                left_down = alpha_left
            if((x+30)/30 >= alpha_front):
                front_up = x*alpha_front
                front_down = alpha_front
            up -= max(abs(left_up), abs(front_up))
            down += max(left_down, front_down)


        for x in range(1, 31):
            right_up = front_up = 0.0
            right_down = front_down = 0.0
            if((30-x)/30 >= alpha_front):
                front_up = x*alpha_front
                front_down = alpha_front
            if(x/30 >= alpha_right):
                right_up = x*alpha_right
                right_down = alpha_right
            up += max(right_up, front_up)
            down += max(right_down, front_down)
            

        for x in range(31, 61):
            if((60-x)/30 >= alpha_right):
                up += x*alpha_right
                down += alpha_right

        if down == 0.0:
            return 0
        else:
            return up / down


    def fs_df(self, df, dis_kind):
        for case in switch(dis_kind):
            if case(self.SMALL):
                if df < 6:
                    return 1
                elif df < 9:
                    return (9.0 - df) / (3.0)
                else:
                    return 0
            elif case(self.MEDIUM):
                px1 = 9.0
                px2 = 13.0
                px3 = 17.0
                if df < px1:
                    return 0
                elif df < px2:
                    return (df - px1) / (px2 - px1)
                elif df < px3:
                    return (px3 - df) / (px3 - px2)
                else:
                    return 0
            elif case(self.LARGE):
                if df > 17:
                    return 1
                else:
                    return 0
            else:
                return 0

    def fs_dlr(self, dl, dr, dis_kind):
        dlr = dl-dr
        for case in switch(dis_kind):
            if case(self.SMALL):    # turn right
                px1 = -12.0
                px2 = -7.0
                if dlr < px1:
                    return 1
                elif dlr < px2:
                    return (px2 - dlr) / (px2 - px1)
                else:
                    return 0
            elif case(self.MEDIUM):
                px1 = -7.0
                px2 = 0.0
                px3 = 7.0
                if dlr < px1:
                    return 0
                elif dlr < px2:
                    return (dr - px1) / (px2 - px1)
                elif dlr < px3:
                    return (px3 - dr) / (px3 - px2)
                else:
                    return 0
            elif case(self.LARGE):  # turn left
                px1 = 7.0
                px2 = 12.0
                if dlr > px2:
                    return 1
                elif dlr > px1:
                    return (dlr - px1) / (px2 - px1)
                else:
                    return 0
            else:
                return 0

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False