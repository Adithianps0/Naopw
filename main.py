import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
import math
import time

# Initialize OpenGL and Pygame
def init_game():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)

    # Enable lighting and create a nighttime ambiance
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)  # Main light
    glEnable(GL_LIGHT1)  # Dynamic RGB light

    # Set ambient lighting to a low value (darkness for night)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))

# Create a ball character
def draw_ball():
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)  # Red ball
    glutSolidSphere(1, 20, 20)
    glPopMatrix()

# Create the ground with dark colors for night
def draw_ground():
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.2, 0.0)  # Dark green ground
    glVertex3f(-10, -1, 10)
    glVertex3f(10, -1, 10)
    glVertex3f(10, -1, -10)
    glVertex3f(-10, -1, -10)
    glEnd()

# Create a function to handle RGB dynamic lighting
def setup_dynamic_lighting():
    # Dynamic RGB light values
    time_val = time.time() % 1
    red = abs(math.sin(time_val * math.pi * 2))
    green = abs(math.sin((time_val + 0.33) * math.pi * 2))
    blue = abs(math.sin((time_val + 0.66) * math.pi * 2))

    # Set RGB light in a position above the ball
    light_position = [0, 5, -5, 1]
    glLightfv(GL_LIGHT1, GL_POSITION, light_position)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (red, green, blue, 1.0))

# Joystick and swipe detection
class GameControls(Widget):
    def __init__(self, **kwargs):
        super(GameControls, self).__init__(**kwargs)
        self.ball_pos = [0, 0, 0]
        self.jump_velocity = 0
        self.is_jumping = False

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            self.is_jumping = True
            self.jump_velocity = 0.2  # Jump speed

    def on_touch_move(self, touch):
        if touch.x < Window.width * 0.5:
            # Swipe left/right
            if touch.dx < 0:
                self.ball_pos[0] -= 0.2  # Move left
            elif touch.dx > 0:
                self.ball_pos[0] += 0.2  # Move right
        else:
            # Swipe up for jumping
            if touch.dy > 0:
                self.is_jumping = True
                self.jump_velocity = 0.2

    def update(self):
        # Gravity
        if self.is_jumping:
            self.ball_pos[1] += self.jump_velocity
            self.jump_velocity -= 0.01  # Simulate gravity
            if self.ball_pos[1] <= 0:  # Back to ground level
                self.ball_pos[1] = 0
                self.is_jumping = False

        # Update the ball position

# Main game loop
def game_loop():
    init_game()
    controls = GameControls()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        controls.update()

        # Clear and redraw scene
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Set up RGB lighting
        setup_dynamic_lighting()

        # Draw objects
        glPushMatrix()
        glTranslatef(controls.ball_pos[0], controls.ball_pos[1], controls.ball_pos[2])
        draw_ball()  # Draw ball character
        glPopMatrix()

        draw_ground()  # Draw ground

        pygame.display.flip()
        clock.tick(60)

# Kivy app for touch interface
class GameApp(App):
    def build(self):
        layout = FloatLayout()
        game_area = RelativeLayout(size_hint=(1, 0.8))
        layout.add_widget(game_area)

        # Adding touch controls via Kivy
        controls = GameControls()
        layout.add_widget(controls)
        return layout

# Run the game
if __name__ == '__main__':
    GameApp().run()
    game_loop()
