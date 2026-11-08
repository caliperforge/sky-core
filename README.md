# sky-core

Shared Python package for CaliperForge sky lanes: site model, visibility, moving check. See issue #1.

Consumers: neo-watch A3 and rubin-alert-monitor B3.

```
uv add "sky-core @ git+https://github.com/caliperforge/sky-core"
```

| Code | Name | Long. E | ρcosφ' | ρsinφ' | limit_mag |
|---|---|---|---|---|---|
| G96 | Mt. Lemmon Survey | 249.21128 | 0.845107 | +0.533611 | 21.5 |
| F51 | Pan-STARRS 1, Haleakala | 203.74409 | 0.936241 | +0.351543 | 22.0 |
| T05 | ATLAS-HKO, Haleakala | 203.74299 | 0.936236 | +0.351547 | 19.5 |
| I41 | Palomar Mountain, ZTF | 243.14022 | 0.836322 | +0.546875 | 20.5 |
| W94 | MAPS, San Pedro de Atacama | 291.82019 | 0.921646 | -0.387713 | 20.0 |
| X05 | Rubin Observatory | 289.25058 | 0.864981 | -0.500958 | 24.5 |
| ANT | Antigua Guatemala | lat 14.5586, lon -90.7295, height 1530 m | | | 16.0 |

`limit_mag` is approximate; edit it in `skycore/sites.py`.
