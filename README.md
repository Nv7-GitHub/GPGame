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
An oval has the same parameters as a Rect, x, y, width, height, color. I am going to create a Cyan ball in the center of the screen. But how do we put it in the center of the screen?
A GPGame object has a window attribute. This attribute is just a kivy.core.window.Window object. This attribute has a width and height attribute. The center of the screen has an x of width/2, and a y of height/2. To do this, the code would be ```ball = Oval(game.window.width/2, game.window.height/2, 100, 100, (0, 1, 1))```. To add this to the game, I am going to put a add_component call. The code now is below.
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
