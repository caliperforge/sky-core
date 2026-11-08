import pytest

from skycore import codes, get


@pytest.mark.parametrize(
    ("code", "lat", "lon"),
    [("G96", 32.44, -110.79), ("F51", 20.71, -156.26), ("X05", -30.24, -70.75)],
)
def test_mpc_sites_match_geodetic_check_values(code: str, lat: float, lon: float):
    location = get(code).location
    assert location.lat.deg == pytest.approx(lat, abs=0.05)
    assert location.lon.deg == pytest.approx(lon, abs=0.05)


def test_get_unknown_code_raises():
    with pytest.raises(KeyError):
        get("ZZZ")


def test_codes_lists_seven_sites():
    assert codes() == ["G96", "F51", "T05", "I41", "W94", "X05", "ANT"]
