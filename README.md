# GPGame
GPGame is an abstraction layer on the Kivy GPU accelerated engine.

## Why GPGame?
Games using Kivy often have a lot of unnecessary code for the OOP. GPGame makes code shorter, makes coding games faster, and makes code more readable. In my examples I am going to be using Pong, a simple game. I am going to measure simplicity by lines of code, although I have also found that GPGame code is more readable. Below is Pong using only Kivy.

```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Rectangle
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.label import Label


class Rect(Widget):
    def __init__(self, player, **kwargs):
        super(Rect, self).__init__(**kwargs)

        self.rectpos = Window.height/2
        self.rect = Rectangle(size=(30, 100), pos=([30 if player else Window.width - 60][0], self.rectpos))
        self.canvas.add(self.rect)

    def update(self):
        self.rect.pos = (self.rect.pos[0], self.rectpos)


class Ball(Widget):
    ball = ObjectProperty(None)

    def __init__(self, size, **kwargs):
        super(Ball, self).__init__(**kwargs)

        self.velocityx = 800
        self.velocityy = 800
        self.ellipse = Ellipse(pos=self.pos, size=(size, size))
        self.canvas.add(self.ellipse)

    def update(self, dt):
        self.pos = Vector(self.velocityx*dt, self.velocityy*dt) + self.pos
        self.ellipse.pos = self.pos


class Pong(Widget):
    def __init__(self, **kwargs):
        super(Pong, self).__init__(**kwargs)

        self.ball = Ball(100)
        self.canvas.add(self.ball.ellipse)

        self.score = 0

        self.mousepos = Window.height/2
        Window.bind(mouse_pos=self.mousehandler)

        self.player = Rect(True)
        self.ai = Rect(False)

        self.canvas.add(self.player.rect)
        self.canvas.add(self.ai.rect)

    def update(self, dt):
        self.ball.update(dt)
        self.player.update()
        self.ai.update()

        if (self.ball.x < 0) or (self.ball.right > (self.width - 60)):
            self.ball.velocityx *= -1
            if self.ball.x < 0:
                self.gameover()

        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocityy *= -1

        self.player.rectpos = self.mousepos
        self.ai.rectpos = self.ball.ellipse.pos[1]

        if (self.ball.x < 60) and (self.player.rectpos in range(round(self.ball.ellipse.pos[1]-50),
                                                                round(self.ball.ellipse.pos[1]+50))):
            self.score += 1
            self.ball.velocityx *= -1

    def gameover(self):
        self.canvas.clear()
        Window.clearcolor = (1, 1, 1, 1)
        label = Label(text="[b]Game Over. Your final score was " + str(self.score) + ".[/b]", font_size="45sp",
                      valign="center", pos=(Window.width/2, Window.height/2), color=(0, 0, 0, 1), markup=True)
        self.add_widget(label)

    def mousehandler(self, w, p):
        self.mousepos = p[1]


class Main(App):
    def build(self):
        self.title = "Pong"
        self.game = Pong()
        Clock.schedule_interval(self.game.update, 1 / 360)
        Clock.schedule_interval(self.update, 1 / 360)
        return self.game

    def update(self, dt):
        self.title = "Pong - Score: " + str(self.game.score)


if __name__ == "__main__":
    Main().run()

```
This program was 105 lines! I noticed that there was a lot of repeated code, like defining a boilerplate class, and creating widgets that could move around. GPGame already has simple objects for commonly used widgets, in addition to a GPGame object that creates a boilerplate game with input handling and mouse movement handling.
## How to create Pong
### Creating an empty GPGame
A basic game in GPGame simply requires 4 lines! To create an empty game in GPGame, you have to import GPGame, and run! Code is below.
```python
from GPGame.engine import GPGame
game = GPGame()
if __name__ == "__main__":
    game.run("Tutorial")
```
Line 1 imports GPGame. The main GPGame object is within engine. A GPGame object is a child of the Kivy Widget. To import, just run ```from GPGame.engine import GPGame```.
Line 2 creates a GPGame. To create a GPGame, just instantiate a class. 
Line 4 runs GPGame. A GPGame class has a run method. The run method accepts a title parameter. This title parameter will be the title of the window.

### Adding a Rectangle for the paddle
For the paddle, we are going to use a rectangle. All canvas items in GPGame are called components. Components are Kivy Widget classes with some methods. Components have their kivy object stored in the kobj attribute. Most of the time you will not need this. A Rect has a kivy.graphics.Rectangle for this.
All components are under the components.py file. To import components, just run ```from GPGame.components import Rect```
Once you have imported Rect, instantiate a rect objects. A rect object accepts the parameters x, y, width, height, and color. color is a 3 item tuple containing a value from 0 to 1 for r, g, and b.
For Pong, we are going to instantiate a Rect with an x of 10, a y of 0, a width of 10, and a height of 100. Since the default background color of a window is black, I am going to make the paddle white by setting the color to (1, 1, 1). The code for this is ```paddle = Rect(10, 0, 10, 100, (1, 1, 1))```
Finally, add this component to the game for it to be rendered. To do this, a GPGame object has a add_component method. This method will add the component. To reverse this, use remove_component. We will put ```game.add_component(paddle)```.
Now, the code is:
```python
from GPGame.engine import GPGame
from GPGame.components import Rect

game = GPGame()
paddle = Rect(0, 0, 10, 100, (1, 1, 1))
game.add_component(paddle)

if __name__ == "__main__":
    game.run("Tutorial")

```
When we run this, we see a rectangle in the bottom right corner of the screen (0, 0)! Congratulations!
![Screenshot of game at this step](https://i.imgur.com/YWXeMeh.png)

## The Ball
For the ball, we are going to use an Oval object. This object can also be imported from the the components. To do this, use ```from GPGame.components import Oval``` I am going to add this to the rectangle import, changing the line to ```from GPGame.components import Rectangle, Oval```.
An Oval's kobj is a ```kivy.graphics.Ellipse``` object. An oval has the same parameters as a Rect, x, y, width, height, color. We are going to create a Cyan ball in the center of the screen. But how do we put it in the center of the screen?
A GPGame object has a window attribute. This attribute is just a ```kivy.core.window.Window``` object. This attribute has a width and height attribute. The center of the screen has an x of width/2, and a y of height/2. To do this, the code would be ```ball = Oval(game.window.width/2, game.window.height/2, 100, 100, (0, 1, 1))```. To add this to the game, I am going to put a add_component call. The code now is below.
```python
from GPGame.engine import GPGame
from GPGame.components import Rect, Oval

game = GPGame()
paddle = Rect(10, 0, 10, 100, (1, 1, 1))
ball = Oval(game.window.width/2, game.window.height/2, 100, 100, (0, 1, 1))
game.add_component(paddle)
game.add_component(ball)

if __name__ == "__main__":
    game.run("Tutorial")

```
Now, our game looks like this.
![Screenshot of the game with the ball](https://i.imgur.com/z1k2BJi.png)

## The Text
For the text we are going to use a Text object. Being a component, we can add this in the imports, changing the line to ```from GPGame.components import Rect, Oval, Text```. 
The Text kobj attribute is a ```kivy.uix.label.Label```. To modify this text, put arguments that would modify kivy Labels, like color, which is a tuple with rgba, and font_size, which is a number with multiple possible extensions. For this, I am going to use sp. 
I am going to create a Text object centered horizontally on the top of the window. To do this, I am once again going to use the ```game.window```. But before this, lets create a variable which would contain the score, called score. I am just going to put ```score = 0```. After that, I am going to instantiate the Text using ```scoredisplay = Text(str(score), font_size="75sp")```. Finally, I am going to move it using ```scoredisplay.move(game.window.width/2, game.window.height-150)``` Finally, add the component to the game. The code now is below.
```python
from GPGame.engine import GPGame
from GPGame.components import Rect, Oval, Text

game = GPGame()
paddle = Rect(10, 0, 10, 100, (1, 1, 1))
ball = Oval(game.window.width/2, game.window.height/2, 100, 100, (0, 1, 1))
score = 0
scoredisplay = Text(str(score), font_size="75sp")
scoredisplay.move(game.window.width/2, game.window.height-150)
game.add_component(paddle)
game.add_component(ball)
game.add_component(scoredisplay)


if __name__ == "__main__":
    game.run("Tutorial")

```
Now, there is some text on the top of the screen that says "0". It looks like this.
![Screenshot of game with score display](https://i.imgur.com/RLiGVxx.png)

## CPU Paddle
Do this in a similar fashion to the player's paddle. The code is ```cpupaddle = Rect(game.window.width - 20, 0, 10, 100, (1, 1, 1))``` and then use add_component.
Now, the code is
```python
from GPGame.engine import GPGame
from GPGame.components import Rect, Oval, Text

game = GPGame()
paddle = Rect(10, 0, 10, 100, (1, 1, 1))
ball = Oval(game.window.width/2, game.window.height/2, 100, 100, (0, 1, 1))
score = 0
scoredisplay = Text(str(score), font_size="75sp")
scoredisplay.move(game.window.width/2, game.window.height-150)
cpupaddle = Rect(game.window.width - 20, 0, 10, 100, (1, 1, 1))

game.add_component(paddle)
game.add_component(ball)
game.add_component(scoredisplay)
game.add_component(cpupaddle)


if __name__ == "__main__":
    game.run("Tutorial")
```
Now, our game looks like this.
![With CPU Paddle](https://i.imgur.com/mD5A9Xt.png)

## Creating a tick function
A tick function is a function that runs every frame. This is very useful in games. GPGame has a method to create tick functions built right in. 
First, create a function after the initialization (instantiating objects, adding components, etc.), but before you use the GPGame.run method. Create one parameter, which will be the dt. This parameter contains the time it has been since the tick function was last called. Finally, create a line before the GPGame.run line, and use the GPGame.set_tick method. The first paramater is going to be the tick function, and the second one is going to be the minimum time interval. I am going to make this to 1/60, for 60FPS.
Now, our code looks like this:
```python
from GPGame.engine import GPGame
from GPGame.components import Rect, Oval, Text

game = GPGame()
paddle = Rect(10, 0, 10, 100, (1, 1, 1))
ball = Oval(game.window.width/2, game.window.height/2, 100, 100, (0, 1, 1))
score = 0
scoredisplay = Text(str(score), font_size="75sp")
scoredisplay.move(game.window.width/2, game.window.height-150)
cpupaddle = Rect(game.window.width - 20, 0, 10, 100, (1, 1, 1))

game.add_component(paddle)
game.add_component(ball)
game.add_component(scoredisplay)
game.add_component(cpupaddle)


def tick(dt):
    pass

game.set_tick(tick, 1/60)
if __name__ == "__main__":
    game.run("Tutorial")

```
## Having the ball bounce around
Now, we are going to work in the tick function. The first step is to make the ball bounce around. To do this, make two variables, one called ballvelx, and one called ballvely. We will set these both to 400. This will be the velocity of our ball. 
To move the ball, we are going to use the move method. All components have a move method. To make the ball move, we will use the line of code following: ```ball.move(ball.pos[0] + ballvelx*dt, ball.pos[1] + ballvely*dt)```. The 2 parameters are the x and y location. To make it translate, we add the current pos, which is an x,y tuple in the pos attribute to the translation. To calculate the translation, we are multiplying the velocity by the difference in time between frames. We multiply by dt so that even if the game is running slowly, the ball will move at the same speed. 
Finally, to make the ball bounce, we will add the following if statements. 
```python
    if (ball.pos[0] < 0) or (ball.pos[0] > game.window.width - 120):
        ballvelx *= -1

    if (ball.pos[1] < 0) or (ball.pos[1] > game.window.height - 100):
        ballvely *= -1
```
In both of these if statements, the first part checks if it is past the bottom/left sides of the screen, and the second part checks if it is past the top/right side of the screen. When checking for the right side of the screen, It does 20pixels away from the right side of the screen, because since the CPU is basically just an animation and will always hit the ball, there is no point in actually checking if the CPU hits. Now, our code looks like this.
```python
from GPGame.engine import GPGame
from GPGame.components import Rect, Oval, Text

game = GPGame()
paddle = Rect(10, 0, 10, 100, (1, 1, 1))
ball = Oval(game.window.width/2, game.window.height/2, 100, 100, (0, 1, 1))
score = 0
scoredisplay = Text(str(score), font_size="75sp")
scoredisplay.move(game.window.width/2, game.window.height-150)
cpupaddle = Rect(game.window.width - 20, 0, 10, 100, (1, 1, 1))
ballvelx = 400
ballvely = 400

game.add_component(paddle)
game.add_component(ball)
game.add_component(scoredisplay)
game.add_component(cpupaddle)


def tick(dt):
    global ballvely, ballvelx, score
    ball.move(ball.pos[0] + ballvelx*dt, ball.pos[1] + ballvely*dt)

    if (ball.pos[0] < 0) or (ball.pos[0] > game.window.width - 120):
        ballvelx *= -1

    if (ball.pos[1] < 0) or (ball.pos[1] > game.window.height - 100):
        ballvely *= -1


game.set_tick(tick, 1/60)
if __name__ == "__main__":
    game.run("Tutorial")

```
Now, it looks like this (warning: this is not the actual FPS. screen recording software was just slow.)
![GIF with ball bouncing](https://i.imgur.com/qw1x6tf.gif)

## Making the paddle mouve with mouse and the cpu paddle move with the ball
Now, we have to add user input. First though, we are going to do the CPU. To do the CPU, we are just going to set the CPU Y position to the paddles Y position. We can acheive this by putting this line of code in out tick function: ```cpupaddle.move(cpupaddle.pos[0], ball.pos[1])```. Now, out CPU moves with the ball, and our ball is no longer bouncing off of thin air (if there is air in a game?)! Next, the user input.
A GPGame class has a mousepos attribute. This is an x,y tuple with the position of the mouse. (WARNING: This is 0, 0 until the user moves their mouse) We are just going to set the y position of the ball to be the y position of the mouse. We can do this with this line of code: ```paddle.move(paddle.pos[0], game.mousepos[1])```. Now, the paddle moves with the player's mouse! The code now looks like this:
```python
from GPGame.engine import GPGame
from GPGame.components import Rect, Oval, Text

game = GPGame()
paddle = Rect(10, 0, 10, 100, (1, 1, 1))
ball = Oval(game.window.width/2, game.window.height/2, 100, 100, (0, 1, 1))
score = 0
scoredisplay = Text(str(score), font_size="75sp")
scoredisplay.move(game.window.width/2, game.window.height-150)
cpupaddle = Rect(game.window.width - 20, 0, 10, 100, (1, 1, 1))
ballvelx = 400
ballvely = 400

game.add_component(paddle)
game.add_component(ball)
game.add_component(scoredisplay)
game.add_component(cpupaddle)


def tick(dt):
    global ballvely, ballvelx, score
    ball.move(ball.pos[0] + ballvelx*dt, ball.pos[1] + ballvely*dt)

    if (ball.pos[0] < 0) or (ball.pos[0] > game.window.width - 120):
        ballvelx *= -1

    if (ball.pos[1] < 0) or (ball.pos[1] > game.window.height - 100):
        ballvely *= -1

    cpupaddle.move(cpupaddle.pos[0], ball.pos[1])
    paddle.move(paddle.pos[0], game.mousepos[1])


game.set_tick(tick, 1/60)
if __name__ == "__main__":
    game.run("Tutorial")

```
And the game now looks like this (The screen recording software does not capture my mouse, but I assure you the paddle is following my mouse).

![GIF with user input](https://i.imgur.com/U8633Fb.gif)

## Making the score change with paddle and making the ball bounce
Now, we have to make the ball bounce off of the paddle and the score change. We can do this by just checking if the ball y is in the range of the paddle. I am sure there is a much better way of doing this but this is the most readable way I could find. To change the text of the score, we will use the Text set_text method. Finally, we will multiply the ball velocity so that it gets faster as the score goes higher. The code below acheives the score changing and ball bouncing.
```python
        if (ball.pos[0] < 20) and (round(ball.pos[1]) in range(round(paddle.pos[1]-100), round(paddle.pos[1] + 100))):
            score += 1
            scoredisplay.set_text(str(score))
            ballvelx *= -1

            ballvelx *= 1.1
            ballvely *= 1.1
```
Now, our program looks like this:
```python
from GPGame.engine import GPGame
from GPGame.components import Rect, Oval, Text

game = GPGame()
paddle = Rect(10, 0, 10, 100, (1, 1, 1))
ball = Oval(game.window.width/2, game.window.height/2, 100, 100, (0, 1, 1))
score = 0
scoredisplay = Text(str(score), font_size="75sp")
scoredisplay.move(game.window.width/2, game.window.height-150)
cpupaddle = Rect(game.window.width - 20, 0, 10, 100, (1, 1, 1))
ballvelx = 400
ballvely = 400

game.add_component(paddle)
game.add_component(ball)
game.add_component(scoredisplay)
game.add_component(cpupaddle)


def tick(dt):
    global ballvely, ballvelx, score
    ball.move(ball.pos[0] + ballvelx*dt, ball.pos[1] + ballvely*dt)

    if (ball.pos[0] < 0) or (ball.pos[0] > game.window.width - 120):
        ballvelx *= -1

    if (ball.pos[1] < 0) or (ball.pos[1] > game.window.height - 100):
        ballvely *= -1

    cpupaddle.move(cpupaddle.pos[0], ball.pos[1])
    paddle.move(paddle.pos[0], game.mousepos[1])

    if (ball.pos[0] < 20) and (round(ball.pos[1]) in range(round(paddle.pos[1] - 100), round(paddle.pos[1] + 100))):
        score += 1
        scoredisplay.set_text(str(score))
        ballvelx *= -1

        ballvelx *= 1.1
        ballvely *= 1.1


game.set_tick(tick, 1/60)
if __name__ == "__main__":
    game.run("Tutorial")
```
And our game looks like this! (again, it is not actually this slow) Also, you can see that when it bounces off the wall, the score does not change:
![Game with ball bouncing off of paddle and score changing](https://i.imgur.com/R7St9za.gif)
