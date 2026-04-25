import asyncio
import time
import RPi.GPIO as GPIO

import motor
import sensor
from mapper import Mapper
from streamer import broadcast, start_server

MOVE_DISTANCE_CM = 20    # how far to move per step
OBSTACLE_THRESHOLD = 25  # cm — stop and turn if closer than this


async def robot_loop(mapper: Mapper):
    """Main robot control loop: scan → decide → move → repeat."""
    print("[main] Starting robot loop...")

    while True:
        # 1. Scan surroundings
        readings = sensor.sweep()
        new_obs = mapper.add_sweep(readings)
        print(f"[main] Sweep done — {len(new_obs)} new obstacle points")

        # 2. Send updated map to laptop
        await broadcast(mapper.get_state())

        # 3. Check front distance (reading at 90 degrees = straight ahead)
        front = next(
            (d for a, d in readings if a == 90 and d is not None), None
        )

        # 4. Decide movement
        if front is None or front > OBSTACLE_THRESHOLD:
            print(f"[main] Path clear ({front} cm) — moving forward")
            motor.forward()
            await asyncio.sleep(0.8)  # move for ~0.8s
            motor.stop()
            mapper.move("forward", MOVE_DISTANCE_CM)
        else:
            print(f"[main] Obstacle at {front} cm — turning right")
            motor.turn_right()
            await asyncio.sleep(0.6)  # turn for ~0.6s
            motor.stop()
            mapper.move("right", 0)

        await asyncio.sleep(0.2)  # brief pause between cycles


async def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    motor.setup()
    sensor.setup()
    mapper = Mapper()

    print("[main] Monstera robot starting up...")

    try:
        # Run WebSocket server + robot loop concurrently
        await asyncio.gather(
            start_server(),
            robot_loop(mapper),
        )
    except KeyboardInterrupt:
        print("\n[main] Shutting down...")
    finally:
        motor.cleanup()
        sensor.cleanup()
        GPIO.cleanup()
        print("[main] GPIO cleaned up. Bye!")


if __name__ == "__main__":
    asyncio.run(main())
