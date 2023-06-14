## Team 3 - The Autonomous Amigos - Human Following Robot with Obstacle Avoidance

### Project Objective
The project goal is for the vehicle to find a human target, then follow them until it gets within a certain distance. Then, when given a hand signal, the robot will open a hatch containing the user's meal. The robot will also avoid any obstacles in its path while navigating toward the person. This project is for an autonomous vehicle controller by a VESC. The idea was motivated by the autonomous robots employed by food delivery companies like DoorDash and Uber Eats. 

### Object Detection
The object detection script is accomplished using DepthAI on an OAK-D Lite. When an object comes into view, the robot will turn away from it depending on which region of the camera's view the object occupies. The camera FOV is divided into 5 "buckets"; objects towards the edge of the FOV (outer buckets) will make the bot turn less and objects towards the middle of the FOV (inner buckets) will make the bot turn more. When an object comes within ___ feet of the camera, the robot is instructed to stop.

### Human Following
The human following script is accomplished using DepthAI Yolo on an OAK-D Lite. This code creates a bounding box around a human and determines its vertical centerline in horizontal pixels. The coordinate is normalized by dividing the coordinate by the horizontal image resolution - call this "x". The VESC steering value is calculated according to the following formula:
<p align="center">
$steering = G(x-0.5) + 0.5$
</p>

where G is the gain [0 1] that defines steering range. For example if G = 0.5, the output steering range is [0.25 0.75].

