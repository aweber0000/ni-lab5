import pytest

from src.manager import Manager
from src.models import Parameters

def test_apartment_balance():
    manager = Manager(Parameters())

    assert manager.get_apartment_settlement("fake-apartment", 2025, 1) is None

    settlement = manager.get_apartment_settlement("apart-polanka", 2025, 1)

    assert settlement is not None
    assert settlement.apartment == "apart-polanka"
    assert settlement.year == 2025
    assert settlement.month == 1
    assert settlement.total_rent_pln == 7500.0
    assert settlement.total_bills_pln == 910.0
    assert settlement.total_due_pln == -6590.0

    settlement = manager.get_apartment_settlement("apart-polanka", 2023, 1)

    assert settlement is not None
    assert settlement.apartment == "apart-polanka"
    assert settlement.year == 2023
    assert settlement.month == 1
    assert settlement.total_rent_pln == 0.0
    assert settlement.total_bills_pln == 0.0
    assert settlement.total_due_pln == 0.0

    with pytest.raises(ValueError):
        manager.get_apartment_settlement("apart-polanka", 2025, 13)
