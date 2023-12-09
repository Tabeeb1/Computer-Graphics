from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

def MidPointLine(zone, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    d_init = (2 * dy) - dx
    e = 2 * dy
    ne = 2 * (dy - dx)

    x = x1
    y = y1

    while x <= x2:
        cx, cy = convert_to_original_zone(zone, x, y)
        glPointSize(2)
        glBegin(GL_POINTS)
        glVertex2f(cx, cy)

        glEnd()

        if d_init <= 0:
            x += 1
            d_init += e
        else:
            x += 1
            y += 1
            d_init += ne


def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) > abs(dy):
        if dx > 0:
            if dy > 0:
                return 0
            else:
                return 7
        else:
            if dy > 0:
                return 3
            else:
                return 4
    else:
        if dx > 0:
            if dy > 0:
                return 1
            else:
                return 6
        else:
            if dy > 0:
                return 2
            else:
                return 5


def convert_to_original_zone(orginal, x, y):
    if orginal == 0:
        return x, y
    if orginal == 1:
        return y, x
    if orginal == 2:
        return -y, -x
    if orginal == 3:
        return -x, y
    if orginal == 4:
        return -x, -y
    if orginal == 5:
        return -y, -x
    if orginal == 6:
        return y, -x
    if orginal == 7:
        return x, -y


def convert_to_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    else:
        return x, -y


def draw_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    one_x, one_y = convert_to_zone0(x1, y1, zone)
    two_x, two_y = convert_to_zone0(x2, y2, zone)

    MidPointLine(zone, one_x, one_y, two_x, two_y)



box_x = 150
box_y = 50
di_x = 150
di_y = 600
up_x = 150
up_y = 20
up_speed = 0.1
box_speed = 10
di_speed = 0.1
chosen_color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))

# AABB func
collision = False
over = False
score = 0
lower_color = (1.0, 1.0, 1.0)
shot = False
play = True



def lower_box():
    global box_x, box_y, collision, box1, box2
    global di_y, score
    count = 1
    glColor3f(*lower_color)

    draw_line(box_x - 20, box_y - 49, box_x + 30, box_y - 49)
    draw_line(box_x - 30, box_y - 39, box_x + 40, box_y - 39)  # upper

    draw_line(box_x - 30, box_y - 39, box_x - 20, box_y - 49)
    draw_line(box_x + 40, box_y - 39, box_x + 30, box_y - 49)


def catcher():
    global di_x, di_y

    glColor3f(*chosen_color)

    draw_line(di_x - 7, di_y, di_x, di_y + 7)
    draw_line(di_x, di_y + 7, di_x + 7, di_y)
    draw_line(di_x + 7, di_y, di_x, di_y - 7)
    draw_line(di_x - 7, di_y, di_x, di_y - 7)


def shooter():
    global up_x, up_y

    glColor3f(0.5, 0.2, 1)

    draw_line(up_x - 7, up_y, up_x + 7, up_y)
    draw_line(up_x - 7, up_y, up_x - 7, up_y - 7)
    draw_line(up_x + 7, up_y, up_x + 7, up_y - 7)
    draw_line(up_x - 7, up_y - 7, up_x + 7, up_y - 7)



def mouse_event(button, state, x, y):
    global shot, up_x, up_y, over
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not shot and not over:
        up_x = box_x
        up_y = 30
        shot = True


def keyboard_special_keys(key, _, __):
    # check against special keys here (e.g. F1..F11, arrow keys, etc.)
    # use GLUT_KEY_* constants while comparing (e.g. GLUT_KEY_F1, GLUT_KEY_LEFT, etc.)
    global box_x, box_y

    if key == GLUT_KEY_LEFT and box_x > 30:
        box_x -= box_speed
    elif key == GLUT_KEY_RIGHT and box_x < 460:
        box_x += box_speed

    glutPostRedisplay()


def iterate():
    glViewport(0, 0, 500, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 600, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def change_x():
    global di_x, di_y, box2

    # Randomize the initial horizontal position within a range
    di_x = random.randint(20, 500)
    di_y = 550

    global chosen_color
    chosen_color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))


def animate():
    global play, over, shot, up_x, up_y
    if not over and play:
        check_collision()

        global di_x, di_y, di_speed, score
        if di_y <= 0:
            change_x()

        if up_y > 550:
            shot = False
            up_x = box_x
            up_y = 30

        if up_y == di_y and abs(up_x - di_x) == 5:
            change_x()
            shot = False
            up_x = box_x
            up_y = 30

        di_y = (di_y - di_speed)
        up_y = (up_y + di_speed)

    global box2, box1

    glutPostRedisplay()


def check_collision():
    global collision, score, di_y, lower_color, di_x, di_speed, over, play, shot, up_x, up_y, shot

    if (
            (up_x - 7 <= di_x + 7 and up_x + 7 >= di_x - 7)
            and (up_y + 7 >= di_y - 7 and up_y - 7 <= di_y + 7)
    ):
        collision = True
        score += 1
        di_x = random.randint(20, 500)
        di_y = 550
        up_x = box_x
        up_y = 30
        shot = False
        global chosen_color
        chosen_color = (random.uniform(0.3, 1), random.uniform(0.3, 1), random.uniform(0.3, 1))
        print("Score:", score)

        if shot:
            # Restart the game when the "lower shot" and "catcher" collide
            restart_game()

    else:
        collision = False

        if di_y < 50:  # If diamond is lower than the lower box without collision
            lower_color = (1, 0, 0)  # Change lower box color to red
            if not over:
                print("Game Over! Score:", score, "\n")
                score = 0
                over = True

        else:
            over = False
            lower_color = (1, 1, 1)


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    glColor3f(1.0, 1.0, 1.0)

    if not over:
        catcher()
        if shot:
            shooter()
    lower_box()
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 600)

glutInitWindowPosition(0, 0)

wind = glutCreateWindow(b"SHOT THE OBJECT")

glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutSpecialFunc(keyboard_special_keys)
glutMouseFunc(mouse_event)
glEnable(GL_DEPTH_TEST)
glutMainLoop()
