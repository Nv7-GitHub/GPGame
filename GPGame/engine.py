from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window


class GPGame(Widget):
    def __init__(self, **kwargs):
        super(GPGame, self).__init__(**kwargs)
        self.tick = None
        self.window = Window
        self.mousepos = (0, 0)
        self.keys_pressed = []
        self.mousedown = False
        Window.bind(mouse_pos=self.kmousehandler, on_key_down=self.kkeyhandlerdown, on_key_up=self.kkeyhandlerup,
                    on_motion=self.kmouseclick)

    def set_tick(self, tickfunc, interval):
        self.tick = tickfunc
        Clock.schedule_interval(self.tick, interval)

    def run(self, title):
        runner = GPRunner(self, title)
        runner.run()

    def add_component(self, component):
        if component.ktype == "GP":
            self.canvas.add(component.kcol)
            self.canvas.add(component.kobj)
        elif component.ktype == "WGP":
            self.add_widget(component.kobj)

    def remove_component(self, component):
        if component.ktype == "GP":
            self.canvas.remove(component.kcol)
            self.canvas.remove(component.kobj)
        elif component.ktype == "WGP":
            self.remove_widget(component.kobj)

    def kmousehandler(self, w, p):
        self.mousepos = p

    def kmouseclick(self, a, etype, c):
        if etype  == "begin":
            self.mousedown = True
        elif etype == "end":
            self.mousedown = False

    def kkeyhandlerdown(self, keyboard, keycode, whoknows, key, modifiers):
        self.keys_pressed.append(chr(keycode))
        print(keycode)

    def kkeyhandlerup(self, a, b, c):
        del self.keys_pressed[self.keys_pressed.index(chr(b))]


class GPRunner(App):
    def __init__(self, game, title):
        super(GPRunner, self).__init__()

        self.title = title
        self.game = game

    def build(self):
        return self.game
