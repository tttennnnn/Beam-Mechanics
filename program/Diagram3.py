import const
from calc import torquesum
from graphing import *

width = const.width
height = const.height
x0 = const.x0
y0 = const.y0
y1 = const.y1
y2 = const.y2
thick = const.thick

def plot_bmd(p, xintersect, loads, xscale):
    points = turnp(loads, sf = False) # sorted positions of all loads

    bm = () # bending moment at each point in points
    for point in points: 
        bm += -torquesum(loads, point, incld = False), -torquesum(loads, point, incld = True),
    
    localy = () # local max/min of bmd
    for x in xintersect:
        localy += -torquesum(loads, x, incld = False), -torquesum(loads, x, incld = True) 

    try:
        yscale = height/9/max((abs(max(bm)), abs(min(bm))) + localy) # pixel per (N*m) (vertical scale)
    except ZeroDivisionError:
        yscale = 0
        
    p.pu()
    xcor = points[0]
    p.goto(x0, y2)
    p.fillcolor('#7192d1')
    p.begin_fill() # fill color in area under graph
    num = 100 # number of points until next turning point

    for i in range(len(points)):
        # xcor -> x position of points[i-1]
        p.goto(x0 + xscale*xcor, y2 + yscale * -torquesum(loads, xcor, incld = True))
        deltax = (points[i] - xcor)/num # separations between each plot
        for j in range(1, num): # since BMD is not always linear -> calculate 
            p.goto(x0 + xscale*(xcor + deltax*j), y2 + yscale * -torquesum(loads, xcor + deltax*j, incld = False))
        p.goto(x0 + xscale*points[i], y2 + yscale * -torquesum(loads, points[i], incld = False))
        xcor = points[i]
    p.goto(x0 + xscale*xcor, y2)
    p.goto(x0, y2)
    p.end_fill()

    axes(p, 'BMD', x0, y2) # draw axes BMD

    mark(p, points, bm, x0, y2, xscale, yscale) # label BMD at each load positions
    mark(p, xintersect, localy, x0, y2, xscale, yscale) # label local max/min due to zero shear force

    for x in xintersect:
        dash(p, x, x0, y0, xscale, color = 'red') # red vertical dash lines to indicate local max/min
