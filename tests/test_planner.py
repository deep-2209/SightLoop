from sightloop.planner import plan

COLORS = {"red", "green", "yellow"}


def fake(resp):
    return lambda prompt: resp


def test_valid_plan_passes():
    resp = ('[{"tool":"pick","args":{"color":"red"}},'
            '{"tool":"place_on","args":{"color":"green"}}]')
    parsed, result = plan("stack red on green", COLORS, fake(resp))
    assert result.valid, result.errors
    assert len(parsed) == 2


def test_unknown_color_is_invalid():
    resp = '[{"tool":"pick","args":{"color":"purple"}}]'
    _, result = plan("pick purple", COLORS, fake(resp))
    assert not result.valid


def test_unparseable_reply_is_invalid():
    _, result = plan("hi", COLORS, fake("sorry, I cannot help"))
    assert not result.valid


def test_bad_direction_is_invalid():
    resp = '[{"tool":"place_relative","args":{"color":"red","direction":"up"}}]'
    _, result = plan("...", COLORS, fake(resp))
    assert not result.valid