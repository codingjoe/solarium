from solarium import led


class TestPowerToggle:
    def test_call(self):
        power = led.PowerToggle()

        power()
        assert not power

        power()
        assert power

    def test_bool(self):
        toggle = led.PowerToggle()
        assert toggle
        toggle.power = 0
        assert not toggle

    def test_int(self):
        toggle = led.PowerToggle()
        assert int(toggle) == 1
        toggle.power = 0
        assert int(toggle) == 0

    def test_mul(self):
        toggle = led.PowerToggle()
        assert toggle * 2 == 2
        toggle.power = 0
        assert toggle * 2 == 0

    def test_rmul(self):
        toggle = led.PowerToggle()
        assert 2 * toggle == 2
        toggle.power = 0
        assert 2 * toggle == 0
