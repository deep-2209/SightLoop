from sightloop.control import set_gripper
from sightloop.sim import Simulator

with Simulator() as sim:
    print("close:", set_gripper(sim, 0.0))
    print("open: ", set_gripper(sim, 0.04))
    print("over: ", set_gripper(sim, 1.0))   # impossible request