import math
import random
from kivy.config import Config
Config.set('graphics', 'width', '378')
Config.set('graphics', 'height', '570')
# ratio on my phone 6.3/9.5

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.clock import Clock
from kivy.graphics import Color


class VerticalBar(Widget):
    g1 = NumericProperty(0) # so you have to make this a kivy.property for it to be updateable in the kv file 
    g2 = NumericProperty(0)
    # collision
    def collision(self, ball):
        # if the ball goes too right or too left -xVel
        if ball.x <= self.right: #left bar
            ball.xVel = 3
            self.g1 =random.uniform(0, 1)

        if ball.right >= self.xRightBar: #right bar
            ball.xVel = -4
            self.g2 =random.uniform(0, 1)


class HorizontalBar(Widget):
    r = NumericProperty(0)
    # collision
    def collision(self, ball):
        # if ball touch top yVel is changed
        # bottom bar
        if (self.top >= ball.y >= self.y) and (self.x <= ball.center_x <= self.right):
            ball.yVel = 3
            self.r =random.uniform(0, 1)
        # top bar
        if (self.yTopBar <= ball.top <= self.yTopBar+self.size[1]) and (self.x <= ball.center_x <= self.right):
            ball.yVel = -4
            self.r =random.uniform(0, 1)
        # edge case when it hits the pos side xVel changes
        # TODO: edge case

class Ball(Widget):
    xVel = NumericProperty(0)
    yVel = NumericProperty(0)
    
    playerScore = NumericProperty(0)
    botScore = NumericProperty(0)

    def move(self):
        self.pos = (self.pos[0]+self.xVel, self.pos[1]+self.yVel)
    
    def center_ball(self, game):
        self.center = game.center
    def serve_player1(self, game):
        # stop the ball from moving
        self.xVel = 0
        self.yVel = 0
        # send players back to original pos
        game.player1.center = game.center_x, 50
        game.bot1.center = game.center_x, game.height-50
        # serve the ball to player 1
        self.center = game.center_x, game.height/2.5
    def serve_player2(self, game):
        # stop the ball from moving
        self.xVel = 0
        self.yVel = 0
        # send players back to original pos
        game.player1.center = game.center_x, 50
        game.bot1.center = game.center_x, game.height-50
        # serve the ball to player 2
        self.center = game.center_x, game.height - game.height/2.5

     
class Player1(Widget):

    def collision(self, ball):
        #distance thing 
        d_sqrd = (ball.center_x - self.center_x)**2 + (ball.center_y - self.center_y)**2
        r_sqrd = (ball.size[0]/2 + self.size[0]/2)**2
        # math.dist([ball.center_x, ball.center_y], [self.center_x, self.center_y]) another way to do this

        if (d_sqrd <= r_sqrd): #so if there is an intersection i need to find out what quadrant of the pad the ball is hitting 
            #intersection point 
            x_intrsct = math.fabs((ball.center_x + self.center_x)/2) #note value can be -tive
            y_intrsct = math.fabs((ball.center_y + self.center_y)/2) #nn value can be -tive
           #top right quad
            if (x_intrsct > self.center_x) and (y_intrsct > self.center_y):
                # y = mx + c, m=+1 cI = self.center_y - self.center_x
                # normal m=-1 cII = y_intrsct + x_intrsct
                # normal_y = (cI + cII)/2
                normal_y = ((self.center_y - self.center_x) + (y_intrsct + x_intrsct))/2

                if y_intrsct > normal_y:
                    ball.xVel = +2.95
                    ball.yVel = +4  
                elif y_intrsct < normal_y:
                    ball.xVel = +4
                    ball.yVel = +2.95
                # else:
                #     print("does the code ever reach here?nope!")
                #     ball.xVel = +4
                #     ball.yVel = +4

            #bottom right quad
            if (x_intrsct > self.center_x) and (y_intrsct < self.center_y):
                # y = mx + c, m=+1 cI = self.center_y + self.center_x
                # normal m=-1 cII = y_intrsct - x_intrsct
                # normal_y = (cI + cII)/2
                normal_y = ((self.center_y + self.center_x) + (y_intrsct - x_intrsct))/2
                if y_intrsct > normal_y:
                    ball.xVel = +4
                    ball.yVel = -2.95  
                elif y_intrsct < normal_y:
                    ball.xVel = +2.95
                    ball.yVel = -4
            #bottom left quad
            if (x_intrsct < self.center_x) and (y_intrsct < self.center_y):
                # y = mx + c, m=+1 cI = self.center_y - self.center_x
                # normal m=-1, cII = y_intrsct + x_intrsct
                # normal_y = (cI + cII)/2
                normal_y = ((self.center_y - self.center_x) + (y_intrsct + x_intrsct))/2
                if y_intrsct > normal_y:
                    ball.xVel = -4
                    ball.yVel = -2.95
                elif y_intrsct < normal_y:
                    ball.xVel = -2.95
                    ball.yVel = -4
            #top left quad
            if (x_intrsct < self.center_x) and (y_intrsct > self.center_y):
                # y = mx + c, m=+1 cI = self.center_y + self.center_x
                # normal m=-1 cII = y_intrsct - x_intrsct
                # normal_y = (cI + cII)/2
                normal_y = ((self.center_y + self.center_x) + (y_intrsct - x_intrsct))/2

                if y_intrsct > normal_y:
                    ball.xVel = -2.95
                    ball.yVel = +4  
                elif y_intrsct < normal_y:
                    ball.xVel = -4
                    ball.yVel = +2.95

class Bot(Widget):
    # move bot
    xVel = NumericProperty(0)
    yVel = NumericProperty(0)

    gamesCenter_y = 0


    def move(self, game): #this bot just blindly follows the ball wherever
        gamesCenter = game.center_y
        # if the ball is in our box then
        if (game.ball.center_y < game.center_y) and (game.ball.xVel == 0 and game.ball.yVel ==0):
            self.yVel = 0
            self.xVel = 0
        elif game.ball.yVel >= 0:
            # if the ball is above the bot move up
            if (game.ball.center_y > self.center_y) and (self.y >= game.center_y):
                self.yVel = +2.5
            # if the ball is below the bot move down
            if game.ball.center_y < self.center_y:
                self.yVel = -2.5
            # if the ball is on the left move right 
            if game.ball.center_x < self.center_x:
                self.xVel = -2.5
            # if the ball is on the right move left
            if game.ball.center_x > self.center_x:
                self.xVel = +2.5
            if self.y <= game.center_y:
                self.yVel = +2.5
            self.pos = (self.x+self.xVel, self.y+self.yVel)     
          
    # check collision
    def collision(self, ball):
        #distance thing 
        d_sqrd = (ball.center_x - self.center_x)**2 + (ball.center_y - self.center_y)**2
        r_sqrd = (ball.size[0]/2 + self.size[0]/2)**2
        

        if (d_sqrd <= r_sqrd): #so if there is an intersection i need to find out what quadrant of the pad the ball is hitting 
            #intersection point 
            x_intrsct = math.fabs((ball.center_x + self.center_x)/2) #note value can be -tive
            y_intrsct = math.fabs((ball.center_y + self.center_y)/2) #nn value can be -tive
           #top right quad
            if (x_intrsct > self.center_x) and (y_intrsct > self.center_y):
                # y = mx + c, m=+1 cI = self.center_y - self.center_x
                # normal m=-1 cII = y_intrsct + x_intrsct
                # normal_y = (cI + cII)/2
                normal_y = ((self.center_y - self.center_x) + (y_intrsct + x_intrsct))/2

                if y_intrsct > normal_y:
                    ball.xVel = +2.95
                    ball.yVel = +4  
                elif y_intrsct < normal_y:
                    ball.xVel = +4
                    ball.yVel = +2.95
                # else:
                #     print("does the code ever reach here?nope!")
                #     ball.xVel = +4
                #     ball.yVel = +4

            #bottom right quad
            if (x_intrsct > self.center_x) and (y_intrsct < self.center_y):
                # y = mx + c, m=+1 cI = self.center_y + self.center_x
                # normal m=-1 cII = y_intrsct - x_intrsct
                # normal_y = (cI + cII)/2
                normal_y = ((self.center_y + self.center_x) + (y_intrsct - x_intrsct))/2
                if y_intrsct > normal_y:
                    ball.xVel = +4
                    ball.yVel = -2.95  
                elif y_intrsct < normal_y:
                    ball.xVel = +2.95
                    ball.yVel = -4
            #bottom left quad
            if (x_intrsct < self.center_x) and (y_intrsct < self.center_y):
                # y = mx + c, m=+1 cI = self.center_y - self.center_x
                # normal m=-1, cII = y_intrsct + x_intrsct
                # normal_y = (cI + cII)/2
                normal_y = ((self.center_y - self.center_x) + (y_intrsct + x_intrsct))/2
                if y_intrsct > normal_y:
                    ball.xVel = -4
                    ball.yVel = -2.95
                elif y_intrsct < normal_y:
                    ball.xVel = -2.95
                    ball.yVel = -4
            #top left quad
            if (x_intrsct < self.center_x) and (y_intrsct > self.center_y):
                # y = mx + c, m=+1 cI = self.center_y + self.center_x
                # normal m=-1 cII = y_intrsct - x_intrsct
                # normal_y = (cI + cII)/2
                normal_y = ((self.center_y + self.center_x) + (y_intrsct - x_intrsct))/2

                if y_intrsct > normal_y:
                    ball.xVel = -2.95
                    ball.yVel = +4  
                elif y_intrsct < normal_y:
                    ball.xVel = -4
                    ball.yVel = +2.95
            # after they collide the bot should not move
            if (ball.y > self.gamesCenter_y): #and colliding
                self.xVel = 0
                self.yVel = 0

class StartMenu(Widget):
    alpha = NumericProperty(1)
    gameStarted = False
         

    
class Game(Widget):
    vBar_down = ObjectProperty()
    vBar_up = ObjectProperty()
    hBar_left = ObjectProperty()
    hBar_right = ObjectProperty()
    ball = ObjectProperty()
    player1 = ObjectProperty()
    score1 = NumericProperty()
    score2 = NumericProperty()
    bot1 = ObjectProperty()
    start_menu = ObjectProperty()
    
    def update(self, dt):
        self.ball.move()
        self.bot1.move(self)

        self.player1.collision(self.ball)
        self.bot1.collision(self.ball)

        self.vBar_down.collision(self.ball)
        self.vBar_up.collision(self.ball)
        self.hBar_left.collision(self.ball)
        self.hBar_right.collision(self.ball)

        if (self.ball.y+self.ball.height < 0):
            # uodate the score
            self.score1 += 1
            self.ball.serve_player1(self)
        if (self.ball.y > self.height):
            # uodate the score
            self.score2 += 1
            self.ball.serve_player2(self)

    
    
    def on_touch_move(self, touch):
        #player1 input 
        if (touch.y <= self.center_y-self.player1.height/2) and (self.player1.width/2 <= touch.x <= self.width-self.player1.width/2):
            self.player1.center = (touch.x, touch.y)
        
        
        
    def on_touch_down(self, touch):
        if self.start_menu.gameStarted == False:
            self.start_menu.clear_widgets()
            self.start_menu.alpha = 0
        
            #player1 input 
            if (touch.y < self.center_y-self.player1.height/2 ) and (self.player1.width/2 <= touch.x <= self.width-self.player1.width/2):
                self.player1.center = (touch.x, touch.y)




class GlowApp(App):
    def build(self):
        game = Game()
        Clock.schedule_interval(game.update, 0.10/60.0)
        return game

if __name__ == '__main__':
    GlowApp().run()