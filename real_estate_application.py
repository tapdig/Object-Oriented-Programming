def get_valid_input(input_string, valid_options):
    input_string += " ({}) ".format(", ".join(valid_options))
    response = input(input_string)
    while response.lower() not in valid_options:
        response = input(input_string)
    return response

class Property:
    def __init__(self, square_feet = "", beds = "", baths = "", **kwargs):
        super().__init__(**kwargs)
        self.square_feet = square_feet
        self.num_bedrooms = beds
        self.num_bathrooms = baths
    
    def display(self):
        print("PROPERTY DETAILS")
        print("================")
        print(f"square footage: {self.square_feet}")
        print(f"bedrooms: {self.num_bedrooms}")
        print(f"bathrooms: {self.num_bathrooms}")
        print()

    def prompt_init():
        return dict(square_feet = input("Enter the square feet: "), 
                beds = input("Enter number of bedrooms: "), 
                baths = input("Enter number of bathrooms: "))
    prompt_init = staticmethod(prompt_init)

class Apartment(Property):
    valid_laundries = ("coin", "ensuite", "none")
    valid_balconies = ("yes", "no", "solarium")

    def __init__(self, balcony = "", laundry = "", **kwargs):
        super().__init__(**kwargs)
        self.balcony = balcony
        self.laundry = laundry

    def display(self):
        super().display()
        print("APARTMENT DETAILS")
        print(f"laundry: {self.laundry}")
        print(f"has balcony: {self.balcony}")
        print()

    def prompt_init():
        parent_init = Property.prompt_init()
        laundry = get_valid_input("What laundry facilities does the property have? ", Apartment.valid_laundries)
        balcony = get_valid_input("Does the property have a balcony? ", Apartment.valid_balconies)
        parent_init.update({
            "laundry": laundry,
            "balcony": balcony
        })
        return parent_init
    prompt_init = staticmethod(prompt_init)

class House(Property):
    valid_garage = ("attached", "detached", "none")
    valid_fenced = ("yes", "no")

    def __init__(self, num_stories = "", garage = "", fenced = "", **kwargs):
        super().__init__(**kwargs)
        self.num_stories = num_stories
        self.garage = garage
        self.fenced = fenced

    def display(self):
        super().display()
        print("HOUSE DETAILS")
        print(f"number of stories: {self.num_stories}")
        print(f"garage: {self.garage}")
        print(f"fenced yard: {self.fenced}")
        print()

    def prompt_init():
        parent_init = Property.prompt_init()
        fenced = get_valid_input("Is the yard fenced? ", House.valid_fenced)
        garage = get_valid_input("Is there a garage? ", House.valid_garage)
        num_stories = input("How many stories: ")

        parent_init.update({
            "fenced": fenced,
            "garage": garage,
            "num_stories": num_stories
            })
        return parent_init
    prompt_init = staticmethod(prompt_init)

class Purchase:
    def __init__(self, price = "", taxes = "", **kwargs):
        super().__init__(**kwargs)
        self.price = price
        self.taxes = taxes

    def display(self):
        super().display()
        print("PURCHASE DETAILS")
        print(f"Selling price: {self.price}")
        print(f"Estimated taxes: {self.taxes}")
        print()

    def prompt_init():
        return dict(
                price = input("What is the selling price? "),
                taxes = input("What are the estimated taxes? "))
    prompt_init = staticmethod(prompt_init)

class Rental:
    def __init__(self, furnished = "", utilities = "", rent = "", **kwargs):
        super().__init__(**kwargs)
        self.furnished = furnished
        self.utilities = utilities
        self.rent = rent

    def display(self):
        super().display()
        print("RENTAL DETAILS")
        print(f"Rent: {self.rent}")
        print(f"Estimated utilities: {self.utilities}")
        print(f"Furnished: {self.furnished}")
        print()

    def prompt_init():
        return dict(
                rent = input("What is the monthly rent? "),
                utilities = input("What are the estimated utilities? "),
                furnished = get_valid_input("Is the property furnished? ", ("yes", "no")))
    prompt_init = staticmethod(prompt_init)

class HouseRental(Rental, House):
    def prompt_init():
        init = House.prompt_init()
        init.update(Rental.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)

class ApartmentRental(Rental, Apartment):
    def prompt_init():
        init = Apartment.prompt_init()
        init.update(Rental.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)

class ApartmentPurchase(Purchase, Apartment):
    def prompt_init():
        init = Apartment.prompt_init()
        init.update(Purchase.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)

class HousePurchase(Purchase, House):
    def prompt_init():
        init = House.prompt_init()
        init.update(Purchase.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)

class Agent:
    def __init__(self):
        self.property_list = []

    def display_properties(self):
        for property in self.property_list:
            property.display()

    type_map = {
            ("house", "rental"): HouseRental,
            ("house", "purchase"): HousePurchase,
            ("apartment", "rental"): ApartmentRental,
            ("apartment", "purchase"): ApartmentPurchase
            }

    def add_property(self):
        property_type = get_valid_input(
                "What type of property? ", ("house", "apartment")).lower()
        payment_type = get_valid_input(
                "What payment type? ", ("purchase", "rental")).lower()
        
        PropertyClass = self.type_map[
                (property_type, payment_type)]
        init_args = PropertyClass.prompt_init()
        self.property_list.append(PropertyClass(**init_args))

# =============== Client abstraction =============== #

agent = Agent()
agent.add_property()
print()
agent.add_property()
agent.display_properties()

