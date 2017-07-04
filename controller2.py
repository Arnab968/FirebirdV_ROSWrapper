#!/usr/bin/env python
#this is with runga kutta method
#from __future__ import division
import rospy
import rosbag
import numpy as np
from math import *
import serial
import time
import timeit
from sensor_msgs.msg import Joy
from xbee import XBee
global w,v
###user defined functions
#globally used
looprate=5 # 30 hz
#publisher node
#pub1=rospy.Publisher('data_logging_chatter',all_states,queue_size=1)
#handle to bag file
#serial comm
port = serial.Serial("/dev/ttyUSB0", baudrate=57600)
xbee = XBee(port)
#initial states and measurements
beta=1;v=0;rc=13;
w=0;

dest_16bit = 'FFFF'
#rf_data = """!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`"""



#controller initialization
def joy_cb(data):
	global w,v
	v= data.axes[1]*15
	w=data.axes[2]*0.3


def generate_packet(v,w):
    """let send both in 4 bits..can be in 8"""
    v_mag = (round(v,2)*100);
    w_mag = (round(w,3)*1000);
    if v_mag >= 0:
        v_sign = '+'
    if v_mag <= 0:
        v_sign = '-'
        v_mag = v_mag*-1
    if w_mag >= 0:
        w_sign = '+'
    if w_mag <= 0:
        w_sign = '-'
        w_mag = w_mag*-1
    v_net = str(int(v_mag)).zfill(4)
    w_net = str(int(w_mag)).zfill(4)
    final_packet = '#' + v_sign + v_net + w_sign + w_net + '$'
    return final_packet
######send packet
def send_packet(packet):
   xbee.tx(dest_addr='\xFF\xFF', data=packet)
######robot models

##initializations
##ros initializations
###define callback function
###define listener/main node
def bot_driver():
    global w,v
    #initialize node
    rospy.init_node('controller_node',anonymous=True)
    #subscribe to topic
    rospy.Subscriber('joy',Joy,joy_cb)
    #looprate=10#hertz
    rate=rospy.Rate(looprate)
    while not rospy.is_shutdown():
        start=timeit.default_timer()
        send_packet(generate_packet(v,w))
                
        end=timeit.default_timer()
        rate.sleep()
   
#define data logging to bag file function

if __name__ == '__main__':
    try:
        bot_driver()
    except rospy.ROSInterruptException:
        pass
         
       
        
        
    
