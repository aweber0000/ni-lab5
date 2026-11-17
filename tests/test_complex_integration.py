import pytest

from src.manager import Manager
from src.models import Parameters


def test_manager_get_apartment_costs():
    parameters = Parameters()
    manager = Manager(parameters)

    assert manager.get_apartment_costs('apart-polanka', 2025, 1) == 910.0
    assert manager.get_apartment_costs('apart-polanka', 2025, 2) == 0.0
    assert manager.get_apartment_costs('apart-polanka', 2000, 1) == 0.0

    with pytest.raises(ValueError):
        manager.get_apartment_costs('FakeApartment', 2025, 1)

    with pytest.raises(ValueError):
        manager.get_apartment_costs('apart-polanka', 2025, 13)

