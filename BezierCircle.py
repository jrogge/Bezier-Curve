#!/usr/bin/python
from Tkinter import *
from math import *

numberOfPoints = int(raw_input("how many points do you want to draw?\n:"))
colorsList = {0:'orange', 1:'yellow', 2:'green', 3:'blue', 4:'purple', 5:'red'}
numColors = len(colorsList)

# dimensions of window
width = 1300
height = 700

points = {0:[], 'draw':[]}
# Dictionary of lists containing all points
# Each value is a 2D list, so calling points follows the format
#    points[degree][point number][x or y]
#       degree - cubic Beziers have 2 degrees, etc
#       point number is the point, points being ordered chronologically
#       0 for x, 1 for y
# The 'draw' entry will contain a 2D list of two sublists, ocntaining
#    the two points that will actually be used to draw

radius = 3 # radius of circles around points
buttonSize = minHeight = 40 # size of buttons

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def evenlySpacedPoints(num, skip):
    for i in xrange(num):
        rad = skip * (i * (2 * pi) / num)
        pointX = 650 + 250 * cos(rad)
        pointY = 350 + 250 * sin(rad)
        point = Point(pointX, pointY)
        handleClick(point)

def intToHexColor(num):
    hexValue = hex(num)[2:]
    if len(hexValue) < 6:
        hexValue = (6 - len(hexValue)) * '0' + hexValue
    return '#' + hexValue
        
def drawButtons(numPoints):
    for button in xrange(numPoints - 2):
        if button >= numColors:
            buttonValue = button - numColors * (button / numColors)
            # appears redundant but integer division truncates
        else:
            buttonValue = button
        canvas.create_rectangle(
                button * buttonSize, 0,
                (button + 1) * buttonSize, buttonSize,
                fill = colorsList[buttonValue]
                )

def quadBezier(point1, point2, point3, percent):
    '''Any degree bezier curve is simply nested quadratic bezier curves.
    This function takes four parameters:
       -Three lists/tuples of floats, representing the three points
            the points should follow the form [x,y]
       -One float, representing the percent across the resultant line
    Returns the endpoints of the appropriate line'''
    x1 = point1[0] + percent * (point2[0]-point1[0])
    y1 = point1[1] + percent * (point2[1]-point1[1])
    x2 = point2[0] + percent * (point3[0]-point2[0])
    y2 = point2[1] + percent * (point3[1]-point2[1])
    return ((x1,y1),(x2,y2))
 
def drawCurve (pointsList, drawLevel): 
    '''Does the drawing of the actual curve and degree handling'''
    degree = len(pointsList[0])-2
    numLines = 1000
    for i in xrange(degree - drawLevel):
        pointsList['draw'][2 * i] = pointsList[0][i]
    # following iterations only append one point, making appending the starting
    # point here necessary

    # Loop iterates throgh drawing the lines and/or points making up the curve
    for curvePoint in xrange(1,numLines+1):
        percent = float(curvePoint)/numLines
        for subLevel in xrange(degree):
            numQuads = len(pointsList[subLevel]) - 2
            # number of quadratic subcurves (3 consecutive points)
            pointsList[subLevel+1] = []
            for iteration in xrange(numQuads):
                tempLine = quadBezier(
                    pointsList[subLevel][iteration],
                    pointsList[subLevel][iteration+1],
                    pointsList[subLevel][iteration+2],
                    percent
                    )
                
                if iteration == 0: # removes duplicate writing of points
                    pointsList[subLevel+1].append((
                        tempLine[0][0],
                        tempLine[0][1]
                        ))
                pointsList[subLevel+1].append((
                    tempLine[1][0],
                    tempLine[1][1]
                    ))
                if subLevel == drawLevel: # only draw for the selected level 

                    pointsList['draw'][2 * iteration + 1] = [
                    tempLine[0][0] + percent * (tempLine[1][0]-tempLine[0][0]),
                    tempLine[0][1] + percent * (tempLine[1][1]-tempLine[0][1])
                    ] # calculate the point of interest, i.e. current percent 
                    if drawLevel >= numColors:
                        colorFill = drawLevel - (
                                numColors * (drawLevel / numColors))
                        # integer division truncates
                    else:
                        colorFill = drawLevel
                    canvas.create_line(
                        pointsList['draw'][2 * iteration][0],
                        pointsList['draw'][2 * iteration][1],
                        pointsList['draw'][2 * iteration + 1][0],
                        pointsList['draw'][2 * iteration + 1][1],
                        fill = colorsList[colorFill]
                        )
                    pointsList['draw'][2 * iteration] = pointsList['draw'][
                            2 * iteration + 1]

def handleClick(event):
    '''interprets a click as creating a point or clicking on a button'''
    if event.y <= buttonSize:
        if event.x >= width - buttonSize: 
            # Black button click
            if points == {0:[], 'draw':['','']}: # second black button click
                canvas.delete("all")
                canvas.create_rectangle(width - buttonSize, 0, width,
                        buttonSize, fill="black") 
                canvas.create_oval(400, 100, 900, 600)
                for i in xrange(2):
                    evenlySpacedPoints(numberOfPoints, 2) 
                handleClick(Point(900,350))
            else:# first black button click
                points.clear()
                points[0] = []
                points['draw'] = ['','']

        elif event.x/buttonSize <= len(points[0]) - 3:
            drawLevel = event.x/buttonSize  
            numQuads = len(points[0]) - (2 + drawLevel)
            for i in xrange(2 * numQuads-len(points['draw'])):
                points['draw'].append(['',''])
            drawCurve(points, drawLevel)
    else: # click anywhere in the canvas, creating a point
        canvas.create_oval(event.x-radius, event.y-radius,
                           event.x+radius, event.y+radius)
        points[0].append([float(event.x),float(event.y)])
        drawButtons(len(points[0]))
 
if __name__ == "__main__":
    # Tkinter handling below
    root = Tk()
    window = Frame(root, width=width, height=height)
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    x = (screenwidth - width)/2
    y = (screenheight - height)/2
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    window.pack()
    canvas = Canvas(window, height=width, width=width) 
    canvas.create_rectangle(
            width - buttonSize, 0,
            width, buttonSize,
            fill="black"
            )
    canvas.create_oval(400, 100, 900, 600)
    for i in xrange(2):
        evenlySpacedPoints(numberOfPoints, 2) 
    handleClick(Point(900,350))
    canvas.bind("<Button-1>", handleClick)
    canvas.pack()

    root.call('wm', 'attributes', '.', '-topmost', True)
    root.mainloop()
