# scripts/camera_test.py
import os
import numpy as np
import pybullet as p
import pybullet_data
from PIL import Image

WIDTH, HEIGHT = 640, 480

p.connect(p.DIRECT)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

p.loadURDF("plane.urdf")
p.loadURDF("franka_panda/panda.urdf", useFixedBase=True)

# One red cube, dropped from just above the floor so it settles.
cube_id = p.loadURDF("cube_small.urdf", basePosition=[0.5, 0.0, 0.05])
p.changeVisualShape(cube_id, -1, rgbaColor=[1, 0, 0, 1])  # -1 = the base link

# letting cube settle
for _ in range(100):
    p.stepSimulation()

# Camera: 0.9 m above the cube, looking straight down.
# Up vector is (1, 0, 0), NOT (0, 0, 1): a down-looking camera with a
# vertical "up" gives a degenerate view matrix.
view = p.computeViewMatrix(
    cameraEyePosition=[0.5, 0.0, 0.9],
    cameraTargetPosition=[0.5, 0.0, 0.0],
    cameraUpVector=[1, 0, 0],
)
proj = p.computeProjectionMatrixFOV(
    fov=60, aspect=WIDTH / HEIGHT, nearVal=0.1, farVal=3.0
)

w, h, rgba, depth, seg = p.getCameraImage(
    WIDTH, HEIGHT, view, proj, renderer=p.ER_TINY_RENDERER
)

# Works whether PyBullet hands back a flat list or an array.
rgba = np.reshape(np.array(rgba, dtype=np.uint8), (h, w, 4))
seg = np.reshape(np.array(seg), (h, w))
print("image shape:", rgba.shape, "| segmentation ids present:", np.unique(seg))

os.makedirs("outputs", exist_ok=True)
Image.fromarray(rgba[:, :, :3]).save("outputs/camera_test.png")
print("saved outputs/camera_test.png")

p.disconnect()