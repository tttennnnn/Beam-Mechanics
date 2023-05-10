import const
from calc import *

height = const.height
width = const.width
thick = const.thick

def axes(p, type, x0, y0, pensize = 1.5): # draw axes for SFD and BMD
    # x-axis
    p.pensize(pensize)
    p.pu()
    p.goto(x0, y0)
    p.setheading(0)
    p.pd()
    p.fd(-2*x0)
    p.pu()
    p.right(90)
    p.fd(height/100)
    p.write(f'   {type}', align = 'left', font = ('Verdana', 11, 'bold'))
    if type == 'SFD':
        p.write('           (N)', align = 'left', font = ('Verdana', 11, 'italic'))
    elif type == 'BMD':
        p.write('           (N\u00B7m)', align = 'left', font = ('Verdana', 11, 'italic'))

def mark(p, points, yval, x0, y0, xscale, yscale): # label y-value of plots
    p.pu()
    for i in range(len(yval)):
        x = points[i//2]
        y = yval[i]
        if abs(y) > 1e-12:
            p.goto(x0 + xscale*x, y0 + yscale*y)
            p.dot(5, 'red')
            p.setheading(90)
            if y < 0:
                p.bk(height/50)
            else:
                p.fd(height/200)
            p.write(f'({droptrail(y, rnd = True)})', align = 'center', font = ('Verdana', 8, 'normal'))

def dash(p, point, x0, y0, xscale, color = 'grey'): # draw dash lines
    p.pu()
    p.pensize(0.5)
    p.color('black')
    p.goto(x0 + xscale*point, - y0 - 4*thick - height/40) 
    p.write(f'({droptrail(point)})', align = 'center', font = ('Verdana', 8, 'normal')) # label position in metre
    p.goto(x0 + xscale*point, - y0 - 4*thick)
    p.dot(4, 'black') # dot on horizontal line

    p.color(color) # dashline color
    
    p.setheading(90) # turtle heading up
    dashlen = height/100 # length of dashline
    n = -1 # 
    while p.ycor() < y0 - 3*thick:
        if n == 1:
            p.pd()
        p.fd(dashlen)
        p.pu()
        n *= -1
    p.color('black')

def annotate(p, loads, length, x0, y0, xscale, support_left = None, support_right = None): # draw axes of X(m) on the bottom of window and draw dash lines
    p.pu() # horizontal line
    p.pensize(1)
    p.color('#332f2e')
    p.goto(x0, - y0 - 4*thick)
    p.pd()
    p.goto(-x0, - y0 - 4*thick)
    p.pu()
    p.goto(-x0, - y0 - 4*thick - height/100) # label 'X(m)'
    p.color('black')
    p.write('   X', align = 'left', font = ('Verdana', 11, 'bold'))
    p.write('      (m)', align = 'left', font = ('Verdana', 11, 'italic'))

    points = turnp(loads, sf = False)
    for point in points: # vertical dash lines and label
        dash(p, point, x0, y0, xscale)

    dash(p, 0, x0, y0, xscale)
    dash(p, length, x0, y0, xscale)
    if support_left:
        dash(p, support_left, x0, y0, xscale)
    if support_right:
        dash(p, support_right, x0, y0, xscale)