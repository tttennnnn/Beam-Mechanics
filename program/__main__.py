import turtle

from Input import instruct, beaminput
from Diagram1 import beam_and_support, depictload_act, depictload_react
from Diagram2 import plot_sfd
from Diagram3 import plot_bmd
from graphing import annotate
import const

# set constant
width = const.width
height = const.height
x0 = const.x0
y0 = const.y0

# setup turtle window
screen = turtle.Screen()
screen.setup(width, height)
turtle.tracer(0, 0)
p = turtle.Turtle() # create turtle

# print instructions
instruct()

while True:
    p.hideturtle() 

    # input data
    length, beamtype, support_left, support_right, loads = beaminput()

    xscale = -2*x0/length # pixel per metre (horizontal)

    #diagram 1
    beam_and_support(p, beamtype, support_left, support_right, xscale) 
    annotate(p, loads, length, x0, y0, xscale, support_left, support_right) # label x axis using vertical dash lines

    for load in loads:
        depictload_act(p, load, xscale) # draw arrows of action loads

    # draw arrows of reaction loads from supports
    # add reaction loads to the loads tuple
    loads = depictload_react(p, beamtype, support_left, support_right, loads, length, xscale)

    #diagram 2
    xintersect = plot_sfd(p, loads, xscale) # plot sfd and return positions of zero shear force (exclude shearforce on both edges of beam)

    #diagram 3
    plot_bmd(p, xintersect, loads, xscale)

    turtle.update()
    
    if input('Create new beam? (Y for yes, else for no): ') != 'Y':
        turtle.bye() # end the program
        break
    else:
        p.clear() # clear screen and create a new beam