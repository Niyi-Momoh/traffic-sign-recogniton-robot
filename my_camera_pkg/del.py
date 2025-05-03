import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import time

# Initialize serial communication with Arduino
try:
    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Update port if needed
    time.sleep(2)  # Wait for Arduino to initialize
    print("Arduino connected successfully.")
except serial.SerialException as e:
    print(f"Failed to connect to Arduino: {e}")
    arduino = None

class TrafficSignSubscriber(Node):
    """ROS2 Node to subscribe to traffic sign commands and send them to Arduino."""

    def __init__(self):
        super().__init__('traffic_sign_subscriber')
        self.subscription = self.create_subscription(
            String,
            'traffic_sign_command',
            self.listener_callback,
            10
        )
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        """Callback to handle received commands."""
        command = msg.data
        self.get_logger().info(f"Received command: {command}")
        self.send_command_to_arduino(command)

    def send_command_to_arduino(self, command):
        """Send the command to the Arduino via serial."""
        if arduino:
            try:
                arduino.write(command.encode())
                self.get_logger().info(f"Command '{command}' sent to Arduino.")
            except Exception as e:
                self.get_logger().error(f"Failed to send command to Arduino: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = TrafficSignSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Node stopped by user.")
    finally:
        if arduino:
            arduino.close()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
