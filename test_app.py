import app


def test_is_threat_respects_thresholds():
    assert app.is_threat(-13, 29, -12, 30)
    assert not app.is_threat(-11, 29, -12, 30)
    assert not app.is_threat(-13, 31, -12, 30)


def test_parse_args_allows_threshold_changes():
    args = app.parse_args(["--shoulder-threshold", "-20", "--arm-threshold", "15"])
    assert args.shoulder_threshold == -20
    assert args.arm_threshold == 15


def test_fire_only_damages_when_locked():
    assert app.apply_fire(100, locked=True, damage=25) == 75
    assert app.apply_fire(100, locked=False, damage=25) == 100


def test_fire_health_stops_at_zero():
    assert app.apply_fire(10, locked=True, damage=25) == 0


if __name__ == "__main__":
    test_is_threat_respects_thresholds()
    test_parse_args_allows_threshold_changes()
    test_fire_only_damages_when_locked()
    test_fire_health_stops_at_zero()
    print("tests passed")
