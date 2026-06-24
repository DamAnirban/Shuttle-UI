# Shuttle-UI

A lightweight operator console for dispatching navigation goals to autonomous mobile robots (AMRs) over a local network. Built with Python, Tkinter, and ROS.

---

## Overview

Shuttle-UI splits into two sides:

| Side | Runs on | Description |
|---|---|---|
| **Master** | Operator's laptop / PC | Tkinter GUI to select a robot and a route, then step through waypoints one by one |
| **Robot** | Robot's onboard computer | ROS node that receives each waypoint over UDP and forwards it to the `move_base` action server |

Communication uses a simple UDP + pickle protocol — no middleware required on the operator side.

```
Operator PC                          Robot (ROS)
┌─────────────────┐   UDP/pickle    ┌──────────────────────┐
│  master/gui.py  │ ─────────────▶ │  robot/nav_node.py   │
│                 │  [x, y, yaw]   │                      │
│  Select cart    │                 │  move_base client    │
│  Select route   │                 │  (autonomous nav)    │
│  NEXT_GOAL btn  │                 └──────────────────────┘
└─────────────────┘
```

---

## Directory Structure

```
Shuttle-UI/
├── master/
│   └── gui.py            # Operator GUI (Tkinter)
├── robot/
│   ├── nav_node.py       # ROS navigation node (runs on robot)
│   └── udp_receiver.py   # Standalone UDP listener for testing
├── requirements.txt
└── README.md
```

---

## Prerequisites

**Operator PC (master)**
- Python 3
- `tkinter` (bundled with most Python 3 installs; on Ubuntu: `sudo apt install python3-tk`)

**Robot (ROS side)**
- ROS Melodic or Noetic
- `move_base` action server configured and running
- Packages: `rospy`, `actionlib`, `tf`, `move_base_msgs`, `geometry_msgs`

---

## Configuration

Before running, set the robot's IP address in both files:

`master/gui.py` — line 15, set the target robot IP(s):
```python
carts = ["192.168.x.x", "192.168.x.x", "192.168.x.x"]
```

`robot/nav_node.py` — line 8, set the interface the robot should listen on:
```python
HOST = "192.168.x.x"
PORT = 2055
```

---

## Usage

**1. Start the ROS navigation stack on the robot:**
```bash
roslaunch <your_robot_pkg> navigation.launch
```

**2. Start the nav node on the robot:**
```bash
python3 robot/nav_node.py
```

**3. Launch the operator GUI on the PC:**
```bash
python3 master/gui.py
```

**4. In the GUI:**
- Select the target **cart** (CART1 / CART2 / CART3)
- Select the **route** (ROUTE1 / ROUTE2 / ROUTE3)
- Press **START** to initialise
- Press **NEXT_GOAL** to send the next waypoint in the sequence
- Press **SKIP_GOAL** to skip a waypoint
- Press **STOP** to halt

---

## Testing Without ROS

To verify the master GUI is sending packets correctly, run the standalone receiver on any machine:
```bash
python3 robot/udp_receiver.py
```
It will print each received waypoint to stdout without requiring a ROS installation.

---

## How It Works

Each waypoint is serialized with `pickle` and sent as a 3-element list `[x, y, yaw_degrees]` over UDP. On the robot, `nav_node.py` converts the yaw angle to a quaternion using `tf.transformations` and dispatches the goal to `move_base`, which handles the actual path planning and motor control.
