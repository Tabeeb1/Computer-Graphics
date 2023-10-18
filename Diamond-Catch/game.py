from OpenGL.GL import *
from OpenGL.GLUT import *
import random 
from time import time
HEIGHT, WIDTH = 800, 500
# Initialize GLUT
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(WIDTH, HEIGHT)
glutCreateWindow(b"Midpoint Line Drawing")

# Set up OpenGL
glClearColor(0.0, 0.0, 0.0, 1.0)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glPointSize(2.0)

IS_PAUSED = False
SPEED = 100
SPWAN_INTERVAL = 5
TIMER = 0
SCORE = 0
IS_GAME_OVER = False
DIAMOND_LIST = []
COLORS = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1)]
PREV_FRAME_TIME = time()
DELTATIME = 1
def clamp(min, max, val):
    if val<min:
        return min
    elif val>max:
        return max
    return val

class Catcher:
    def __init__(self) -> None:
        self.reset()
        self.color = [1,1,1]
    def reset(self):
        self.x1 = 200
        self.y1 = 10
        self.x2 = 300 
        self.y2 = 10 
        self.x3 = 190
        self.y3 = 30
        self.x4 = 310
        self.y4 = 30
        self.update_bbox()
        self.reset_color()
        
    def update_bbox(self):
        self.bbox = {"min_x":min(self.x1,self.x2,self.x3,self.x4), 
                     "min_y":min(self.y1,self.y2,self.y3,self.y4), 
                     "max_x":max(self.x1,self.x2,self.x3,self.x4), 
                     "max_y":max(self.y1,self.y2,self.y3,self.y4)}
    def color_red(self):
        self.color = [1,0,0]
        
    def reset_color(self):
        self.color = [1,1,1]
        
    def move_left(self, move_val):
        global WIDTH, HEIGHT
        # print(self.x1, self.x2, self.x3, self.x4)
        self.x1 = clamp(10, (WIDTH-10)-(self.x2-self.x1), self.x1-int((move_val)*DELTATIME))
        self.x2 = clamp(10+(self.x2-self.x1),WIDTH-10, self.x2-int((move_val)*DELTATIME))
        self.x3 = clamp(0,WIDTH-(self.x4-self.x3), self.x3-int((move_val)*DELTATIME))
        self.x4 = clamp((self.x4-self.x3),WIDTH, self.x4-int((move_val)*DELTATIME))
        self.update_bbox()
        
    def move_right(self, move_val):
        global WIDTH, HEIGHT
        # print(self.x1, self.x2, self.x3, self.x4)
        self.x1 = clamp(10, (WIDTH-10)-(self.x2-self.x1), self.x1+int((move_val)*DELTATIME))
        self.x2 = clamp(10+(self.x2-self.x1),WIDTH-10, self.x2+int((move_val)*DELTATIME))
        self.x3 = clamp(0,WIDTH-(self.x4-self.x3), self.x3+int((move_val)*DELTATIME))
        self.x4 = clamp((self.x4-self.x3),WIDTH, self.x4+int((move_val)*DELTATIME))
        self.update_bbox()
        
class Diamond:
    def __init__(self) -> None:
        x_offset = random.randrange(-230, 230)
        self.x1 = 250+x_offset
        self.y1 = 700
        self.x2 = 265+x_offset 
        self.y2 = 725 
        self.x3 = 235+x_offset
        self.y3 = 725
        self.x4 = 250+x_offset
        self.y4 = 750
        self.update_bbox()
        self.color = random.choice(COLORS)
        
        
    def update_bbox(self):
        self.bbox = {"min_x":min(self.x1,self.x2,self.x3,self.x4), 
                     "min_y":min(self.y1,self.y2,self.y3,self.y4), 
                     "max_x":max(self.x1,self.x2,self.x3,self.x4), 
                     "max_y":max(self.y1,self.y2,self.y3,self.y4)}
        
    def move_down(self, move_val):
        global WIDTH, HEIGHT, DELTATIME
        # print(self.x1, self.x2, self.x3, self.x4)
        # print((self.y1+move_val)*DELTATIME, DELTATIME)
        self.y1 -= int((move_val)*DELTATIME)
        self.y2 -= int((move_val)*DELTATIME)
        self.y3 -= int((move_val)*DELTATIME)
        self.y4 -= int((move_val)*DELTATIME)
        self.update_bbox()
        

def draw_catcher():
    global CATCHER
    glColor3f(*CATCHER.color)
    draw_line(CATCHER.x1, CATCHER.y1, CATCHER.x2, CATCHER.y2)
    draw_line(CATCHER.x2, CATCHER.y2, CATCHER.x4, CATCHER.y4)
    draw_line(CATCHER.x3, CATCHER.y3, CATCHER.x4, CATCHER.y4)
    draw_line(CATCHER.x3, CATCHER.y3, CATCHER.x1, CATCHER.y1)
    
def spwan_diamond():
    global DIAMOND_LIST
    diamond = Diamond()
    DIAMOND_LIST.append(diamond)
    
def draw_diamonds():
    global DIAMOND_LIST
    for diamond in DIAMOND_LIST:
        glColor3f(*diamond.color)
        draw_line(diamond.x1, diamond.y1, diamond.x2, diamond.y2)
        draw_line(diamond.x2, diamond.y2, diamond.x4, diamond.y4)
        draw_line(diamond.x3, diamond.y3, diamond.x4, diamond.y4)
        draw_line(diamond.x3, diamond.y3, diamond.x1, diamond.y1)
# Function to draw a line using the midpoint line drawing algorithm
def draw_line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    x_incr = 1 if x1 < x2 else -1
    y_incr = 1 if y1 < y2 else -1

    if dx > dy:
        d = 2 * dy - dx
        incrE = 2 * dy
        incrNE = 2 * (dy - dx)

        # Set the color to white
        # glColor3f(1.0, 1.0, 1.0)

        glBegin(GL_POINTS)
        for _ in range(dx + 1):
            glVertex2f(x, y)
            if d <= 0:
                d += incrE
            else:
                d += incrNE
                y += y_incr
            x += x_incr
        glEnd()
    else:
        d = 2 * dx - dy
        incrE = 2 * dx
        incrNE = 2 * (dx - dy)

        # Set the color to white
        # glColor3f(1.0, 1.0, 1.0)

        glBegin(GL_POINTS)
        for _ in range(dy + 1):
            glVertex2f(x, y)
            if d <= 0:
                d += incrE
            else:
                d += incrNE
                x += x_incr
            y += y_incr
        glEnd()

def check_collision(bbox1:dict, bbox2:dict=None, x=None, y=None):
    if bbox2:
        return bbox1['min_x'] < bbox2['max_x'] and bbox1['max_x'] > bbox2['min_x'] and bbox1['min_y'] < bbox2['max_y'] and bbox1['max_y'] > bbox2['min_y']
    else:
        return bbox1['min_x'] <= x <= bbox1['max_x'] and bbox1['min_y'] <= y <= bbox1['max_y']
    
RESTART_BBOX = {"min_x":30, "min_y":750, "max_x":60, "max_y":790}    
def draw_restart():
    glColor3f(0, 0.5, 0.5)
    draw_line(30, 770, 40, 790)
    draw_line(30, 770, 40, 750)
    draw_line(30, 770, 60, 770)

PLAY_PAUSE_BBOX = {"min_x":230, "min_y":750, "max_x":270, "max_y":790}      
def play_pause():
    glColor3f(1, 0.75, 0)
    if IS_PAUSED:
        draw_line(230, 770, 270, 790)
        draw_line(230, 770, 270, 750)
        draw_line(270, 790, 270, 750)
    else:
        draw_line(240, 790, 240, 750)
        draw_line(260, 790, 260, 750)

EXIT_BBOX = {"min_x":430, "min_y":750, "max_x":470, "max_y":790}      
def exit_btn():
    glColor3f(1, 0, 0)
    draw_line(430, 790, 470, 750)
    draw_line(430, 750, 470, 790)

def on_pause_click():
    global IS_PAUSED, IS_GAME_OVER
    IS_PAUSED = not IS_PAUSED
    print(IS_PAUSED, IS_GAME_OVER)
    if (not IS_PAUSED) and IS_GAME_OVER:
        on_start()
    
def on_start():
    global IS_PAUSED, SPEED, DIAMOND_LIST, IS_GAME_OVER, SCORE, CATCHER, TIMER, SPWAN_INTERVAL
    IS_PAUSED = IS_GAME_OVER = False
    DIAMOND_LIST.clear()
    SCORE = 0
    SPEED = 100
    SPWAN_INTERVAL = 5
    TIMER = 0
    CATCHER.reset()
    spwan_diamond()
    
def mouse(button, state, x, y):
    global IS_PAUSED
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if check_collision(RESTART_BBOX, x=x, y=800-y):
            on_start()
        elif check_collision(PLAY_PAUSE_BBOX, x=x, y=800-y):
            on_pause_click()
        elif check_collision(EXIT_BBOX, x=x, y=800-y):
            glutLeaveMainLoop()
    glutPostRedisplay()

def special(key, x, y):
    global speed, CATCHER, IS_PAUSED, IS_GAME_OVER
    if IS_PAUSED or IS_GAME_OVER:
        return
    if key == GLUT_KEY_LEFT:
        CATCHER.move_left(500)
    if key == GLUT_KEY_RIGHT:
        CATCHER.move_right(500)
    glutPostRedisplay()

def animate():
    global SPEED, CATCHER, IS_PAUSED, SCORE, IS_GAME_OVER, PREV_FRAME_TIME, DELTATIME, SPWAN_INTERVAL, TIMER
    t0 = time()
    DELTATIME = t0 - PREV_FRAME_TIME
    PREV_FRAME_TIME = t0
    TIMER += DELTATIME
    
    print(SPEED, SPWAN_INTERVAL)
    # print(int(1/DELTATIME))
    # print(TIMER)
    if not IS_PAUSED:
        if TIMER > SPWAN_INTERVAL:
            spwan_diamond()
            SPWAN_INTERVAL -= 0.1
            SPWAN_INTERVAL = clamp(0.5, 5, SPWAN_INTERVAL)
            SPEED += 2
            TIMER = 0
        
        for diamond in DIAMOND_LIST.copy():
            if check_collision(diamond.bbox, CATCHER.bbox):
                DIAMOND_LIST.remove(diamond)
                SCORE += 1
                print(f"Score: {SCORE}")
            if diamond.y1 <=0:
                CATCHER.color_red()
                print(f"GAME OVER! Score: {SCORE}")
                DIAMOND_LIST.clear()
                IS_PAUSED = True
                IS_GAME_OVER = True
                break
            diamond.move_down(SPEED)
    glutPostRedisplay()
    # glutTimerFunc(1000 // 60, timer, 0) # 10 Frame Per second    


CATCHER = Catcher()
spwan_diamond()
# Display function
def display():
    glClear(GL_COLOR_BUFFER_BIT)

    draw_restart()
    play_pause()
    exit_btn()
    
    draw_catcher()
    draw_diamonds()
    glutSwapBuffers()

glutSpecialFunc(special)
glutMouseFunc(mouse)
glutDisplayFunc(display)
# glutTimerFunc(0, timer, 0)

glutIdleFunc(animate)
# Start the main loop
glutMainLoop()
