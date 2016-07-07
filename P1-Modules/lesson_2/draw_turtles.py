import turtle

def draw_petals(petals) :
    petals.pu()
    petals.setpos(-200,0)
    petals.pd()
    
    for i in range(36) :
        petals.left(35)
        petals.forward(50)
        petals.right(35)
        petals.forward(50)
        petals.right(145)
        petals.forward(50)
        petals.right(35)
        petals.forward(50)
        petals.right(10)

def draw() :
    window = turtle.Screen()
    window.bgcolor("light gray")

    petals = turtle.Turtle()
    petals.shape("turtle")
    petals.color("green")
    petals.speed(10)

    draw_petals(petals)

    petals.setheading(270)
    petals.forward(200)

    window.exitonclick()

draw()

    
