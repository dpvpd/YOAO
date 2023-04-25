from ultralytics import YOLO
import cv2
import time
import numpy as np
import math

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture('http://192.168.0.77:9000/stream.mjpg')

msg12 = ''

def avg(l):
    if len(l)==0:
        return 0
    return sum(l)/len(l)

def drawRect(src, boxes, scores, classes):
    result = src
    for i in range(len(boxes)):
        x,y,xh,yh = boxes[i]
        x,y,xh,yh = int(x.item()),int(y.item()),int(xh.item()),int(yh.item())
        #print(x,y,xh,yh)
        score = scores[i].item()
        cat = classes[i].item()
        text = 'class {0} : {1}'.format(cat,score)
        #print((x,y),(xh,yh))
        result = cv2.rectangle(result,(x,y),(xh,yh),(0,255,0),1)
        cv2.putText(result,text,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    return result

class YoloDetect:
    def __init__(self):
        self.nowtime = time.time()
        self.prevtime = 0
        self.fpsList = []
        self.cnt = 0
        self.CamAngle = 62.2
        ret, img = cap.read()
        self.ImageHeight, self.ImageWidth, _ = img.shape

    def __call__(self):
        if cap.isOpened():
            ret, img = cap.read()
            #img = np.array(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            prevtime = self.nowtime
            self.nowtime = time.time()
            fps = 1/(self.nowtime-prevtime)
            self.fpsList.append(fps)
            self.cnt+=1
            low1 = avg(sorted(self.fpsList)[:len(self.fpsList)//10])
            high1 = avg(sorted(self.fpsList)[len(self.fpsList)-(len(self.fpsList)//10):])
            #print('FPS : %.2f \nLOW %.2f AVG %.2f HIGH %.2f'%(fps, low1, avg(self.fpsList), high1))
            if self.cnt==1:
                self.fpsList = []

        res = model(img)

        humans = []
        for i in res:
            for j in range(len(i.boxes.cls)):
                if i.boxes.cls.tolist()[j]==0:
                    humans.append(i.boxes.xyxy.tolist()[j])

        result = []
        for i in range(len(humans)):
            x1,y1,x2,y2 = humans[i]
            cx, xy = (x1+x2)//2, (y1+y2)//2
            xAngle = ((cx/self.ImageWidth)-.5)*self.CamAngle
            #print(xAngle)
            result.append(xAngle)

        res_plotted = cv2.cvtColor(res[0].plot(),cv2.COLOR_RGB2BGR)
        cv2.imshow("result", res_plotted)
        return result


        #if cv2.waitKey(1)&0xff==27:
        #    cv2.destroyAllWindows()
    def releaseCapture(self):
        cap.release()
        #cv2.destroyAllWindows()

def findDistance(ranges, angle_min, angle_increment, desired_angle_degrees):
    desired_angle_radians = math.radians(desired_angle_degrees)
    index = int((desired_angle_radians - angle_min) / angle_increment)
    
    distance = 'err'
    if index < len(ranges):
        distance = ranges[index]
    
    #print('\n'*20)
    #print('분해능 : ',len(ranges))
    #print('index : ',index)
    #print('rad : ', desired_angle_radians)
    #print(f'{desired_angle_degrees}도방향 {distance}(m) 떨어져 있음')


if __name__=='__main__':
    asdf = YoloDetect()
    while True:

        humanXposition = asdf()
        print(humanXposition)
        nan = 0
        
        try:
            with open('sharedValue.txt', 'r') as f:
                ranges = eval(f.readline())
                angle_min = eval(f.readline())
                angle_increment = eval(f.readline())

            findDistance(ranges, angle_min, angle_increment, humanXposition[0])
        except:
            pass

        if cv2.waitKey(1)&0xff==27:
            asdf.releaseCapture()

