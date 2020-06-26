from kivy.graphics import Rectangle, Ellipse, Color, Line
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget


class Rect(Widget):
    def __init__(self, x, y, width, height, color, **kwargs):
        super(Rect, self).__init__()
        self.size = (width, height)
        self.pos = (x, y)
        self.kcol = Color(color[0], color[1], color[2])
        self.kobj = Rectangle(pos=self.pos, size=self.size, **kwargs)
        self.ktype = "GP"

    def resize(self, width, height):
        self.size = (width, height)
        self.kobj.size = self.size

    def move(self, x, y):
        self.pos = (x, y)
        self.kobj.pos = self.pos


class Oval(Widget):
    def __init__(self, x, y, width, height, color, **kwargs):
        super(Oval, self).__init__()
        self.size = (width, height)
        self.pos = (x, y)
        self.kcol = Color(color[0], color[1], color[2])
        self.kobj = Ellipse(pos=self.pos, size=self.size, **kwargs)
        self.ktype = "GP"

    def resize(self, width, height):
        self.size = (width, height)
        self.kobj.size = self.size

    def move(self, x, y):
        self.pos = (x, y)
        self.kobj.pos = self.pos


class Text(Widget):
    def __init__(self, text, **kwargs):
        super(Text, self).__init__()
        self.text = text
        self.kobj = Label(text=self.text, pos=self.pos, **kwargs)
        self.ktype = "WGP"

    def move(self, x, y):
        self.pos = (x, y)
        self.kobj.pos = self.pos

    def set_text(self, text):
        self.text = text
        self.kobj.text = self.text


class Img(Widget):
    def __init__(self, imagepath, **kwargs):
        super(Img, self).__init__()
        self.kobj = Image(source=imagepath, pos=self.pos, size=self.size, **kwargs)
        self.ktype = "WGP"

    def move(self, x, y):
        self.pos = (x, y)
        self.kobj.pos = self.pos

    def resize(self, width, height):
        self.size = (width, height)
        self.kobj.size = self.size


class Btn(Widget):
    def __init__(self, text, onclick, x, y, width, height, **kwargs):
        super(Btn, self).__init__()
        self.text = text
        self.pos = (x, y)
        self.size = (width, height)
        self.kobj = Button(pos=self.pos, size=self.size, text=self.text, on_press=onclick, **kwargs)
        self.ktype = "WGP"

    def move(self, x, y):
        self.pos = (x, y)
        self.kobj.pos = self.pos

    def resize(self, width, height):
        self.size = (width, height)
        self.kobj.size = self.size

    def set_text(self, text):
        self.text = text
        self.kobj.text = text


class Polygon(Widget):
    def __init__(self, points, color,  **kwargs):
        super(Polygon, self).__init__()
        self.points = points
        self.kcol = Color(color[0], color[1], color[2])
        self.kobj = Line(points=self.points, **kwargs)
        self.ktype = "GP"

    def set_points(self, points):
        self.points = points
        self.kobj.points = self.points
