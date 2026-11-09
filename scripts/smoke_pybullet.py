# scripts/smoke_pybullet.py
import pybullet as p
import pybullet_data

# Start physics with no window (DIRECT). Returns a client id for this connection.
client = p.connect(p.DIRECT)

# Tell PyBullet where its bundled model files (plane, Panda) live.
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Gravity is off by default, so set it. Units are m/s^2, z is "up".
p.setGravity(0, 0, -9.81)

# Load the floor, then the arm. useFixedBase pins the arm's base in place.
plane_id = p.loadURDF("plane.urdf")
robot_id = p.loadURDF("franka_panda/panda.urdf", useFixedBase=True)

# Count joints. Includes fixed ones, not just the arm's movable joints.
num_joints = p.getNumJoints(robot_id)
print(f"Loaded plane={plane_id}, robot={robot_id}, joints={num_joints}")

pos, orn = p.getBasePositionAndOrientation(robot_id)
print("Base position before 240 steps:", pos)

# Time only moves when we step it. One step is 1/240 s by default.
for _ in range(240):
    p.stepSimulation()

# Where is the arm's base after 1 simulated second? Should not have moved.
pos, orn = p.getBasePositionAndOrientation(robot_id)
print("Base position after 240 steps:", pos)

p.disconnect()