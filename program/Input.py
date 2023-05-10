from clrprint import clrprint

def interactiveinput():
    loads = () # tuple with loads data
    while True: #input length of beam
        try:
            length = float(input('Enter beam length (metre): '))
            break
        except:
            clrprint('Invalid length. Try again.', clr = 'red')

    while True: #input type of beam
        beamtype = input('Enter type of beam (1, 2, or 3): ')
        if beamtype == '1' or beamtype == '3':
            support_left, support_right = 0, length # position of supports (though support_left will not be used in cantilever)
            break
        elif beamtype == '2': # over-hanging beam
            while True: # first support
                try:
                    first = float(input('Distance of the 1st support (metre): '))
                    if 0 <= first <= length:
                        break
                except:
                    pass
                clrprint('Invalid distance. Try again.', clr = 'red')
            while True: # second support
                try:
                    second = float(input('Distance of the 2nd support (metre): '))
                    if 0 <= second <= length:
                        break
                except:
                    pass
                clrprint('Invalid distance. Try again.', clr = 'red')
            support_left = min(first, second)
            support_right = max(first, second) 
            break
        clrprint('Invalid beam type. Try again.', clr = 'red')

    while True: #input loads
        while True:
            load = input('Add a load on beam : ')
            load = load.split()
            if len(load) == 3: # nested if -> to prevent exception if the user input with len(load) == 0
                if load[0] == 'p' or load[0] == 'm':
                    try:
                        load[1] = float(load[1])
                        load[2] = float(load[2])
                        if 0 <= load[2] <= length:
                            break
                    except:
                        pass
            elif len(load) == 4:
                if load[0] == 'w':
                    try:
                        load[1] = float(load[1])
                        load[2] = float(load[2])
                        load[3] = float(load[3])
                        if load[2] < load[3] and 0 <= load[2] and load[3] <= length:
                            break
                    except:
                        pass
            clrprint('Invalid load. Try again.', clr = 'red')
        if load[1] != 0: # only add the load if the magnitude is not 0
            loads += tuple(load),
        if input('Add load? (Y for yes, else for no): ' ) != 'Y':
            break # no load to add
    return length, beamtype, support_left, support_right, loads

def fileinput():
    loads = ()
    while True:
        infile = input('Enter file address: ') # get file input
        try:
            infile = open(infile, 'r')
        except:
            clrprint('File name error. Try again.', clr = 'red')
            continue
    
        try: # retrieve length
            length = float(infile.readline())
        except:
            clrprint('Invalid beam length: line 1', clr = 'red')
            continue

        support_left, support_right = 0, length # positions of support (will change if the user inputs over-hanging)

        second_line = infile.readline().split() # retrieve second line
        if not second_line: # check if second line is empty
            clrprint('Line empty: line 2', clr = 'red')
            continue
        beamtype = second_line[0] # no exception since second line is not empty
        if beamtype != '1' and beamtype != '3':
            if beamtype != '2':
                clrprint('Invalid beam type: line 2', clr = 'red')
                continue
            elif len(second_line) != 3:
                clrprint('Need 2 supports for over-hanging beam: line 2', clr = 'red')
                continue
            else: # if indicated as over-hanging with 3 components in line
                try:
                    first = float(second_line[1])
                    second = float(second_line[2])
                    if not (0 <= first <= length and 0 <= second <= length):
                        clrprint('Support positions must be within beam length: line 2', clr = 'red')
                        continue
                    support_left = min(first, second)
                    support_right = max(first, second)
                except:
                    clrprint('Invalid support positions: line 2', clr = 'red')
                    continue

        line = 3 # count line in data file
        for load in infile: # retrieve loads
            err = False # value to check if an error occurs from line 3 and below
            load = load.split()
            if not load:
                clrprint(f'Line empty: line {line}', clr = 'red')
                err = True
                break # break from for loop immediately to prevent further exceptions
            if len(load) == 3 and (load[0] == 'p' or load[0] == 'm'):
                try:
                    load[1] = float(load[1])
                    load[2] = float(load[2])
                    if not(0 <= load[2] <= length):
                        clrprint(f'Invalid load position: line {line}', clr = 'red')
                        err = True
                except:
                    clrprint(f'Invalid load: line {line}', clr = 'red')
                    err = True
            elif len(load) == 4 and load[0] == 'w':
                try:
                    load[1] = float(load[1])
                    load[2] = float(load[2])
                    load[3] = float(load[3])
                    if not (load[2] < load[3] and 0 <= load[2] and load[3] <= length):
                        clrprint(f'Invalid span position: line {line}', clr = 'red')
                        err = True
                except:
                    clrprint(f'Invalid load: line {line}', clr = 'red')
                    err = True
            else:
                clrprint(f'Invalid load: line {line}', clr = 'red')
                err = True
            if err: # break from for loop if error
                break
            line += 1
            if load[1] != 0:
                loads += tuple(load),
        if err: # continue while loop; ask for file address again after prompting the user what the error is
            continue
        return length, beamtype, support_left, support_right, loads

def instruct(): # print instructions
    clrprint('\u2014'*100, clr = 'purple')
    clrprint('[Input Mode]', clr = 'blue')
    clrprint('\u2022 1: ', end = '')
    clrprint('[Interactive Input]', clr = 'blue')
    clrprint('     -> input accordingly as prompted')
    clrprint('\u2022 2: ', end = '')
    clrprint('[File Input]', clr = 'blue', end = '')
    clrprint(': must be a ".txt" file') 
    clrprint('     -> 1st line: Beam length in metre')
    clrprint('     -> 2nd line: Beam type')
    clrprint('     -> 3rd line and so on: addition of loads (1 line = 1 load)')
    clrprint('\u2014'*100, clr = 'purple')
    clrprint('[Type of Beam]', clr = 'green')
    clrprint(' -> 1: simply-supported, 2: over-hanging, 3: cantilever')
    clrprint()
    clrprint('[Type of loads]', clr = 'green')
    clrprint(' -> p: concentrated load, w: linearly distributed load, m: bending moment')
    clrprint()
    clrprint('[Input format for loads]', clr = 'green', end = '')
    clrprint(': 3 (4 for distributed load) ordered parameters separated with whitespace')
    clrprint(' -> 1st: Type of load')
    clrprint(' -> 2nd: Magnitude of load (positive for downward force/clockwise bending moment)')
    clrprint(' -> 3rd: Position of load (x) (for distributed loads: input the left-end position of its span)')
    clrprint(' -> 4th (for distributed load): Right-end position of its span')
    clrprint('e.g. ', clr = 'green', end = '')
    clrprint('w 5 0 2', clr = 'purple', end = '')
    clrprint(': add a downward distributed load of 5 N spanning within x = [0, 2] m')
    clrprint('     m 10 15', clr = 'purple', end = '')
    clrprint(': to add a clockwise bending moment of 10 N\u00B7m at x = 15 m')
    clrprint('\u2014'*100, clr = 'purple')
    clrprint('\u2022 Re-enter file address if the file contains error during file input.', clr = 'yellow')
    clrprint('\u2022 Take distance x = 0 is the left-end of the beam; x increases to the right.', clr = 'yellow')
    clrprint('\u2022 Position of loads must be within the length of beam.', clr = 'yellow')
    clrprint('\u2022 Unit of position is metre (m).', clr = 'yellow')
    clrprint('\u2022 Unit of load magnitude is Newton(N) for force, Newton*metre (N\u00B7m) for bending moment.', clr = 'yellow')
    clrprint('\u2022 0-magnitude loads will not be illustrated.', clr = 'yellow')
    clrprint('\u2022 The output SFD and BMD follow the sign convention.', clr = 'yellow')
    clrprint('\u2022 All numbers will be represented in 3 decimals maximum.', clr = 'yellow')
    clrprint('\u2022 Red dash lines indicate zero shearforce positions (zero-gradient of BMD, i.e., local max/min).', clr = 'yellow')

def beaminput():
    clrprint('\u2014'*100, clr = 'purple')
    while True: # input mode
        mode = input('Enter Input mode (1 or 2): ')
        if mode == '1':
            return interactiveinput()
        elif mode == '2':
            return fileinput()
        clrprint('Invalid. Try again.', clr = 'red')