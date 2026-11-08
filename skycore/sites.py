import math
from dataclasses import dataclass

import astropy.units as u
from astropy.coordinates import EarthLocation

_R_KM = 6378.137


@dataclass(frozen=True)
class Site:
    code: str
    name: str
    location: EarthLocation
    limit_mag: float


def _mpc(code: str, lon_e: float, rc: float, rs: float, name: str, limit_mag: float) -> Site:
    lam = math.radians(lon_e)
    location = EarthLocation.from_geocentric(
        rc * math.cos(lam) * _R_KM, rc * math.sin(lam) * _R_KM, rs * _R_KM, unit=u.km
    )
    return Site(code, name, location, limit_mag)


_SITES = {
    site.code: site
    for site in (
        _mpc("G96", 249.21128, 0.845107, +0.533611, "Mt. Lemmon Survey", 21.5),
        _mpc("F51", 203.74409, 0.936241, +0.351543, "Pan-STARRS 1, Haleakala", 22.0),
        _mpc("T05", 203.74299, 0.936236, +0.351547, "ATLAS-HKO, Haleakala", 19.5),
        _mpc("I41", 243.14022, 0.836322, +0.546875, "Palomar Mountain, ZTF", 20.5),
        _mpc("W94", 291.82019, 0.921646, -0.387713, "MAPS, San Pedro de Atacama", 20.0),
        _mpc("X05", 289.25058, 0.864981, -0.500958, "Rubin Observatory", 24.5),
        Site(
            "ANT",
            "Antigua Guatemala",
            EarthLocation.from_geodetic(lon=-90.7295 * u.deg, lat=14.5586 * u.deg, height=1530 * u.m),
            16.0,
        ),
    )
}


def get(code: str) -> Site:
    return _SITES[code]


def codes() -> list[str]:
    return list(_SITES)
