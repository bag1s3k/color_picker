import math


class RGB:
    """A class representing a color in the RGB color space."""

    def __init__(self, r: int, g: int, b: int):
        self.r, self.g, self.b = [
            value / 255 for value in [r, g, b]
        ]  # normalize RGB channels (0-1)

        self._max = max(self.r, self.g, self.b)
        self._min = min(self.r, self.g, self.b)
        self._delta = self._max - self._min

    def _hue(self) -> float:
        """Calculate Hue in degrees (0.0 - 360.0)."""
        if self._delta == 0:
            return 0.0

        result = 0.0
        match self._max:
            case self.r:
                result = ((self.g - self.b) / self._delta) % 6
            case self.g:
                result = ((self.b - self.r) / self._delta) + 2
            case self.b:
                result = ((self.r - self.g) / self._delta) + 4

        hue = result * 60
        return hue if hue >= 0 else hue + 360.0

    def _hsl_lightness(self) -> float:
        """Calculate HSL lightness as a coefficient (0.0 - 1.0)."""
        return (self._max + self._min) / 2

    def _hsl_saturation(self) -> float:
        """Calculate HSL saturation as a coefficient (0.0 - 1.0)."""
        if self._delta == 0:
            return 0.0

        result = 0.0
        if self._hsl_lightness() <= 0.5:
            result = self._delta / (self._max + self._min)
        else:
            result = self._delta / (2 - self._max - self._min)

        return result

    def _hsv_saturation(self) -> float:
        """Calculate HSV saturation as a coefficient (0.0 - 1.0)."""
        if self._max == 0:
            return 0.0
        return self._delta / self._max

    def _hsv_value(self) -> float:
        """Calculate HSV value (brightness) as a coefficient (0.0 - 1.0)."""
        return self._max

    def _hwb_whiteness(self) -> float:
        """Calculate HWB whiteness as a coefficient (0.0 - 1.0)."""
        return self._min

    def _hwb_blackness(self) -> float:
        """Calculate HWB blackness as a coefficient (0.0 - 1.0)."""
        return 1 - self._max

    def rgb(self) -> tuple[int, int, int]:
        """Return RGB"""
        return round(self.r * 255), round(self.g * 255), round(self.b * 255)

    def hsl(self) -> tuple[float, float, float]:
        """Convert RGB to HSL (Hue: 0-360°, Saturation: 0-100%, Lightness: 0-100%)."""
        return (
            round(self._hue(), 1),
            round(self._hsl_saturation() * 100, 1),
            round(self._hsl_lightness() * 100, 1),
        )

    def hsv(self) -> tuple[float, float, float]:
        """Convert RGB to HSV (Hue: 0-360°, Saturation: 0-100%, Value: 0-100%)."""
        return (
            round(self._hue(), 1),
            round(self._hsv_saturation() * 100, 1),
            round(self._hsv_value() * 100, 1),
        )

    def hwb(self) -> tuple[float, float, float]:
        """Convert RGB to HWB (Hue: 0-360°, Whiteness: 0-100%, Blackness: 0-100%)."""
        return (
            round(self._hue(), 1),
            round(self._hwb_whiteness() * 100, 1),
            round(self._hwb_blackness() * 100, 1),
        )

    def oklch(self) -> tuple[float, float, float]:
        """Convert RGB to OKLCH (Lightness: 0.0-1.0, Chroma: 0.0-0.4+, Hue: 0-360°)."""
        linear_channels = []
        for c in [self.r, self.g, self.b]:
            if c <= 0.04045:
                linear_channels.append(c / 12.92)
            else:
                linear_channels.append(((c + 0.055) / 1.055) ** 2.4)

        r_lin, g_lin, b_lin = linear_channels

        l = (0.41222147 * r_lin) + (0.53633253 * g_lin) + (0.05144599 * b_lin)  # noqa: E741
        m = (0.21190349 * r_lin) + (0.68069954 * g_lin) + (0.10739695 * b_lin)
        s = (0.08830246 * r_lin) + (0.28171883 * g_lin) + (0.62997870 * b_lin)

        l_ = math.cbrt(l)
        m_ = math.cbrt(m)
        s_ = math.cbrt(s)

        L = (0.21045425 * l_) + (0.79361778 * m_) - (0.00407204 * s_)
        a = (1.97799849 * l_) - (2.42859220 * m_) + (0.45059370 * s_)
        b = (0.02590403 * l_) + (0.78277176 * m_) - (0.80867576 * s_)

        C = math.sqrt(a**2 + b**2)

        H = math.degrees(math.atan2(b, a))
        if H < 0:
            H += 360.0

        return round(L, 3), round(C, 3), round(H, 1)
