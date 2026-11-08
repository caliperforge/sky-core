import datetime

import astropy.units as u
import numpy as np
from astropy.coordinates import AltAz, SkyCoord, get_body
from astropy.time import Time

from skycore.sites import Site

_TWILIGHT_DEG = -18.0
_NIGHT_STEP = 5 * u.min


def _altaz(site: Site, times: Time) -> AltAz:
    return AltAz(obstime=times, location=site.location)


def track(
    site: Site, ra: float, dec: float, start: Time, end: Time, step_min: float
) -> list[tuple[Time, float, float]]:
    n = int((end - start).to_value(u.min) / step_min)
    times = start + np.arange(n) * step_min * u.min
    altaz = SkyCoord(ra=ra, dec=dec, unit="deg", frame="icrs").transform_to(_altaz(site, times))
    return [(t, float(alt), float(az)) for t, alt, az in zip(times, altaz.alt.deg, altaz.az.deg)]


def _crossing(times: Time, alt: np.ndarray, i: int) -> Time:
    return times[i] + (alt[i] - _TWILIGHT_DEG) / (alt[i] - alt[i + 1]) * _NIGHT_STEP


def night(site: Site, date: datetime.date) -> tuple[Time, Time]:
    noon = Time(f"{date} 12:00", scale="utc") - site.location.lon.deg / 15 * u.hour
    times = noon + np.arange(24 * 60 // 5 + 1) * _NIGHT_STEP
    alt = get_body("sun", times, site.location).transform_to(_altaz(site, times)).alt.deg
    up = alt >= _TWILIGHT_DEG
    dusk = np.flatnonzero(up[:-1] & ~up[1:])[0]
    rises = np.flatnonzero(~up[:-1] & up[1:])
    dawn = rises[rises > dusk][0]
    return _crossing(times, alt, dusk), _crossing(times, alt, dawn)


def hours_above(site: Site, ra: float, dec: float, date: datetime.date, min_alt: float = 20.0) -> float:
    dusk, dawn = night(site, date)
    return sum(alt >= min_alt for _, alt, _ in track(site, ra, dec, dusk, dawn, 10)) * 10 / 60


def _elongation_deg(sun: SkyCoord, moon_body: SkyCoord) -> float:
    return float(sun.separation(moon_body).deg)


def moon(site: Site, ra: float, dec: float, t: Time) -> dict[str, float]:
    sun = get_body("sun", t, site.location)
    moon_body = get_body("moon", t, site.location)
    frame = _altaz(site, t)
    target = SkyCoord(ra=ra, dec=dec, unit="deg", frame="icrs").transform_to(frame)
    moon_altaz = moon_body.transform_to(frame)
    e = _elongation_deg(sun, moon_body)
    return {
        "separation_deg": float(target.separation(moon_altaz).deg),
        "alt_deg": float(moon_altaz.alt.deg),
        "illumination": float((1 - np.cos(np.radians(e))) / 2),
    }
