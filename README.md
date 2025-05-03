# traffic-sign-recogniton-robot
Robot that detects traffic signs and moves accordingly using camera input, TensorFlow, and ROS 2

# Traffic Sign Recognition Robot

An autonomous robot that detects traffic signs using a camera and responds in real-time using ROS 2 motion control. It recognizes signs such as **Left**, **Right**, **Forward**, and **Stop** using a TensorFlow model trained on traffic symbol images.

## 🎯 Features
- Real-time image classification using a camera
- Sign recognition via TensorFlow and OpenCV
- Motor control logic using ROS 2
- Simulated in Gazebo and deployed on hardware

## 🛠 Technologies Used
- ROS 2 (Humble)
- Python 3
- TensorFlow / Keras
- OpenCV
- Gazebo (simulation)
- Arduino (for physical actuation)

## 🗂 Folder Structure
traffic-sign-recognition-robot/
├── src/ # ROS 2 nodes
├── models/ # Trained model (.h5)
├── launch/ # ROS 2 launch files
├── README.md


## 🚀 How to Run
import git files into pakge folder (database not included as to large)
ensure folder path is same as the trained model path on system (traffic_recognition.h5)

```bash

colcon build
source install/setup.bash

ros2 launch traffic_sign_recognition_package robot_camera_publisher

ros2 launch traffic_sign_recognition_package robot_camera_subscriber
