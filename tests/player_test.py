from core.player import Player


def test_player_create() -> None:
    p = Player((1, 1), 2.0)

    assert p._start == (1, 1)
    assert p.tile == (1, 1)
    assert p.direction is None
    assert p.speed == 2.0


def test_player_reset() -> None:
    p = Player((1, 1), 2.0)
    p.tile = (2, 2)
    p.direction = "right"
    p._progress = 0.8
    p.reset()

    assert p.tile == (1, 1)
    assert p.direction is None
    assert p.speed == 2.0
    assert p._progress == 0.0


def test_scree_pos() -> None:
    p = Player((1, 1), 2.0)
    assert p.screen_pos() == (1.0, 1.0)
    p.direction = "right"
    p._progress = 0.25
    p.tile = (3, 1)
    assert p.screen_pos() == (3.25, 1.0)
    p.direction = "up"
    assert p.screen_pos() == (3.0, 0.75)
