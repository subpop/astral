import datetime
from math import degrees, radians, sin
from typing import Optional, Union

from astral import today
from astral.sun import julianday, proper_angle

__all__ = ["phase"]


def _phase_asfloat(date: datetime.date) -> float:
    jd = julianday(date)
    DT = pow((jd - 2382148), 2) / (41048480 * 86400)
    T = (jd + DT - 2451545.0) / 36525
    T2 = pow(T, 2)
    T3 = pow(T, 3)
    D = 297.85 + (445267.1115 * T) - (0.0016300 * T2) + (T3 / 545868)
    D = radians(proper_angle(D))
    M = 357.53 + (35999.0503 * T)
    M = radians(proper_angle(M))
    M1 = 134.96 + (477198.8676 * T) + (0.0089970 * T2) + (T3 / 69699)
    M1 = radians(proper_angle(M1))
    elong = degrees(D) + 6.29 * sin(M1)
    elong -= 2.10 * sin(M)
    elong += 1.27 * sin(2 * D - M1)
    elong += 0.66 * sin(2 * D)
    elong = proper_angle(elong)
    elong = round(elong)
    moon = ((elong + 6.43) / 360) * 28
    return moon


def phase(date: Optional[datetime.date] = None) -> float:
    """Calculates the phase of the moon on the specified date.

    Args:
        date: The date to calculate the phase for. Dates are always in the UTC timezone.

    Returns:
        A number designating the phase.

        ============  ==============
        0 .. 6.99     New moon
        7 .. 13.99    First quarter
        14 .. 20.99   Full moon
        21 .. 27.99   Last quarter
        ============  ==============
    """

    if date is None:
        date = today()

    moon = _phase_asfloat(date)
    if moon >= 28.0:
        moon -= 28.0
    return moon
