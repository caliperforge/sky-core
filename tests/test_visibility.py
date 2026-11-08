from datetime import date

import astropy.units as u
import pytest
from astropy.coordinates import AltAz, get_body
from astropy.time import Time

from skycore import Site, get, hours_above, moon, night, track, visibility

NIGHT = date(2026, 11, 10)
POLARIS = (37.95, 89.26)
T = Time("2026-11-11 03:00", scale="utc")


def _sun_alt(site: Site, t: Time) -> float:
    return get_body("sun", t, site.location).transform_to(AltAz(obstime=t, location=site.location)).alt.deg


def test_night_bounds_sit_at_astronomical_twilight():
    site = get("ANT")
    dusk, dawn = night(site, NIGHT)
    assert dusk < dawn
    assert _sun_alt(site, dusk) == pytest.approx(-18, abs=1)
    assert _sun_alt(site, dawn) == pytest.approx(-18, abs=1)
    assert 9 <= (dawn - dusk).to_value(u.hour) <= 12


def test_polaris_altitude_tracks_latitude():
    site = get("ANT")
    samples = track(site, *POLARIS, *night(site, NIGHT), 10)
    assert samples
    assert all(alt == pytest.approx(14.56, abs=1.5) for _, alt, _ in samples)


def test_hours_above_zero_for_never_risen_object():
    assert hours_above(get("G96"), 0.0, -80.0, NIGHT) == 0


def test_hours_above_exceeds_six_for_zenith_object():
    site = get("G96")
    midnight = Time("2026-11-11 00:00", scale="utc") - site.location.lon.deg / 15 * u.hour
    ra = midnight.sidereal_time("mean", longitude=site.location.lon).deg
    assert hours_above(site, ra, 32.4, NIGHT) > 6


def test_moon_values_in_range():
    m = moon(get("ANT"), *POLARIS, T)
    assert 0 <= m["separation_deg"] <= 180
    assert 0 <= m["illumination"] <= 1


def test_illumination_full_at_opposition(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(visibility, "_elongation_deg", lambda sun, moon_body: 180.0)
    assert moon(get("ANT"), *POLARIS, T)["illumination"] == pytest.approx(1.0, abs=1e-6)


def test_track_step_count():
    assert len(track(get("ANT"), *POLARIS, T, T + 2 * u.hour, 10)) == 12
