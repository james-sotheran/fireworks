# Project: Fireworks using Kivy

# Kivy modules
import kivy
kivy.require("1.11.0")
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.properties import ObjectProperty

# Other modules
from random import randint, randrange
from functools import partial
from math import sin, cos
from decimal import Decimal

class FireworkAnimation(FloatLayout):

    def fire(self): # Sets off firework
        self.launch_button = self.ids["btn"] # Loading button from kv to py file
        self.launch_button.opacity = 0 # Makes button dissapear
        # Start and end positions of firework
        self.x_start = randint(0, Window.width)
        self.y_start = 0
        self.x_end = self.x_start
        self.y_end = randint(int(Window.height/4), Window.height)
        self.alpha = 1
        # Launching a firework
        with self.canvas:
            self.canvas.opacity = 1
            self.canvas_color = Color(1, 0, 0, self.alpha, mode = "rgba") # Color of firework
            rocket = Ellipse(pos=(self.x_start, self.y_start), size=(5, 5))
            anim = Animation(pos=(self.x_end, self.y_end), duration=1, step=1/120, transition="out_quad")
            anim.start(rocket)
            anim.bind(on_complete=partial(self.explode, rocket)) # Explodes once firework reaches final position


    def explode(self, rocket, *args):
        self.canvas.remove(rocket) # Removes main rocket
        num_of_sparks = 30 # Number of sparks per explosion
        radius = 100 # Max radius of explosion
        # List of coords to append to
        self.spark_coords = []
        self.final_coord = []
        for i in range(0, num_of_sparks):
            angle = randint(0, 360) # Randomly chooses angle
            multiplier = float(Decimal(randrange(20, 100)/100)) # Sets how far are each spark will be from initial rocket

            # Creates points a random distance and angle from starting point
            x_travel = self.x_end+(multiplier*radius*cos(angle))
            y_travel = self.y_end+(multiplier*radius*sin(angle))

            self.spark_coords.append((x_travel, y_travel))
            self.final_coord.append((randint(0,Window.width), -100))

        for coord in self.spark_coords:
            # Generating random RGB
            rand_red = randint(0, 1)
            rand_green = randint(0, 1)
            rand_blue = randint(0, 1)
            with self.canvas:
                spark_color = Color(rand_red, rand_green, rand_blue, 1, mode="rgba")
                spark = Ellipse(pos=(self.x_end, self.y_end), size=(5, 5))
                #spark_animation = Animation(pos=(coord), duration=0.1) + Animation(pos=(coord[0], coord[1]-Window.height*2), transition="in_quad")
                spark_animation = Animation(pos=(coord), duration=0.1) + Animation(pos=(coord[0], coord[1]-Window.height*2), transition="in_quad")
                color_animation = Animation(a=0.1) # transitions the alpha from 1 to 0.1
            color_animation.start(spark_color)
            spark_animation.start(spark)

        self.fire() # Triggers another firework to go off
class FireworkApp(App):
    def build(self):
        return FireworkAnimation()


if __name__ == "__main__":
    FireworkApp().run()
