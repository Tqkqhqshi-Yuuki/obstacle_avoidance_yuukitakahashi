#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import select
import tty
import termios
import random

from cv2 import SUBDIV2D_NEXT_AROUND_RIGHT
from std_srvs.srv import SetBool, SetBoolResponse
from std_srvs.srv import Empty
from geometry_msgs.msg import PoseWithCovarianceStamped
from std_msgs.msg import Int8MultiArray
from nav_msgs.msg import Path
from std_srvs.srv import Trigger
from std_msgs.msg import Int8
from geometry_msgs.msg import PoseArray
from geometry_msgs.msg import Twist
from skimage.transform import resize
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import rospy
import roslib


msg = """
Control path direction!
--------------------------
        w
    a   s   d
        x

w : Moving start
a : Input left direction [0 100 0]
s : Moving stop
d : Input right direction [0 0 100]
x : exit
"""

err = """
Communications Failed
"""


def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def outdata(data):
    data = "Input_data : " + str(data.data)
    return data


if __name__ == "__main__":
    settings = termios.tcgetattr(sys.stdin)
    rospy.init_node('save')
    f_pub = rospy.Publisher('save_flag', Int8, queue_size=1)

    flag = 0

    try:
        print(msg)
        while(1):
            key = getKey()
            if key == 's':
                flag = 1
            elif key == 'q':
                break
            else:
                flag = 0
            f_pub.publish(flag)
            flag = 0
    except:
        print(err)

    finally:
        print(err)