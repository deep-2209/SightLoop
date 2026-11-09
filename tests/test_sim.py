import numpy as np
import pybullet as p

from sightloop.sim import IMG_H, IMG_W, MIN_BLOCK_SPACING, Simulator

COLORS3 = ["red", "green", "yellow"]


def block_positions(sim):
    """World xy position of each block, by color name."""
    out = {}
    for name, body_id in sim.blocks.items():
        pos, _ = p.getBasePositionAndOrientation(body_id, physicsClientId=sim.client)
        out[name] = np.array(pos[:2])
    return out


def test_same_seed_gives_same_layout():
    with Simulator() as a, Simulator() as b:
        a.spawn_blocks(COLORS3, seed=7)
        b.spawn_blocks(COLORS3, seed=7)
        pa, pb = block_positions(a), block_positions(b)
        for name in COLORS3:
            # tolerance, not exact equality: physics settling is float math
            assert np.allclose(pa[name], pb[name], atol=1e-4)


def test_different_seed_gives_different_layout():
    with Simulator() as a, Simulator() as b:
        a.spawn_blocks(COLORS3, seed=1)
        b.spawn_blocks(COLORS3, seed=2)
        pa, pb = block_positions(a), block_positions(b)
        assert not np.allclose(pa["red"], pb["red"], atol=1e-3)


def test_blocks_do_not_overlap():
    with Simulator() as sim:
        sim.spawn_blocks(COLORS3, seed=3)
        pos = list(block_positions(sim).values())
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                # small slack: blocks may shift a little while settling
                assert np.linalg.norm(pos[i] - pos[j]) >= MIN_BLOCK_SPACING - 0.01


def test_reset_clears_blocks():
    with Simulator() as sim:
        sim.spawn_blocks(COLORS3, seed=0)
        assert len(sim.blocks) == 3
        sim.reset()
        assert sim.blocks == {}


def test_simulators_are_isolated():
    with Simulator() as a, Simulator() as b:
        a.spawn_blocks(COLORS3, seed=0)
        assert a.client != b.client
        assert b.blocks == {}


def test_capture_shapes_and_cleanup():
    sim = Simulator()
    sim.spawn_blocks(["red"], seed=0)
    rgb, depth = sim.capture_rgbd()
    assert rgb.shape == (IMG_H, IMG_W, 3) and rgb.dtype == np.uint8
    assert depth.shape == (IMG_H, IMG_W)
    sim.close()
    assert not p.isConnected(physicsClientId=sim.client)