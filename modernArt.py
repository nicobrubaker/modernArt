# By Nico Brubaker, applying 9th grade

from tkinter import *
from webbrowser import open_new
from random import randint, choice
from PIL import Image, ImageDraw
from os import remove

root = Tk()

root.wm_title("Mondrian Generator")

runAgain = Button(root, text="Generate Another!")
runAgain.pack()

save = Button(root, text="Open in your default photo viewer")
save.pack()

thick = randint(10, 20)

cht = randint(500, 700)

cwd = cht + randint(-(1*(cht//3)), 1*(cht//3))

while cwd < 8*thick:
    cwd = cht + randint(-(1*(cht//3)), 1*(cht//3))

c = Canvas(root, width=cwd+1, height=cht+1, highlightthickness=0, borderwidth=0)

image = Image.new("RGB", (cwd, cht), (255, 255, 255))
m_draw = ImageDraw.Draw(image)


def find_endpoints(x1, y1, x2):
    if x1 == x2:
        s = c.find_overlapping(x1, 0, x1, cht+2)

        intersections = []

        for item in s:
            cs = c.coords(item)
            intersections.append([x1, cs[1]])

    else:
        s = c.find_overlapping(0, y1, cwd+2, y1)

        intersections = []

        for item in s:
            cs = c.coords(item)
            intersections.append([cs[0], y1])

    return intersections


def split():
    if randint(0, 1) == 0:
        # Draw vert split 4thk away from other split
        lx = 0
        print("X:", badX)
        while False in [abs(lx-i) > 3*thick for i in badX]:  # find the x-value of the line
            lx = randint(0, cwd)

        s = find_endpoints(lx, 0, lx)

        st = choice(s)
        s.pop(s.index(st))
        end = choice(s)

        c.create_line(st[0], st[1], end[0], end[1], width=thick)
        m_draw.line([st[0], st[1], end[0], end[1]], (0, 0, 0), thick)

        badX.append(lx)

    else:
        # horiz split same rules
        ly = 0
        print("Y:", badY)
        while False in [abs(ly-i) > 3*thick for i in badY]:
            ly = randint(0, cht)

        s = find_endpoints(0, ly, cwd)

        st = choice(s)
        s.pop(s.index(st))
        end = choice(s)

        c.create_line(st[0], st[1], end[0], end[1], width=thick)
        m_draw.line([st[0], st[1], end[0], end[1]], (0, 0, 0), thick)

        badY.append(ly)


def color():
    data = list(image.getdata())
    real_data = []

    for i in range(int(len(data)/(cwd+1))):
        x = []
        for j in range(cwd):
            x.append(data[j])
        real_data.append(x)
    colors = [(255, 0, 0), (0, 0, 255), (255, 255, 0)]

    for i in range(randint(1, 5)):
        x = randint(1, cwd)
        y = randint(1, cht)
        ImageDraw.floodfill(image, (x, y), choice(colors), (0, 0, 0))


def draw():
    global badX
    global badY
    global thick
    global root
    global final_show

    badX = [0, cwd]
    badY = [0, cht]
    c.delete(ALL)

    c.create_line(0, 0, cwd, 0)
    c.create_line(cwd, 0, cwd, cht)
    c.create_line(cwd, cht, 0, cht)
    c.create_line(0, cht, 0, 0)

    m_draw.line([0, 0, cwd - 1, 0], (0, 0, 0))
    m_draw.line([cwd - 1, 0, cwd - 1, cht - 1], (0, 0, 0))
    m_draw.line([cwd - 1, cht - 1, 0, cht - 1], (0, 0, 0))
    m_draw.line([0, cht - 1, 0, 0], (0, 0, 0))

    for i in range(randint(4, 25-thick)):
        split()

    color()

    image1 = image.crop((1, 1, cwd-1, cht-1))

    c.delete(ALL)

    image1.save("temp.gif")
    final_show = PhotoImage(file="temp.gif")
    remove("temp.gif")
    c["width"] = cwd - 2
    c["height"] = cht - 2
    c.create_image(0, 0, image=final_show, anchor=NW)
    root.update()

    return image1


def draw_another():
    global showImage
    global image
    global m_draw
    image = Image.new("RGB", (cwd, cht), (255, 255, 255))
    m_draw = ImageDraw.Draw(image)
    m_draw.line([0, 0, cwd - 1, 0], (0, 0, 0))
    m_draw.line([cwd - 1, 0, cwd - 1, cht - 1], (0, 0, 0))
    m_draw.line([cwd - 1, cht - 1, 0, cht - 1], (0, 0, 0))
    m_draw.line([0, cht - 1, 0, 0], (0, 0, 0))
    m_draw = ImageDraw.Draw(image)
    showImage = draw()

runAgain["command"] = draw_another


def credit(e):
    open_new("https://github.com/fogleman/Piet#procedurally-generating-images-in-the-style-of-piet-mondrian")
    credits2["fg"] = "purple"
    credits2.update()

c.pack()

credits1 = Label(root, text="Algorithm inspired by GitHub user fogleman", font=("Arial", 9))
credits1.pack()

credits2 = Label(root, text="Click for source/info", font=("Arial", 9, "underline"), fg="blue")
credits2.pack()
credits2.bind("<Button-1>", credit)

credits3 = Label(root, text="By Nico Brubaker, applying for grade 9", font=("Arial", 9))
credits3.pack()

showImage = draw()


def save_the_image():
    global showImage
    showImage.show()

save["command"] = save_the_image

root.mainloop()
