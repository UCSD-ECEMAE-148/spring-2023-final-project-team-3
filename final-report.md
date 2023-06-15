# Team 3 - The Autonomous Amigos - Human Following Robot with Obstacle Avoidance
## UCSD JSOE - ECE/MAE 148 - SP23 - Team 3
### Team:
* ECE: Sialoi Taa
* MAE: Daniel Ruiz, Ryan Evans, Hanyang Feng

## Project Objective
The project goal is for the vehicle to find a human target, then follow them until it gets within a certain distance. Then, when given a hand signal, the robot will open a hatch containing the user's meal. The robot will also avoid any obstacles in its path while navigating toward the person. This project is for an autonomous vehicle controller by a VESC. The idea was motivated by the autonomous robots employed by food delivery companies like DoorDash and Uber Eats. 
### Must Have:
* Object avoidance
* Human detection
* hand proximity for locked box
### Nice to Have:
* PID controller for steering/throttle
* Follow a particular human with visual identifier
* customizable hand gestures for locked box

## Dependencies:
* OpenCV
* DepthAI
* Pathlib
* Numpy
* Math
* Sys
* MatPlotLib
* Time

## Running the Program
Navigate to this [sub-directory](https://github.com/UCSD-ECEMAE-148/spring-2023-final-project-team-3/tree/main/depthai-python/examples/Yolo) and run main.py to start the program.

## Object Detection - "obs_avoid_2.py"
The object detection script is accomplished using DepthAI on an OAK-D Lite. When an object comes into view, the robot will turn away from it depending on which region of the camera's view the object occupies. The camera FOV is divided into 5 "buckets"; objects towards the edge of the FOV (outer buckets) will make the bot turn less and objects towards the middle of the FOV (inner buckets) will make the bot turn more. The robot is instructed to stop when an object comes within ~2 feet of the camera.
![image](https://github.com/UCSD-ECEMAE-148/spring-2023-final-project-team-3/assets/15269806/189d5475-183b-4c0f-bd0d-2c076e6d43dc)
![image](https://github.com/UCSD-ECEMAE-148/spring-2023-final-project-team-3/assets/15269806/f32fb4be-09ff-4ea5-ba47-bbf48851dea6)


## Human Following
The human following script is accomplished using DepthAI Yolo on an OAK-D Lite. The function "displayframe" creates a bounding box around a human and determines its vertical centerline in horizontal pixels. The coordinate is normalized with the function "frameNorm" by dividing the coordinate by the horizontal image resolution - call this "x". The VESC steering value is calculated according to the following formula:
<p align="center">
$steering = G(x-0.5) + 0.5$
</p>

where G is the gain [0 1] that defines the steering range. For example for G=0.5, the value used, the output steering range is [0.25 0.75]. 

The width of the boundary box is used as a reference for human distance from the bot - call this "w". The VESC throttle value is calculated according to the following equation:
<p align="center">
$throttle = S*e^{-T(w-1)} - U$
</p>

where S, T, and U are experimentally determined scalars. S=0.08, T=1.2, and U=0.04 are used.

## Hand Gesture-Locked Box
This component is controlled by a separate microcontroller: an Arduino. The script uses DepthAI to recognize a particular hand gesture. Upon recognizing the user's close hand proximity, a servo motor is activated to open the box. The user may then retrieve their prize.

## Future wants - if given more time
* higher H-FOV camera: cam loses sight of human easily
* algorithm to direct robot towards direction where human was last seen
* more robust human detection software - bounding box flickers
* way to detach obstacle avoidance from human detection (maybe with lidar): obstacles are closer to the ground - humans are higher up, can't have the camera point at both

## Contributions
* Daniel Ruiz - object avoidance
* Sialoi Taa - human detection
* Hanyang Feng - hand gesture-locked box
* Ryan Evans - script integration + documentation
