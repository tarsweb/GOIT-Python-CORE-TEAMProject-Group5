from fields import Field

''''country. city. street. house. apartment.'''
class Address(Field):
    def __init__(self, country=None, city=None, street=None, house=None, apartment=None):
        self.address_dict ={'country': country, 'city': city, 'street': street, 'house': house, 'apartment': apartment}
        super().__init__(self.address_dict)

    def set_country(self, new_country):
        self.address_dict['country'] = new_country

    def set_city(self, new_city):
        self.address_dict['city'] = new_city

    def set_street(self, new_street):
        self.address_dict['street'] = new_street

    def set_house(self, new_house):
        self.address_dict['house'] = new_house

    def set_apartment(self, new_apartment):
        self.address_dict['apartment'] = new_apartment

    def __str__(self):
        address = [value for value in self.address_dict.values() if value is not None]
        return ', '.join(address)

x = Address('USE','eew',apartment='3', street='feerg', )
print(x)