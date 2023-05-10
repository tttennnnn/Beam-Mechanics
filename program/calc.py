from decimal import Decimal # for precise calc

def droptrail(num, rnd = True): # round to 3 decimals and drop trailing zeros
    num = float(num)
    if rnd == True:
        num = round(num, 3)
    num = str(num)
    dot = num.find('.')
    num = num[:dot + 1] + num[dot + 1:].strip('0')
    return num.strip('.') # return a string

def turnp(loads, sf = True): # return distances of turning points (positions of all loads)
    points = ()              # sf == True means considering sfd (no need to account for bending-moment load), False means bmd
    for load in loads:
        if load[0] == 'p':
            points += load[2],
        elif load[0] == 'w':
            points += load[2], load[3],
        elif sf == False: # only if load is a bending moment
            points += load[2],
    return tuple(sorted(points)) # return a sorted tuple for the turtle to draw in order

def xintersect(points, sf): # calculate x-value of where sfd intersects with x-axis (zero shear force)
    xintersect = ()
    for i in range(len(points) - 1):
        if (sf[2*i + 1] > 0 and sf[2*i + 2] < 0) or (sf[2*i + 1] < 0 and sf[2*i + 2] > 0):
            yratio = abs(Decimal(str(sf[2*i + 2]))/Decimal(str(sf[2*i + 1])))
            x = (Decimal(str(points[i + 1])) + Decimal(str(points[i])) * yratio)/(1 + yratio)
            x = float(x)
            if x != points[i]: # x == points[i] -> points[i+1] == points[i] -> the graph doesn't actually intersect x-axis
                xintersect += x,
    return xintersect

def forcesum(loads, dist, incld): # shear force at x = dist
    force = 0                     # incld == True -> account for force at x == dist, False -> does not account for  
    dist = Decimal(str(dist))
    for load in loads:
        load1 = Decimal(str(load[1]))
        load2 = Decimal(str(load[2]))
        if load[0] == 'p':
            if load2 < dist:
                force += load1
            elif incld == True and load2 == dist:
                force += load1
        elif load[0] == 'w':
            load3 = Decimal(str(load[3]))
            if load2 <= dist < load3:
                force += load1 * (dist - load2)
            elif load3 <= dist:
                force += load1 * (load3 - load2)
    return float(force)
    
def torquesum(loads, dist, incld): # bending moment at x = dist
    torque = 0                     # incld == True -> account for concentrated bending moment at x == dist, False -> does not account for
    dist = Decimal(str(dist))
    for load in loads:
        load1 = Decimal(str(load[1]))
        load2 = Decimal(str(load[2]))
        if load[0] == 'p' and load2 < dist:
            torque += load1 * (dist - load2)
        elif load[0] == 'w':
            load3 = Decimal(str(load[3]))
            if load2 <= dist < load3:
                torque += Decimal('0.5') * load1 * (dist - load2)**2
            elif load3 <= dist:
                torque += Decimal('0.5') * load1 * ((dist - load2)**2 - (dist - load3)**2)
        elif load[0] == 'm':
            if load2 < dist:
                torque -= load1
            elif incld == True and load2 == dist:
                torque -= load1
    return float(torque)