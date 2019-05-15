import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    print symbols
    print("   ")
    for command in commands:
        print command

        if command["op"] == "push":
            stack.append( [ x[:] for x in stack[-1] ] )
            
        elif command["op"] == "pop":
            stack.pop()

        elif command["op"] == "sphere":

            if command["constants"] != None:
                ref = command["constants"]
            else:
                ref = reflect
            
            add_sphere( tmp,
                            command["args"][0],
                            command["args"][1],
                            command["args"][2],
                            command["args"][3],
                            step_3d )
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, ref)
            tmp = []
            
        elif command["op"] == "torus":
            
            if command["constants"] != None:
                ref = command["constants"]
            else:
                ref = reflect
                
            add_torus( tmp,
                           command["args"][0],
                           command["args"][1],
                           command["args"][2],
                           command["args"][3],
                           command["args"][4],
                           step_3d )
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, ref)
            tmp = []

        elif command["op"] == "box":

            if command["constants"] != None:
                ref = command["constants"]
            else:
                ref = reflect
            
            add_box( tmp,
                         command["args"][0],
                         command["args"][1],
                         command["args"][2],
                         command["args"][3],
                         command["args"][4],
                         command["args"][5] )
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, ref)
            tmp = []

        elif command["op"] == "line":
            add_edge( tmp,
                          command["args"][0],
                          command["args"][1],
                          command["args"][2],
                          command["args"][3],
                          command["args"][4],
                          command["args"][5] )
            matrix_mult( stack[-1], tmp )
            draw_lines( tmp, screen, zbuffer, color )
            tmp = []
            
        elif command["op"] == "scale":
            t = make_scale( command["args"][0], command["args"][1], command["args"][2] )
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t ]

            t = []
            
        elif command["op"] == "move":
            t = make_translate( command["args"][0], command["args"][1], command["args"][2] )
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t ]

            t = []
            
        elif command["op"] == "rotate":
            theta = command["args"][1] * (math.pi / 180)
            print theta
            
            if command["args"][0] == 'x':
                t = make_rotX(theta)
            elif command["args"][0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)

            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t ]

            t = []
            
        elif command["op"] == "display" or command["op"] == "save":
            if command["op"] == "display":
                display(screen)
            else:
                save_extension( screen, command["args"][0] )
