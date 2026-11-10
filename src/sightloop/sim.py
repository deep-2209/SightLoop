"""Simulator: owns one PyBullet connection, the world, blocks, and the camera."""
import numpy as np
import pybullet as p
import pybullet_data
from sightloop.kinematics import set_home_pose

TIME_STEP = 1.0 / 240.0

# Block colors (RGBA). No blue: the floor is blue/white, so a blue block would
# confound perception for reasons unrelated to what we want to measure.
COLORS = {
    "red": [1.0, 0.0, 0.0, 1.0],
    "green": [0.0, 0.8, 0.0, 1.0],
    "yellow": [1.0, 0.9, 0.0, 1.0],
    "orange": [1.0, 0.5, 0.0, 1.0],
}

# Where blocks may appear (meters; robot base at the origin).
WORKSPACE_X = (0.40, 0.70)
WORKSPACE_Y = (-0.25, 0.25)
MIN_BLOCK_SPACING = 0.10  # center-to-center; blocks are about 0.05 wide

# Fixed top-down camera.
IMG_W, IMG_H = 640, 480
CAM_EYE = [0.55, 0.0, 0.9]
CAM_TARGET = [0.55, 0.0, 0.0]
CAM_UP = [1, 0, 0]  # not vertical: a down-looking camera needs a sideways up
CAM_FOV, CAM_NEAR, CAM_FAR = 60, 0.1, 3.0


class Simulator:
    def __init__(self, gui: bool = False) -> None:
        mode = p.GUI if gui else p.DIRECT
        self.client = p.connect(mode)
        self.plane_id: int | None = None
        self.robot_id: int | None = None
        self.blocks: dict[str, int] = {}  # color name -> body id
        self.reset()

    def reset(self) -> None:
        """Rebuild the same empty world: floor + fixed-base Panda, no blocks."""
        c = self.client
        p.resetSimulation(physicsClientId=c)
        p.setAdditionalSearchPath(pybullet_data.getDataPath(), physicsClientId=c)
        p.setGravity(0, 0, -9.81, physicsClientId=c)
        p.setTimeStep(TIME_STEP, physicsClientId=c)
        self.plane_id = p.loadURDF("plane.urdf", physicsClientId=c)
        self.robot_id = p.loadURDF(
            "franka_panda/panda.urdf", useFixedBase=True, physicsClientId=c
        )
        self.blocks = {}  # resetSimulation deleted every object; forget the ids
        set_home_pose(self) # every episode starts from the same arm pose

    def step(self, n: int = 1) -> None:
        for _ in range(n):
            p.stepSimulation(physicsClientId=self.client)

    # ---- scene -----------------------------------------------------------

    def spawn_blocks(self, colors: list[str], seed: int) -> dict[str, int]:
        """Scatter one block per color name at seeded, non-overlapping spots."""
        rng = np.random.default_rng(seed)
        placed: list[np.ndarray] = []
        for name in colors:
            for _ in range(1000):
                xy = np.array(
                    [rng.uniform(*WORKSPACE_X), rng.uniform(*WORKSPACE_Y)]
                )
                if all(np.linalg.norm(xy - q) >= MIN_BLOCK_SPACING for q in placed):
                    break
            else:  # the loop never hit `break`: no valid spot found
                raise RuntimeError(f"could not place block '{name}'")
            placed.append(xy)
            self.blocks[name] = self._add_block(name, xy)
        self.step(120)  # let the blocks settle onto the floor
        return dict(self.blocks)

    def _add_block(self, color_name: str, xy: np.ndarray) -> int:
        body_id = p.loadURDF(
            "cube_small.urdf",
            basePosition=[float(xy[0]), float(xy[1]), 0.03],
            physicsClientId=self.client,
        )
        p.changeVisualShape(
            body_id, -1, rgbaColor=COLORS[color_name], physicsClientId=self.client
        )
        return body_id

    # ---- camera ----------------------------------------------------------

    def _render(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        c = self.client
        # view = p.computeViewMatrix(CAM_EYE, CAM_TARGET, CAM_UP, physicsClientId=c)
        # proj = p.computeProjectionMatrixFOV(
        #     CAM_FOV, IMG_W / IMG_H, CAM_NEAR, CAM_FAR, physicsClientId=c
        # )
        view, proj = self.camera_matrices()
        w, h, rgba, depth, seg = p.getCameraImage(
            IMG_W, IMG_H, view, proj, renderer=p.ER_TINY_RENDERER, physicsClientId=c
        )
        rgba = np.reshape(np.array(rgba, dtype=np.uint8), (h, w, 4))
        return (
            rgba[:, :, :3],
            np.reshape(np.array(depth), (h, w)),
            np.reshape(np.array(seg), (h, w)),
        )

    def capture_rgbd(self) -> tuple[np.ndarray, np.ndarray]:
        """What the AGENT may see: color image and raw depth buffer."""
        rgb, depth, _ = self._render()
        return rgb, depth

    def ground_truth_mask(self) -> np.ndarray:
        """EVALUATION ONLY. Per-pixel body ids from the simulator. The agent's
        perception must never read this, or the perception metric is meaningless."""
        _, _, seg = self._render()
        return seg

    def camera_matrices(self):
        c = self.client
        view = p.computeViewMatrix(CAM_EYE, CAM_TARGET, CAM_UP, physicsClientId=c)
        proj = p.computeProjectionMatrixFOV(
            CAM_FOV, IMG_W / IMG_H, CAM_NEAR, CAM_FAR, physicsClientId=c
        )
        return view, proj

    # ---- lifecycle -------------------------------------------------------

    def close(self) -> None:
        if p.isConnected(physicsClientId=self.client):
            p.disconnect(physicsClientId=self.client)

    def __enter__(self) -> "Simulator":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()