import const
from calc import forcesum, xintersect
from graphing import *

width = const.width
height = const.height
x0 = const.x0
y1 = const.y1
thick = const.thick

def plot_sfd(p, loads, xscale):
    points = turnp(loads) # sorted positions of all loads except concentrated bending moment
    sf = () # shearforce
    for point in points:
        sf += -forcesum(loads, point, incld = False), -forcesum(loads, point, incld = True), # calculate y-value -> len(sf) == 2*len(points)

    try:
        yscale = height/9/max(abs(max(sf)), abs(min(sf))) # pixel per newton (vertical scale)
    except ZeroDivisionError:
        yscale = 0

    p.pu()
    p.goto(x0, y1)
    p.fillcolor('#39bf8a')
    p.begin_fill() # fill color in area under graph 
    for i in range(len(points)): # each line is always linear
        p.goto(x0 + xscale*points[i], y1 + yscale*sf[2*i])
        p.goto(x0 + xscale*points[i], y1 + yscale*sf[2*i + 1])
    p.goto(-x0, y1)
    p.goto(x0, y1)
    p.end_fill()

    axes(p, 'SFD', x0, y1) # draw axes SFD
    
    mark(p, points, sf, x0, y1, xscale, yscale)

    return xintersect(points, sf)