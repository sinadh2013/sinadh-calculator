
from turtle import *
from time import *

wn = Screen()
wn.title("sina dh")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

W_S = 5

p_a = Turtle()
p_a.speed(0)
p_a.color("white")
p_a.shape("square")
p_a.shapesize(stretch_wid=5, stretch_len=1)
p_a.penup()
p_a.goto(-350, 0)

p_b = Turtle()
p_b.speed(0)
p_b.color("white")
p_b.shape("square")
p_b.shapesize(stretch_wid=5, stretch_len=1)
p_b.penup()
p_b.goto(350, 0)

b = Turtle()
b.speed(5)
b.color("white")
b.shape("square")
b.penup()
b.goto(0, 0)
b.dx = 2
b.dy = -2

p = Turtle()
p.speed(0)
p.color("white")
p.penup()
p.hideturtle()

def sh_g_o(loser_text):
    p.clear()
    p.goto(0, 0)
    p.write(loser_text, align="center", font=("Arial", 24, "normal"))

def p_a_up():
    y = p_a.ycor()
    if y < 250:
        p_a.sety(y + 20)

def p_a_down():
    y = p_a.ycor()
    if y > -250:
        p_a.sety(y - 20)

def p_b_up():
    y = p_b.ycor()
    if y < 250:
        p_a.sety(y + 20)

def p_b_down():
    y = p_b.ycor()
    if y > -250:
        p_a.sety(y - 20)

wn.listen()
wn.onkeypress(p_a_up, "w")
wn.onkeypress(p_a_down, "s")
wn.onkeypress(p_b_up, "Up")
wn.onkeypress(p_b_down, "Down")

done()