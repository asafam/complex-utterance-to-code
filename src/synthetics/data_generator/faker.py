from typing import Optional
from faker import Faker
from faker.providers import BaseProvider, DynamicProvider


_fake = None


def get_faker(seed: Optional[int]) -> Faker:
    if not _fake:
        _fake = Faker()

        if seed:
            Faker.seed(seed)

        _fake.add_provider(brand_provider)
        _fake.add_provider(DigitsProvider)
        _fake.add_provider(TimeProvider)
    else:
        return _fake


brand_provider = DynamicProvider(
    provider_name="brand",
    elements=[
        "Apple",
        "Coca Cola",
        "Amazon",
        "Google",
        "Samsung",
        "Microsoft",
        "Disney",
        "Louis Vuitton",
        "Lego",
        "Nike",
    ],
)


class DigitsProvider(BaseProvider):
    def digit(self) -> str:
        digits = self.digits(1)
        return digits

    def two_digits(self) -> str:
        digits = self.digits(2)
        return digits

    def digits(self, n: int) -> str:
        digits = _fake.msisdn()[:n]
        while digits.startswith("0"):
            digits = _fake.msisdn()[:n]
        return digits


class TimeProvider(BaseProvider):
    def fake_hour(self) -> str:
        hour = int(_fake.time("%H"))
        hour = hour % 12 or 12
        hour_str = str(hour)
        return hour_str

    def time_hour(self) -> str:
        hours = self.fake_hour()
        time = f"{hours} {_fake.am_pm()}"
        return time

    def time_hour_minutes(self) -> str:
        hours = self.fake_hour()
        minutes = _fake.time("%M")
        time = f"{hours}:{minutes} {_fake.am_pm()}"
        return time
