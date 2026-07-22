"""
sinadh — Calculator
A simple, real Android app built with Python + Kivy.
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hexc

# ---- Theme (green / black / white) ----
BG_COLOR = hexc("#0A0F0A")
PANEL_COLOR = hexc("#121A12")
GREEN = hexc("#3ECF5F")
GREEN_DIM = hexc("#1F6B34")
WHITE = hexc("#F4F6F4")
GRAY = hexc("#7A877C")
KEY_COLOR = hexc("#1A231A")

Window.clearcolor = BG_COLOR


class RoundButton(Button):
    """A button with rounded corners and a flat color background."""

    def __init__(self, bg_color=KEY_COLOR, fg_color=WHITE, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ""
        self.background_down = ""
        self.color = fg_color
        self.font_size = "26sp"
        self.bold = True
        self._bg_color = bg_color
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(radius=[24], pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class CalculatorLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=18, spacing=10, **kwargs)

        # ---- Brand header ----
        self.add_widget(
            Label(
                text="[b]s i n a d h[/b]",
                markup=True,
                color=GREEN,
                font_size="16sp",
                size_hint=(1, 0.08),
            )
        )

        # ---- Display ----
        display_box = BoxLayout(
            orientation="vertical",
            size_hint=(1, 0.28),
            padding=(10, 0),
        )
        self.expr_label = Label(
            text="",
            color=GRAY,
            font_size="20sp",
            halign="right",
            valign="bottom",
            size_hint=(1, 0.35),
        )
        self.expr_label.bind(size=self._update_text_align)

        self.result_label = Label(
            text="0",
            color=WHITE,
            font_size="52sp",
            halign="right",
            valign="bottom",
            size_hint=(1, 0.65),
        )
        self.result_label.bind(size=self._update_text_align)

        display_box.add_widget(self.expr_label)
        display_box.add_widget(self.result_label)
        self.add_widget(display_box)

        # ---- Keypad ----
        grid = GridLayout(cols=4, spacing=10, size_hint=(1, 0.64))

        buttons = [
            ("C", "func"), ("±", "func"), ("%", "func"), ("÷", "op"),
            ("7", "num"), ("8", "num"), ("9", "num"), ("×", "op"),
            ("4", "num"), ("5", "num"), ("6", "num"), ("−", "op"),
            ("1", "num"), ("2", "num"), ("3", "num"), ("+", "op"),
            ("0", "num"), (".", "num"), ("=", "eq"),
        ]

        self.current = "0"
        self.previous = None
        self.operator = None
        self.just_evaluated = False

        for label, kind in buttons:
            if kind == "op":
                btn = RoundButton(text=label, bg_color=GREEN_DIM, fg_color=WHITE)
            elif kind == "func":
                btn = RoundButton(text=label, bg_color=hexc("#1C231C"), fg_color=GREEN)
            elif kind == "eq":
                btn = RoundButton(text=label, bg_color=GREEN, fg_color=hexc("#06210D"))
            else:
                btn = RoundButton(text=label, bg_color=KEY_COLOR, fg_color=WHITE)

            btn.bind(on_press=self.on_key)
            grid.add_widget(btn)

        self.add_widget(grid)

    def _update_text_align(self, instance, value):
        instance.text_size = instance.size

    def render(self):
        self.result_label.text = self.current
        if self.operator and self.previous is not None:
            self.expr_label.text = f"{self.previous} {self.operator}"
        else:
            self.expr_label.text = ""

    def format_num(self, n):
        if n is None:
            return "خطا"
        if n == int(n):
            n = int(n)
        s = str(n)
        if len(s) > 12:
            n = round(n, 6)
            s = str(n)
        return s

    def compute(self, a, b, op):
        a, b = float(a), float(b)
        if op == "+":
            return a + b
        if op == "−":
            return a - b
        if op == "×":
            return a * b
        if op == "÷":
            return None if b == 0 else a / b

    def on_key(self, instance):
        key = instance.text

        if key.isdigit():
            if self.just_evaluated:
                self.current = key
                self.just_evaluated = False
            else:
                self.current = key if self.current == "0" else self.current + key

        elif key == ".":
            if self.just_evaluated:
                self.current = "0."
                self.just_evaluated = False
            elif "." not in self.current:
                self.current += "."

        elif key == "C":
            self.current = "0"
            self.previous = None
            self.operator = None
            self.just_evaluated = False

        elif key == "±":
            if self.current != "0":
                self.current = self.current[1:] if self.current.startswith("-") else "-" + self.current

        elif key == "%":
            self.current = self.format_num(float(self.current) / 100)

        elif key in ("+", "−", "×", "÷"):
            if self.operator and not self.just_evaluated:
                result = self.compute(self.previous, self.current, self.operator)
                self.current = self.format_num(result)
                self.previous = self.current
            else:
                self.previous = self.current
            self.operator = key
            self.just_evaluated = True

        elif key == "=":
            if self.operator is not None and self.previous is not None:
                result = self.compute(self.previous, self.current, self.operator)
                self.current = self.format_num(result)
                self.previous = None
                self.operator = None
                self.just_evaluated = True

        self.render()


class SinadhApp(App):
    def build(self):
        self.title = "sinadh"
        return CalculatorLayout()


if __name__ == "__main__":
    SinadhApp().run()
