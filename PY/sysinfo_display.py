#!/usr/bin/env python
import os
import time
import socket
import fcntl
import struct
import requests
import math
import datetime
import sys
import logging
#from demo_opts import get_device
from luma.core.render import canvas
from luma.core import cmdline, error
#setdisplay
def display_settings(args):

    iface = ''
    display_types = cmdline.get_display_types()
    if args.display not in display_types['emulator']:
        iface = 'Interface: {}\n'.format(args.interface)

    lib_name = cmdline.get_library_for_display_type(args.display)
    if lib_name is not None:
        lib_version = cmdline.get_library_version(lib_name)
    else:
        lib_name = lib_version = 'unknown'

    import luma.core
    version = 'luma.{} {} (luma.core {})'.format(
        lib_name, lib_version, luma.core.__version__)

    return 'Version: {}\nDisplay: {}\n{}Dimensions: {} x {}\n{}'.format(
        version, args.display, iface, args.width, args.height, '-' * 60)

#device
def get_device(actual_args=None):

    if actual_args is None:
        actual_args = sys.argv[1:]
    parser = cmdline.create_parser(description='luma.examples arguments')
    args = parser.parse_args(actual_args)

    if args.config:
        # load config from file
        config = cmdline.load_config(args.config)
        args = parser.parse_args(config + actual_args)

    print(display_settings(args))

    # create device
    try:
        device = cmdline.create_device(args)
    except error.Error as e:
        parser.error(e)

    return device

#get sys info
def diskinfo():
	st = os.statvfs('/')
	total = float(st.f_blocks * st.f_frsize)
	used = float(st.f_blocks - st.f_bfree) * st.f_frsize
	return format(used/total, '.1%')
def cpuinfo():
	with open('/proc/stat') as f:
		info = f.readline().split()
		t0 = float(info[1]) + float(info[2]) + float(info[3])
		s0 = t0 + float(info[4]) + float(info[5]) + float(info[6]) + float(info[7])
	time.sleep(0.033)
	with open('/proc/stat') as f:
		info = f.readline().split()
		t1 = float(info[1]) + float(info[2]) + float(info[3])
		s1 = t1 + float(info[4]) + float(info[5]) + float(info[6]) + float(info[7])
	return format((t1-t0)/(s1-s0), '.1%')
def raminfo():
	with open('/proc/meminfo') as f:
		total = float(f.readline().split()[1])
		free = float(f.readline().split()[1])
	return format((total-free)/total, '.1%')
def cputemp():
	with open('/sys/class/thermal/thermal_zone0/temp') as f:
		temp = float(f.readline())
	return format(temp/1000, '.1f')
def wifiinfo():
    with open('/proc/net/wireless') as f:
        f.readline()
        f.readline()
        info = f.readline().split()
    return info[3][:-1]

#line
def lineram():
	with open('/proc/meminfo') as f:
		total = float(f.readline().split()[1])
		free = float(f.readline().split()[1])
	return int((total-free)/total * 62 + 68)
def linedisk():
	st = os.statvfs('/')
	total = float(st.f_blocks * st.f_frsize)
	used = float(st.f_blocks - st.f_bfree) * st.f_frsize
	return int(used/total * 62 + 3)
def cpuline():
	with open('/proc/stat') as f:
		info = f.readline().split()
		t0 = float(info[1]) + float(info[2]) + float(info[3])
		s0 = t0 + float(info[4]) + float(info[5]) + float(info[6]) + float(info[7])
	time.sleep(0.066)
	with open('/proc/stat') as f:
		info = f.readline().split()
		t1 = float(info[1]) + float(info[2]) + float(info[3])
		s1 = t1 + float(info[4]) + float(info[5]) + float(info[6]) + float(info[7])
	return int((t1-t0)/(s1-s0) * 126 + 3)




#timeanddisplay
def main():
    today_last_time = "Unknown"
    while True:
        now = datetime.datetime.now()
        today_date = now.strftime("%d %b %y")
        today_time = now.strftime("%H:%M:%S")
        if today_time != today_last_time:
			today_last_time = today_time
			with canvas(device) as draw:
				draw.text((1, 1), today_date, fill="yellow")
				draw.text((70, 1), today_time, fill="yellow")
				draw.text((2, 14),'Disk:' + diskinfo() + ' RAM:' + raminfo(), fill="yellow")
				draw.rectangle((1,26,62,30), outline="yellow", fill="black")
				draw.rectangle((64,26,126,30), outline="yellow", fill="black")
				draw.line((3,28,linedisk(),28), fill="yellow")
				draw.line((66,28,lineram(),28), fill="yellow")
				draw.text((2, 32),'Temp:' + cputemp() + 'c CPU:' + cpuinfo(), fill="yellow")
#				draw.text((2, 34),'signal:' + 'null' + 'dBm', fill="yellow")
				draw.rectangle((1,44,126,48), outline="yellow", fill="black")
				draw.line((3,46,cpuline(),46), fill="yellow")
	time.sleep(0.1)

if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass

