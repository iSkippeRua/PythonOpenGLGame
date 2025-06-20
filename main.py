import pygame
import pygame.mixer
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Cube import *
from Camera import *

pygame.init()
pygame.mixer.init()


screen_width = 1000
screen_height = 800
goal_sound = pygame.mixer.Sound("levelcomplete.wav")
loose_sound = pygame.mixer.Sound("levellose.wav")
cube = Cube()
camera = Camera()

MAZE = []
CELL_SIZE = 2
MAZE_HEIGHT = 1
player_x, player_z = 1, 1

level_files = ["level1.txt", "level2.txt", "level3.txt"]
current_level_index = 0

screen = pygame.display.set_mode((screen_width,screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('3D Maze Game')

def Light():
    ambientLight = [0.25, 0.25, 0.0, 1.0]
    diffuseLight = [0.9, 0.9, 0.0, 1.0]
    lightPos = [-50.0, 20.0, -50.0, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0,0.0,0.0,1.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glFrontFace(GL_CCW)
    glEnable(GL_LIGHTING)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glMateriali(GL_FRONT, GL_SHININESS, 10)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def initialise():
    # projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 0.1, 500.0)
    Light()
    #modelview
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)

def camera_init():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)
    camera.update(screen.get_width(), screen.get_height())

def color_wall():
    glColor4f(0.3,0.4,0.8,1)

def color_player():
    glColor3f(1.0, 0.0, 0.0)

def color_goal():
    glColor3f(1.0, 1.0, 0.0)

def draw_wall(x, z):
    glPushMatrix()
    glTranslatef(x * CELL_SIZE + CELL_SIZE / 2, MAZE_HEIGHT / 2, z * CELL_SIZE + CELL_SIZE / 2)
    glScalef(CELL_SIZE, MAZE_HEIGHT, CELL_SIZE)
    color_wall()
    cube.draw()
    glPopMatrix()

def draw_maze():
    for x in range(len(MAZE)):
        for z in range(len(MAZE[0])):
            if MAZE[x][z] == 1:
                draw_wall(x, z)
            elif MAZE[x][z] == 2:
                draw_goal(x, z)

def draw_player():
    glPushMatrix()
    glTranslatef(player_x * CELL_SIZE + CELL_SIZE / 2, CELL_SIZE / 4, player_z * CELL_SIZE + CELL_SIZE / 2)
    glScalef(CELL_SIZE / 2, CELL_SIZE / 2, CELL_SIZE / 2)
    color_player()
    cube.draw()
    glPopMatrix()

def draw_goal(x, z):
    glPushMatrix()
    glTranslatef(x * CELL_SIZE + CELL_SIZE / 2, MAZE_HEIGHT / 2, z * CELL_SIZE + CELL_SIZE / 2)
    glScalef(CELL_SIZE, MAZE_HEIGHT, CELL_SIZE)
    color_goal()
    cube.draw()
    glPopMatrix()

def reset_player_position():
    global player_x, player_z
    player_x, player_z = 1, 1

def move_player(dx, dz):
    global player_x, player_z
    new_x = player_x + dx
    new_z = player_z + dz
    if MAZE[new_x][new_z] == 0 or MAZE[new_x][new_z] == 2:
        player_x = new_x
        player_z = new_z
        if MAZE[new_x][new_z] == 2:
            goal_sound.play()
            load_next_level()

def load_maze_from_file(filename):
    global MAZE
    with open(filename, 'r') as f:
        lines = f.readlines()
        MAZE = []
        for x, line in enumerate(lines):
            row = [int(char) for char in line.strip()]
            MAZE.append(row)

def reset_level():
    loose_sound.play()
    load_maze_from_file(level_files[current_level_index])
    reset_player_position()

def load_next_level():
    global current_level_index
    current_level_index += 1
    if current_level_index < len(level_files):
        load_maze_from_file(level_files[current_level_index])
        reset_player_position()
    else:
        print("Congratulations, you completed all levels!")
        pygame.quit()
        exit()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camera_init()
    load_maze_from_file(level_files[current_level_index])
    draw_maze()
    draw_player()

done = False
initialise()
pygame.mouse.set_visible(False)
while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.mouse.set_visible(True)
            if event.key == pygame.K_w:
                move_player(0, 1)
            if event.key == pygame.K_s:
                move_player(0, -1)
            if event.key == pygame.K_a:
                move_player(1, 0)
            if event.key == pygame.K_d:
                move_player(-1, 0)
            if event.key == pygame.K_r:
                reset_level()
    display()
    pygame.display.flip()
    pygame.time.wait(1000 // 60)
pygame.quit()