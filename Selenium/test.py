import main

test1 = main.Test()
def main():
    test1.start()
    test1.test_shipping_cost_calculation_valid()
    test1.test_shipping_cost_calculation_invalid()
    test1.test_registration_invalid_data()
    test1.test_registration_valid_data()
    test1.test_authorization_validdata()
    test1.test_authorization_invaliddata()

if __name__ == '__main__':
    main()