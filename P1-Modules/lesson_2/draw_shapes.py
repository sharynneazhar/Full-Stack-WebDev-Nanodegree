# library that draws shapes on the screen
import turtle

def draw_square() :
    brad = turtle.Turtle()
    brad.shape("turtle")
    brad.color("green")
    brad.speed(5)

    for i in range(36) :
        for x in range(4) :
            brad.forward(100)
            brad.right(90)
        brad.right(10)

def draw_circle() :
    angie = turtle.Turtle()
    angie.shape("arrow")
    angie.color("blue")
    angie.circle(100)

def draw_triangle() :
    john = turtle.Turtle()
    john.shape("triangle")
    john.color("red")
    john.speed(2)

    for x in range(3) :
        john.forward(100)
        john.right(120)

def draw_all() :
    window = turtle.Screen()
    window.bgcolor("light gray")

    draw_square()
    draw_circle()
    draw_triangle()

    window.exitonclick()

draw_square()
