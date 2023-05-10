import const
from calc import *

width = const.width
height = const.height
x0 = const.x0
y0 = const.y0   # y0 varies between the 3 diagrams
thick = const.thick

def beam_and_support(p, beamtype, support_left, support_right, scale): # draw beam and support
    p.pensize(1) # draw beam
    p.fillcolor('grey') # color of beam
    p.begin_fill()
    p.pu()
    p.goto(x0, y0 + thick)
    p.pd()
    p.goto(-x0, y0 + thick)
    p.goto(-x0, y0 - thick)
    p.goto(x0, y0 - thick)
    p.goto(x0, y0 + thick)
    p.pu()
    p.end_fill()
    if beamtype in '12': # draw two supports 
        drawsupport(p, support_left*scale)
        drawsupport(p, support_right*scale)
    else:
        drawcantilever(p)

def drawsupport(p, dist): # draw one support
    p.pensize(1)
    p.goto(x0 + dist, y0 - thick)
    p.fillcolor('#C4A6A0')
    p.begin_fill()
    p.pd()
    p.goto(x0 + dist - thick, y0 - 2.5*thick)
    p.goto(x0 + dist + thick, y0 - 2.5*thick)
    p.goto(x0 + dist, y0 - thick)
    p.pu()
    p.end_fill()
    
def drawcantilever(p): # draw wall for cantilever
    p.goto(-x0, y0 - 3*thick)
    p.fillcolor('#C4A6A0')
    p.begin_fill()
    p.pd()
    p.goto(-x0, y0 + 3*thick)
    p.pu()
    p.goto(-x0 + 2*thick, y0 + 3*thick)
    p.goto(-x0 + 2*thick, y0 - 3*thick)
    p.goto(-x0, y0 - 3*thick)
    p.end_fill()

#######################################################################################################################################

def depictload_act(p, load, scale): # draw arrows and label magnitude of action loads
    p.pu()
    rev = load[1] < 0 # rev indicates direction of arrow
    if load[0] == 'p':
        drawforce(p, load[2], scale, y0 + thick, arrowlen = 1/14, headsize = 0.8, pensize = 1.7, rev = rev)
        writeforce(p, load, scale, vert = 0.08)
    elif load[0] == 'w':
        num = 7 # draw 6 arrows
        separate = (load[3] - load[2]) / (num - 1)
        dist = load[2]
        for _ in range(num): # draw multiple arrows 
            drawforce(p, dist, scale, y0 + thick, rev = rev)
            dist += separate
        p.goto(x0 + load[2]*scale, y0 + thick + height/20) # draw a line over the span of distributed load
        p.pd()
        p.goto(x0 + load[3]*scale, y0 + thick + height/20)
        p.pu()
        writeforce(p, load, scale)
    else:
        drawmoment(p, load[1], load[2], scale)
        writeforce(p, load, scale)

def depictload_react(p, beamtype, support_left, support_right, loads, length, scale): # draw arrows and label magnitude of reaction loads
    force = forcesum(loads, length, incld = True)
    torque = torquesum(loads, length, incld = True)
    if beamtype in '12':
        mag_left = (torque - force*(length - support_right))/(support_right - support_left)
        mag_right = (torque - force*(length - support_left))/(support_left - support_right)
        rev = mag_left >= 0
        drawforce(p, support_left, scale, y0 - 2.5*thick - height/20, headsize = 0.8, pensize = 1.5, rev = rev)
        rev = mag_right >= 0
        drawforce(p, support_right, scale, y0 - 2.5*thick - height/20, headsize = 0.8, pensize = 1.5, rev = rev)
        writeforce(p, ('p', mag_left, support_left), scale, vert = -3.5*thick/height - 0.08)
        writeforce(p, ('p', mag_right, support_right), scale, vert = -3.5*thick/height - 0.08)
        loads += ('p', -mag_left, support_left), ('p', -mag_right, support_right),
    else: # cantilever
        drawforce(p, length, scale, y0 - 1.8*thick - height/20, headsize = 0.8, pensize = 1.5, rev = True)
        writeforce(p, ('p', force, length), scale, vert = -2.5*thick/height - 0.08)
        drawmoment(p, torque, length, scale) # draw bending moment on wall
        writeforce(p, ('m', torque, length), scale, cantilever = True)
        loads += ('p', -force, length), ('m', torque, length),

    return loads

def drawforce(p, dist, scale, arrowhead, arrowlen = 1/20, headsize = 0.5, color = 'black', pensize = 1.3, rev = False): # draw arrow of 'p' or 'w'
    arrowlen *= height # length of arrow
    p.pensize(pensize)
    p.turtlesize(headsize)
    p.color(color)
    p.goto(x0 + dist*scale, arrowhead + arrowlen) # arrowhead -> y coor of arrowhead
    p.pd()          
    p.setheading(p.towards(x0 + dist*scale, arrowhead))
    if rev:
        p.left(180)
        p.stamp()
    p.goto(x0 + dist*scale, arrowhead)
    if not rev:
        p.stamp()
    p.color('black')
    p.pu()

def drawmoment(p, mag, dist, scale, dotsize = 5, size = 40): # draw curved arrow of 'm'
    p.goto(x0 + dist*scale, y0)
    p.dot(dotsize)
    p.goto(x0 + dist*scale, y0 - 0.9*size)
    if mag >= 0:
        p.write('\u2938', font = ('', size, '')) # clockwise arrow
    else:
        p.setheading(0)
        p.back(2.2*thick)
        p.write('\u2939', font = ('', size, '')) # counter-clockwise arrow

def writeforce(p, load, scale, vert = 0.06, cantilever = False): # label magnitude of load
    vert *= height # vert -> vertical distance from the top surface of beam
    dist = load[2]
    if load[0] == 'p':
        unit = 'N'
    elif load[0] == 'm':
        unit = 'N\u00B7m'
        vert /= 4
    else:
        dist = (load[2] + load[3])/2 # the middle of distributed-load's span
        unit = 'N/m'
    if not cantilever:
        p.goto(x0 + dist*scale, y0 + thick + vert)
        p.write(f'{droptrail(abs(load[1]), rnd = True)} {unit}', align = 'center', font = ('Verdana', 9, 'italic')) # write magnitude (always positive)
    else: # bending moment due to cantilever
        p.goto(x0 + dist*scale, y0 - thick/2)
        p.write(f'      {droptrail(abs(load[1]), rnd = True)} {unit}', align = 'left', font = ('Verdana', 9, 'italic'))
