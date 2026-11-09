# scripts/joint_table.py
import pybullet as p
import pybullet_data

# Joint type codes from the PyBullet docs.
JOINT_TYPES = {0: "REVOLUTE", 1: "PRISMATIC", 2: "SPHERICAL", 3: "PLANAR", 4: "FIXED"}

p.connect(p.DIRECT)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
robot_id = p.loadURDF("franka_panda/panda.urdf", useFixedBase=True)

print(f"{'idx':>3}  {'joint name':<22} {'type':<10} {'lower':>7} {'upper':>7}  child link")
for i in range(p.getNumJoints(robot_id)):
    info = p.getJointInfo(robot_id, i)
    idx = info[0]
    name = info[1].decode("utf-8")      # PyBullet returns names as bytes
    jtype = JOINT_TYPES[info[2]]
    lower, upper = info[8], info[9]     # joint limits
    link = info[12].decode("utf-8")     # the link this joint moves
    print(f"{idx:>3}  {name:<22} {jtype:<10} {lower:>7.2f} {upper:>7.2f}  {link}")

p.disconnect()