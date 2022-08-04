# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 02:15:48 2022

@author: Maxime
"""
from pydub import AudioSegment
from pydub.playback import play
import multiprocessing
import keyboard
import time

def waitForKeyDown(key):
    while not keyboard.is_pressed(key) and not keyboard.is_pressed(exit_key):
        pass
        
def waitForKeyUp(key):
    while keyboard.is_pressed(key) and not keyboard.is_pressed(exit_key):
        pass

def waitForPress(key):
    waitForKeyDown(key)
    waitForKeyUp(key)
        
def timeToAngle(time, bpm):
    return 180*time / (60/bpm)

def recordPressLists(music_name, press_key='e'):
    song = AudioSegment.from_wav(music_name)
    waitForPress(press_key)
    t = multiprocessing.Process(target=play, args=(song,))
    t.start() #music is played in the blackground in a thread
            
    press_list = []
    start_time = time.time()
    while not keyboard.is_pressed(exit_key):
        waitForKeyDown(press_key)
        press_list.append(time.time()-start_time)
        waitForKeyUp(press_key)
            
    t.terminate()
    return press_list

def getAngleList(press_list, bpm, resolution=4):
    angle_list = []
    beat_time = 60/bpm
    used_time = press_list[0]
    for i in range(1, len(press_list)):
        diff = press_list[i] - used_time
        angle = timeToAngle(diff, bpm)
        closest_cat = round(angle/180 * resolution) #round to closest angle possible to map
        closest_angle = closest_cat/resolution * 180 #
        angle_list.append(closest_angle)
        
        used_time += beat_time * closest_cat/resolution 
 
    return angle_list

def buildMap(angle_list):
    #build_keys = ['a', 'q', 'w', 'e', 'd', 'c', 's', 'z']
    build_keys = ['a', 'shift+h', 'q', 'shift+t', 'w', 'shift+y', 'e', 'shift+j', 'd',
                  'shift+m', 'c', 'shift+b', 's', 'shift+v', 'z', 'shift+n']
    current_angle = 0
    for full_angle in angle_list:
        while full_angle > 0:
            if full_angle >= 360: #angles higher than 360 degres are divided into smaller angles
                angle = 180
            else:
                angle = full_angle
                
            angle_correction = angle - 180
            next_angle = (current_angle + angle_correction) % 360
            
            build_key = build_keys[round((next_angle+180) // 22.5) % 16]
            
            keyboard.press_and_release(build_key)
            time.sleep(0.1)
            
            current_angle = next_angle
            full_angle -= angle
    
if __name__ == '__main__':
    music_name = "Rakuen.wav"
    bpm = 196
    resolution = 4
    exit_key = 'q'
    press_key = 'e'
    
    press_list = recordPressLists(music_name, press_key)
    #press_list : [5.129, 5.390, 5.529, 5.898, ...]
    angle_list = getAngleList(press_list, bpm, resolution)
    #angle_list : [135.0, 90.0, 225.0, 180.0, ...]
    time.sleep(6)
    buildMap(angle_list)
    #for the offset (in miliseconds) to put in for map, for me it was the second value of press_list plus 130 ms : press_list[1]*1000 + 130

    

        
    

