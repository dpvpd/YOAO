from sensor_msgs.msg import LaserScan
import rclpy
import math

def chatter_callback(msg, desired_angle_degrees):

    ranges = msg.ranges

    angle_min = msg.angle_min
    angle_increment = msg.angle_increment
    intensities = msg.intensities

    desired_angle_radians = math.radians(desired_angle_degrees)
    
    index = int((desired_angle_radians - angle_min) / angle_increment)
    
    distance = 'err'
    if index < len(ranges):
        distance = ranges[index]
        #distance += ranges[index]
        #distance += ranges[index]
    
    print('\n'*20)
    print('ranges len : ',len(ranges))
    print('index : ',index)
    print('rad : ', desired_angle_radians)
    print(f'{desired_angle_degrees}도방향 {distance}(m) 떨어져 있음')

    with open("getLidar2andSave.txt", "a") as f:
        f.write("%s\n" % distance)

def startSubscribe(desired_angle_degrees):
    rclpy.init()
    node = rclpy.create_node('scan_listener')
    sub = node.create_subscription(LaserScan,'scan',lambda msg: chatter_callback(msg, desired_angle_degrees), qos_profile=rclpy.qos.qos_profile_sensor_data)

    try:
        count = 0
        while(count < 100):
            rclpy.spin_once(node)
            count += 1

    except KeyboardInterrupt:
        print()

    finally:
        node.destroy_node()
        rclpy.shutdown()

# 와플 기준 (카메라가 보는곳이 정면)
# 0 도 정면
# 90 도 왼쪽
# 180 도 후방
# 270 도 오른쪽
if __name__ == "__main__":
    print('Starting scan listener')
    startSubscribe(0)
    print('exit')        
