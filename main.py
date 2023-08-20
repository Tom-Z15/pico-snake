from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
from random import randint
from utime import sleep
import sys


class Game:
    
    def __init__(self):

        self.direction = 'right'
        self.x_cord = randint(0, 128//6) * 6 - 6
        self.y_cord = randint(0, 64//6) * 6 - 6
        self.score = 0
        self.cords = []

        self.point_x_cord = 48
        self.point_y_cord = 24

        self.running = True

        self.buzzer = PWM(Pin(16))

        self.i2c = I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)

        self.oled = SSD1306_I2C(128, 64, self.i2c)

        #buttons handlers and iterupts

        self.buttons = [Pin(_, Pin.IN, Pin.PULL_DOWN) for _ in range(12, 16)]


        for button in self.buttons:
            button.irq(self.__change_direction, Pin.IRQ_RISING)

    #function for changing direction

    def __change_direction(self, pin):
        if pin is self.buttons[0]:
            self.direction = "left"
        elif pin is self.buttons[1]:
            self.direction = "up"
        elif pin is self.buttons[2]:
            self.direction = "right"
        elif pin is self.buttons[3]:
            self.direction = "down"



        
    
    def __die_sound(self):

        self.buzzer.freq(300)

        self.buzzer.duty_u16(15000)

        sleep(0.9)

        self.buzzer.duty_u16(0)

        sleep(1)

    def __eat_sound(self):

        self.buzzer.freq(1500)

        self.buzzer.duty_u16(15000)

        sleep(0.1)

        self.buzzer.duty_u16(0)

        sleep(1)
    
    
    #function for moving our snake

    def __move(self):
        
        if self.direction == "right":
            self.x_cord -= 6
        elif self.direction == "left":
            self.x_cord += 6
        elif  self.direction == "up":
            self.y_cord += 6
        elif self.direction == "down":
            self.y_cord -= 6
        
# fucntion for border of game
    def __border(self):
        if self.x_cord <= 0:  
            self.x_cord = 6;
        elif self.x_cord >= 128:
            self.x_cord = 126
        elif self.y_cord <=0:
            self.y_cord = 6
        elif self.y_cord >= 64:
            self.y_cord = 60

    #adding some points
    def points(self):

        self.oled.fill_rect(self.point_x_cord, self.point_y_cord, 6, 6, 1)

    #drawing tail    
    def __draw_tail(self):

        self.cords.append((self.x_cord, self.y_cord))
        #snake tail logic
        if self.score > 0:
            for i in range(self.score):
                self.oled.fill_rect(self.cords[- i -1 ][0], self.cords[- i -1][1], 4, 4, 1)
        
        if len(self.cords) > self.score:

            self.cords.pop(0)

    # dying because of tail / update also because of border
    def __check_tail(self):

         for i in range (self.score):

            if (self.x_cord, self.y_cord) in self.cords:
               self.__die_sound()
               sys.exit()

    #logic
    def __logic(self):
        
        self.__draw_tail()

        #food logic
        if self.point_x_cord == self.x_cord and self.point_y_cord == self.y_cord: 
            self.point_x_cord = randint(6, 128//6) * 6 - 6
            self.point_y_cord = randint(6, 64//6) * 6 - 6
            self.points()
            self.__eat_sound()
            self.score += 1

    
    

    def mainloop(self):
            while True:
                self.points()
                self.__logic()
                self.__move()
                self.__border()
                self.__check_tail()

                self.oled.fill_rect(self.x_cord, self.y_cord, 6, 6, 1)

                
                self.oled.show()
    
                self.oled.fill(0)

                sleep(1)

            


game = Game()

game.mainloop()
    
    
