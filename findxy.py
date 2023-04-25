import math
import matplotlib.pyplot as plt

def findPosition(distance, angleDegrees):
    xPosition = distance * math.sin(math.radians(angleDegrees))
    yPosition = distance * math.cos(math.radians(angleDegrees))
    return xPosition, yPosition

#파일 처음부터 끝까지 읽음
with open('xyValue.txt', 'r') as f:
    plt.scatter(0,0)
    while True:
        x = f.readline()
        y = f.readline()
        if not x or not y:
            break
        x = eval(x)
        y = eval(y)
        plt.scatter(x, y)

plt.show()