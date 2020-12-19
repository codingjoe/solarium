from solarium import led


class TestPowerToggleMixinMixin:
    def test_toggle(self):
        power = led.PowerToggleMixin()

        power.toggle()
        assert not power

        power.toggle()
        assert power

    def test_bool(self):
        toggle = led.PowerToggleMixin()
        assert toggle
        toggle.power = 0
        assert not toggle

    def test_int(self):
        toggle = led.PowerToggleMixin()
        assert int(toggle) == 1
        toggle.power = 0
        assert int(toggle) == 0

    def test_mul(self):
        toggle = led.PowerToggleMixin()
        assert toggle * 2 == 2
        toggle.power = 0
        assert toggle * 2 == 0

    def test_rmul(self):
        toggle = led.PowerToggleMixin()
        assert 2 * toggle == 2
        toggle.power = 0
        assert 2 * toggle == 0
