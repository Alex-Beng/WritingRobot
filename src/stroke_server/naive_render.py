import json
import numpy as np
import matplotlib.pyplot as plt

from skeleton import pnts2skeleton

color = ['red', 'blue', 'yellow', 'black', 'orange', 'pink', 'gray', 'green']
color_idx = 0

class TextRender:
    def __init__(self, ttf_path, cd='gbk', upt=1000):
        self.ttf_path = ttf_path
        # 接着读入ttf的json
        # 获得upm & dict
        ttf_file = open(ttf_path, encoding=cd)
        ttf_dict = json.load(ttf_file)

        self.upm = ttf_dict['head']['unitsPerEm']
        self.ttf_dict = ttf_dict

        self.upt = upt

    # 渲染一个字符
    def render_once(self):
        global color_idx
        cnt = 0
        for name, contours in self.gen_contours():
            cnt += 1
            if cnt < 1600:
                continue
            if cnt > 1609:
                break
            
            plt.figure(name)
            # img = np.zeros((512, 512), np.uint8)
            for contour in contours:
                ploy_pnts = []
                for pnt_dict in contour:
                    ploy_pnts.append([pnt_dict['x'], 255-(pnt_dict['y']+36)])
                
                pnts2skeleton(ploy_pnts, (512, 512))

                i = 0
                while i < len(contour):
                    ip1 = (i+1)%len(contour)
                    ip2 = (i+2)%len(contour)
                    c_p = []
                    c_p.append([contour[i]['x'], contour[i]['y']])
                    c_p.append([contour[ip1]['x'], contour[ip1]['y']])
                    self.bezier(c_p, color[color_idx])

                    i += 1
                    continue

                    # 一次
                    if contour[i]['on'] and contour[ip1]['on']:
                        c_p = []
                        c_p.append([contour[i]['x'], contour[i]['y']])
                        c_p.append([contour[ip1]['x'], contour[ip1]['y']])
                        # print(c_p)
                        print(i, ip1)
                        self.bezier(c_p)
                        # i += 1
                    # 二次
                    elif contour[i]['on'] and not contour[ip1]['on']:
                        c_p = []
                        c_p.append([contour[i]['x'], contour[i]['y']])
                        c_p.append([contour[ip1]['x'], contour[ip1]['y']])
                        c_p.append([contour[ip2]['x'], contour[ip2]['y']])
                        print(i, ip1, ip2)
                        self.bezier(c_p)
                        # i += 1
                    # else:
                    i += 1
                color_idx += 1
                if color_idx >= len(color):
                    color_idx %= len(color)

        plt.show()
    # 绘制一条bezier曲线
    def bezier(self, control_pnts, color):
        cur_ord = len(control_pnts)-1
        ts = np.linspace(0, 1, self.upt)
        xs = [0.]*self.upt
        ys = [0.]*self.upt
        # 对所有t, 计算对应的x y
        for i in range(self.upt):
            x, y = 0., 0.
            t = ts[i]
            for j in range(cur_ord+1):
                x += self.__B_nx(cur_ord, j, t) * control_pnts[j][0]
                y += self.__B_nx(cur_ord, j, t) * control_pnts[j][1]
            xs[i] = x
            ys[i] = y
        
        plt.plot(xs, ys, color, linewidth=1)

    # 递归计算Bnx
    def __B_nx(self, n, i, x):
        if i>n:
            return 0
        elif i==0:
            return 1.*(1-x)**n
        elif i==1:
            return 1.*n*x*((1-x)**(n-1))
        else:
            return 1.*self.__B_nx(n-1, i, x)*(1-x)+self.__B_nx(n-1, i-1, x)*x

        

    # contours的generator
    def gen_contours(self):
        glyfs = list(self.ttf_dict['glyf'].keys())
        for glyf in glyfs:
            if 'contours' in self.ttf_dict['glyf'][glyf]:
                yield glyf, self.ttf_dict['glyf'][glyf]['contours']

def main():
    tr = TextRender('../../config/font/fangsong_gb2312.json', 'utf-8')
    tr.render_once()

if __name__ == '__main__':
    main()