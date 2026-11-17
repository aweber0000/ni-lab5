from src.models import Apartment, Bill, Parameters, Tenant, Transfer


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []

        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True

    def get_apartment_costs(self, apartment_key: str, year: int, month: int) -> float:
        out = 0.0

        if apartment_key not in self.apartments:
            raise ValueError("Nieznane mieszkanie")

        if month < 0 or month > 12:
            raise ValueError("Nieprawidłowy numer miesiąca")

        for bill in filter(
            lambda b: (
                b.apartment == apartment_key
                and b.settlement_year == year
                and b.settlement_month == month
            ),
            self.bills,
        ):
            out += bill.amount_pln

        return out
