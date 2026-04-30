import math

class Mapper:
    """
    Builds a simple occupancy map from ultrasonic sensor sweeps.
    Tracks robot position and converts polar sensor readings
    (angle + distance) into absolute x/y obstacle coordinates.
    """

    def __init__(self):
        self.robot_x = 0.0       # robot position x (cm)
        self.robot_y = 0.0       # robot position y (cm)
        self.robot_heading = 90  # degrees — 90 = facing up (north)
        self.obstacles = []      # list of (x, y) obstacle points
        self.path = [(0.0, 0.0)] # robot's travel path

    def add_sweep(self, readings):
        """
        Process one full servo sweep.
        readings: list of (angle, distance_cm) from sensor.sweep()
        Converts sensor-local polar coords to absolute map coords.
        """
        new_obstacles = []

        for angle, distance in readings:
            if distance is None:
                continue  # skip failed readings

            # angle is relative to robot (90 = straight ahead)
            absolute_angle = math.radians(self.robot_heading + angle - 90)

            obs_x = self.robot_x + distance * math.cos(absolute_angle)
            obs_y = self.robot_y + distance * math.sin(absolute_angle)

            new_obstacles.append((round(obs_x, 1), round(obs_y, 1)))

        self.obstacles.extend(new_obstacles)
        return new_obstacles

    def move(self, direction, distance_cm):
        """
        Update robot position after movement.
        direction: 'forward' | 'backward' | 'left' | 'right'
        distance_cm: how far the robot moved
        """
        angle_rad = math.radians(self.robot_heading)

        if direction == "forward":
            self.robot_x += distance_cm * math.cos(angle_rad)
            self.robot_y += distance_cm * math.sin(angle_rad)
        elif direction == "backward":
            self.robot_x -= distance_cm * math.cos(angle_rad)
            self.robot_y -= distance_cm * math.sin(angle_rad)
        elif direction == "left":
            self.robot_heading = (self.robot_heading + 90) % 360
        elif direction == "right":
            self.robot_heading = (self.robot_heading - 90) % 360

        self.path.append((round(self.robot_x, 1), round(self.robot_y, 1)))

    def get_state(self):
        """Returns full map state as a dict (JSON-serializable)."""
        return {
            "robot": {
                "x": round(self.robot_x, 1),
                "y": round(self.robot_y, 1),
                "heading": self.robot_heading,
            },
            "obstacles": self.obstacles,
            "path": self.path,
        }
