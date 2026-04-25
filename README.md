# Monstera

A Raspberry Pi robot car that drives autonomously and streams a live map to your laptop over WiFi.

## How it works

```
Raspberry Pi                     MacBook
-----------                      -------
main.py                          dashboard/app.py
  ├── motor.py   (L298N)            └── templates/index.html
  ├── sensor.py  (HC-SR04 + servo)      └── live map canvas
  ├── mapper.py  (builds map)
  └── streamer.py ──── WebSocket ────► browser
```

## Setup

### On your Mac (dashboard)

```bash
cd ~/Projects/monstera
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env — set PI_IP to your Pi's IP address
python dashboard/app.py
# open http://localhost:5000
```

### On the Raspberry Pi (robot)

```bash
git clone <your-repo> monstera
cd monstera/robot
pip install -r ../requirements-pi.txt
cp ../.env.example ../.env
# edit .env — set PI_PORT if needed
python main.py
```

## Pin wiring

### L298N motor driver

| L298N | Pi GPIO (BCM) |
| ----- | ------------- |
| IN1   | 17            |
| IN2   | 18            |
| IN3   | 22            |
| IN4   | 23            |
| ENA   | 24            |
| ENB   | 25            |

### HC-SR04 ultrasonic sensor

| HC-SR04 | Pi GPIO (BCM) |
| ------- | ------------- |
| TRIG    | 5             |
| ECHO    | 6             |
| VCC     | 5V            |
| GND     | GND           |

### Servo motor

| Servo  | Pi GPIO (BCM) |
| ------ | ------------- |
| Signal | 13            |
| VCC    | 5V            |
| GND    | GND           |

## Tuning

- `MOVE_DISTANCE_CM` in `main.py` — adjust based on actual movement per step
- `OBSTACLE_THRESHOLD` in `main.py` — how close before turning (default 25cm)
- `SPEED` in `motor.py` — motor speed 0–100
- Servo sweep step in `sensor.py` — currently every 15 degrees
