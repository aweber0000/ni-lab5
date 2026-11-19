from src.models import Apartment, ApartmentSettlement, Bill, Parameters, Tenant, TenantSettlement, Transfer


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

    def get_apartment_costs(self, apartment_key: str, year: int | None = None, month: int | None = None) -> float | None:
        out = 0.0

        if apartment_key not in self.apartments:
            return None

        if year is None and month is not None:
            raise ValueError("Przy podaniu roku należy podać miesiąc")

        if month is not None and (month < 0 or month > 12):
            raise ValueError("Nieprawidłowy numer miesiąca")

        for bill in self.bills:
            if bill.apartment != apartment_key:
                continue
            if year is not None and bill.settlement_year != year:
                continue
            if month is not None and bill.settlement_month != month:
                continue

            out += bill.amount_pln

        return out

    def get_apartment_settlement(self, apartment_key: str, year: int, month: int) -> ApartmentSettlement | None:
        if apartment_key not in self.apartments:
            return None

        if month < 0 or month > 12:
            raise ValueError("Nieprawidłowy numer miesiąca")

        # Przyjmujemy, że:
        # total_rent_pln = łącznie ile zarobiliśmy z transferów od lokatorów, czyli suma "amount" z "transfers"
        total_rent_pln: float = 0.0
        # total_bills_pln = łącznie ile musieliśmy zapłacić, czyli suma "amount" z "bills"
        total_bills_pln: float = 0.0

        for bill in self.bills:
            if bill.settlement_year != year or bill.settlement_month != month:
                continue

            total_bills_pln += bill.amount_pln

        for transfer in self.transfers:
            if transfer.settlement_year != year or transfer.settlement_month != month:
                continue

            total_rent_pln += transfer.amount_pln

        total_due_pln = total_bills_pln - total_rent_pln

        return ApartmentSettlement(
            apartment=apartment_key,
            year=year,
            month=month,
            total_rent_pln=total_rent_pln,
            total_bills_pln=total_bills_pln,
            total_due_pln=total_due_pln,
        )

    def create_tenant_settlements(self, apartment_key: str, year: int, month: int) -> list[TenantSettlement]:
        apartment_settlement = self.get_apartment_settlement(apartment_key, year, month)

        if apartment_settlement is None:
            return []

        out = []
        tenant_keys = []

        for tenant_key, tenant in self.tenants.items():
            if tenant.apartment != apartment_key:
                continue

            tenant_keys.append(tenant_key)

        bills_pln = apartment_settlement.total_bills_pln / len(tenant_keys)

        for tenant_key in tenant_keys:
            rent_pln = self.tenants[tenant_key].rent_pln
            out.append(TenantSettlement(
                tenant=tenant_key,
                apartment_settlement=apartment_key,
                year=year,
                month=month,
                bills_pln=bills_pln,
                rent_pln=rent_pln,
                total_due_pln=bills_pln+rent_pln,
                balance_pln=0.0
            ))

        return out
