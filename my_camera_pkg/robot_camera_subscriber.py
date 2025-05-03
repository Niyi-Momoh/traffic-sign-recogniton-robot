import rclpy
from rclpy.node import Node
import serial

class RobotCommandNode(Node):
    def __init__(self):
        super().__init__('robot_command_node')
        try:
            # Initialize the serial connection
            self.serial_port = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            self.get_logger().info('Robot Command Node has started. Type R for Right, L for Left, F for Forward, S for Stop.')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to connect to Arduino: {e}')
            raise

    def send_command(self, command):
        try:
            if command in ['R', 'L', 'F', 'S']:
                self.serial_port.write(command.encode())  # Send the command as a byte
                self.get_logger().info(f"Command '{command}' sent to Arduino")
            else:
                self.get_logger().warning('Invalid command. Use R (Right), L (Left), F (Forward), S (Stop).')
        except Exception as e:
            self.get_logger().error(f'Failed to send command: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = RobotCommandNode()

    try:
        while rclpy.ok():
            command = input("Enter R (Right), L (Left), F (Forward), or S (Stop): ").strip().upper()
            node.send_command(command)
    except KeyboardInterrupt:
        pass
    finally:
        node.serial_port.close()  # Close the serial port on exit
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
