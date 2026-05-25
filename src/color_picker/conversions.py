import math

from color_picker.constants import ColorSpaceType


class ColorConverter:
    """A class representing a color in the RGB color space."""

    def __init__(self, r: int, g: int, b: int, selected_space: ColorSpaceType):
        self.r, self.g, self.b = [
            value / 255
            for value in [r, g, b]  # normalize RGB channels (0-1)
        ]

        self._max = max(self.r, self.g, self.b)
        self._min = min(self.r, self.g, self.b)
        self._delta = self._max - self._min

        self._channels: list[float | int | str] = [r, g, b]
        self.selected_space = selected_space

    @property
    def channels(self) -> list[float | int | str]:
        return self._channels

    @channels.setter
    def channels(self, new_channels: list[float | int | str]):
        """Setter # todo:"""
        self._channels = new_channels

        convert_method = getattr(self, f"from_{self.selected_space.lower()}")
        convert_method()

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

    def hex(self) -> list[str]:
        """Convert RGB to HEX

        Returns:
            list[str]: Wrapped in a list to match the interface of other conversions
                methods: (rgb, hsl, etc.) for the formatter
        """
        return [
            f"#{round(self.r * 255):02X}{round(self.g * 255):02X}{round(self.b * 255):02X}"
        ]

    @staticmethod
    def _hue_to_rgb_channels(self, h_prime: float, c: float, x: float) -> tuple[float, float, float]:
        """Helper method to determine temporary RGB channels based on hue sector."""
        if 0 <= h_prime < 1: return c, x, 0.0
        if 1 <= h_prime < 2: return x, c, 0.0
        if 2 <= h_prime < 3: return 0.0, c, x
        if 3 <= h_prime < 4: return 0.0, x, c
        if 4 <= h_prime < 5: return x, 0.0, c
        if 5 <= h_prime <= 6: return c, 0.0, x
        return 0.0, 0.0, 0.0

    def from_rgb(self) -> None:
        """Convert RGB to normalized RGB channels (0.0 - 1.0)."""
        self.r, self.g, self.b = (
            value / 255
            for value in self._channels
        )

    def from_hsl(self) -> None:
        """Convert HSL to RGB."""
        h = float(self._channels[0])
        s = float(self._channels[1]) / 100
        l = float(self._channels[2]) / 100

        c = (1 - abs((2 * l) - 1)) * s
        h_prime = h / 60
        x = c * (1 - abs((h_prime % 2) - 1))
        m = l - (c / 2)

        r1, g1, b1 = self._hue_to_rgb_channels(h_prime, c, x)

        self.r = r1 + m
        self.g = g1 + m
        self.b = b1 + m

    def from_hsv(self) -> None:
        """Convert HSV to RGB."""
        h = float(self._channels[0])
        s = float(self._channels[1]) / 100
        v = float(self._channels[2]) / 100

        c = v * s
        h_prime = h / 60
        x = c * (1 - abs((h_prime % 2) - 1))
        m = v - c

        r1, g1, b1 = self._hue_to_rgb_channels(h_prime, c, x)

        self.r = r1 + m
        self.g = g1 + m
        self.b = b1 + m

    def from_hwb(self) -> None:
        """Convert HWB to RGB."""
        h = float(self._channels[0])
        w = float(self._channels[1]) / 100
        b_black = float(self._channels[2]) / 100

        if w + b_black >= 1:
            gray = w / (w + b_black)

            self.r = gray
            self.g = gray
            self.b = gray
            return

        v = 1 - b_black
        s = 1 - (w / v) if v > 0 else 0

        c = v * s
        h_prime = h / 60
        x = c * (1 - abs((h_prime % 2) - 1))
        m = v - c

        r1, g1, b1 = self._hue_to_rgb_channels(h_prime, c, x)

        self.r = r1 + m
        self.g = g1 + m
        self.b = b1 + m

    def from_oklch(self) -> None:
        """Convert OKLCH to RGB."""
        l = float(self._channels[0])
        c = float(self._channels[1])
        h_deg = float(self._channels[2])

        h_rad = math.radians(h_deg)

        a = c * math.cos(h_rad)
        b = c * math.sin(h_rad)

        l_lin = l + (0.3963377774 * a) + (0.2158037573 * b)
        m_lin = l - (0.1055613458 * a) - (0.0638541728 * b)
        s_lin = l - (0.0894841775 * a) - (1.2914855480 * b)

        l_cubed = l_lin ** 3
        m_cubed = m_lin ** 3
        s_cubed = s_lin ** 3

        r_lin = (
                (4.0767416621 * l_cubed)
                - (3.3077115913 * m_cubed)
                + (0.2309699292 * s_cubed)
        )

        g_lin = (
                -(1.2684380046 * l_cubed)
                + (2.6097574011 * m_cubed)
                - (0.3413193965 * s_cubed)
        )

        b_lin = (
                -(0.0041960863 * l_cubed)
                - (0.7034186147 * m_cubed)
                + (1.7076147010 * s_cubed)
        )

        def to_srgb(channel: float) -> float:
            if channel <= 0.0031308:
                result = 12.92 * channel
            else:
                result = (1.055 * (max(channel, 0.0) ** (1 / 2.4))) - 0.055

            return max(0.0, min(1.0, result))

        self.r = to_srgb(r_lin)
        self.g = to_srgb(g_lin)
        self.b = to_srgb(b_lin)

    def from_hex(self) -> None:
        """Convert HEX to RGB."""
        data = str(self._channels[0])

        self.r, self.g, self.b = (
            int(data[i: i + 2], 16) / 255
            for i in range(0, 6, 2)
        )