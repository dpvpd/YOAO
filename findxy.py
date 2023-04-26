import math
import matplotlib.pyplot as plt

def findPosition(distance, angleDegrees):
    xPosition = distance * math.sin(math.radians(angleDegrees))
    yPosition = distance * math.cos(math.radians(angleDegrees))
    return xPosition, yPosition

def makePlot():
    # 파일 처음부터 끝까지 읽음
    # 파일의 홀수 줄 : x
    # 파일의 짝수 줄 : y
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

if __name__=='__main__':
    makePlot()