
import json
import os
from datetime import datetime

# ==========================================
#          THE CODE VIBES CAFE
#          Owner: Ayush Shukla
# ==========================================

MENU_FILE = "menu.json"
ORDERS_FILE = "orders.json"

DEFAULT_MENU = {
    "TEA": [
        {"name": "Masala Chai", "price": 15},
        {"name": "Kulhad Chai", "price": 25}
    ],

    "COFFEE": [
        {"name": "Hot Coffee", "price": 40},
        {"name": "Black Coffee", "price": 50},
        {"name": "Cold Coffee", "price": 70}
    ],

    "SANDWICH": [
        {"name": "Veg Sandwich", "price": 50},
        {"name": "Paneer Sandwich", "price": 70},
        {"name": "Paneer Cheese Sandwich", "price": 90},
        {"name": "Chicken Sandwich", "price": 70}
    ],

    "BURGER": [
        {"name": "Veg Burger", "price": 30},
        {"name": "Chicken Burger", "price": 50},
        {"name": "Extra Cheese Chicken Burger", "price": 70}
    ],

    "PIZZA": [
        {"name": "Margerita Pizza", "price": 100},
        {"name": "Paneer Pizza", "price": 150},
        {"name": "Sweet Corn Pizza", "price": 120},
        {"name": "Chicken Pizza", "price": 170}
    ],

    "DESSERT": [
        {"name": "Ice Cream (1 Scoop)", "price": 50},
        {"name": "Brownie", "price": 100},
        {"name": "Waffle", "price": 100},
        {"name": "Rasmalai", "price": 80},
        {"name": "Choco Chip Cookies (2 pcs)", "price": 100}
    ]
}

ICE_CREAM_FLAVOURS = [
    "Vanilla",
    "Strawberry",
    "Choco Chips",
    "Butterscotch",
    "Chocolate"
]

COUPONS = {
    "FIRST10": 10,
    "VIE20": 20,
    "BTECH25": 25,
    "KRMU30": 30
}


# ==========================================
#             DATA HANDLING
# ==========================================

def load_menu():
    if os.path.exists(MENU_FILE):
        try:
            with open(MENU_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Menu file could not be read. Loading default menu.")

    save_menu(DEFAULT_MENU)
    return DEFAULT_MENU.copy()


def save_menu(menu):
    with open(MENU_FILE, "w") as file:
        json.dump(menu, file, indent=4)


def save_order(order):
    orders = []

    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, "r") as file:
                orders = json.load(file)
        except (json.JSONDecodeError, OSError):
            orders = []

    orders.append(order)

    with open(ORDERS_FILE, "w") as file:
        json.dump(orders, file, indent=4)


menu = load_menu()


# ==========================================
#             HELPER FUNCTIONS
# ==========================================

def line():
    print("=" * 55)


def get_number(message, minimum=1):
    while True:
        try:
            number = int(input(message))

            if number < minimum:
                print("Please enter a valid number.")
            else:
                return number

        except ValueError:
            print("Please enter numbers only.")


def get_menu_items():
    items = []
    item_id = 1

    for category, products in menu.items():
        for product in products:
            items.append({
                "id": item_id,
                "category": category,
                "name": product["name"],
                "price": product["price"]
            })
            item_id += 1

    return items


# ==========================================
#                 WELCOME
# ==========================================

def welcome():
    line()
    print("             THE CODE VIBES")
    print("          FRESH BREWS & BITES")
    print("           Owner: Ayush Shukla")
    line()


# ==========================================
#              DISPLAY MENU
# ==========================================

def display_menu():
    print("\n                  CAFE MENU")
    line()

    items = get_menu_items()

    for category in menu:
        print("\n" + category)
        print("-" * 40)

        for item in items:
            if item["category"] == category:
                print(
                    str(item["id"]) + ".",
                    item["name"],
                    "- Rs.",
                    item["price"]
                )

    line()


# ==========================================
#             MENU MANAGEMENT
# ==========================================

def menu_management():
    while True:
        print("\n         MENU MANAGEMENT")
        line()
        print("1. View Menu")
        print("2. Add New Item")
        print("3. Update Item Price")
        print("4. Delete Item")
        print("5. Back to Main Menu")
        line()

        choice = input("Enter your choice: ")

        if choice == "1":
            display_menu()

        elif choice == "2":
            categories = list(menu.keys())

            print("\nAvailable Categories:")
            for i, category in enumerate(categories, start=1):
                print(i, ".", category)

            category_choice = get_number(
                "Choose category number: "
            )

            if category_choice > len(categories):
                print("Invalid category.")
                continue

            category = categories[category_choice - 1]

            name = input("Enter new item name: ").strip()

            if not name:
                print("Item name cannot be empty.")
                continue

            price = get_number("Enter item price: ")

            menu[category].append({
                "name": name,
                "price": price
            })

            save_menu(menu)
            print("Item added successfully!")

        elif choice == "3":
            display_menu()

            item_id = get_number("Enter item number to update: ")
            items = get_menu_items()

            if item_id > len(items):
                print("Invalid item number.")
                continue

            selected = items[item_id - 1]

            new_price = get_number("Enter new price: ")

            for product in menu[selected["category"]]:
                if product["name"] == selected["name"]:
                    product["price"] = new_price
                    break

            save_menu(menu)
            print("Price updated successfully!")

        elif choice == "4":
            display_menu()

            item_id = get_number("Enter item number to delete: ")
            items = get_menu_items()

            if item_id > len(items):
                print("Invalid item number.")
                continue

            selected = items[item_id - 1]

            menu[selected["category"]] = [
                product for product in menu[selected["category"]]
                if product["name"] != selected["name"]
            ]

            save_menu(menu)
            print("Item deleted successfully!")

        elif choice == "5":
            break

        else:
            print("Invalid choice. Try again.")


# ==========================================
#              PLACE NEW ORDER
# ==========================================

def place_order():
    cart = []

    while True:
        display_menu()

        print("\nEnter 0 to finish adding items.")

        item_id = get_number(
            "Enter item number (0 to finish): ",
            minimum=0
        )

        if item_id == 0:
            break

        items = get_menu_items()

        if item_id > len(items):
            print("Invalid item number.")
            continue

        selected = items[item_id - 1]

        quantity = get_number("Enter quantity: ")

        flavour = None

        if selected["name"] == "Ice Cream (1 Scoop)":
            print("\nAvailable Ice Cream Flavours:")

            for i, flavour_name in enumerate(
                ICE_CREAM_FLAVOURS, start=1
            ):
                print(i, ".", flavour_name)

            flavour_choice = get_number("Choose flavour: ")

            if flavour_choice > len(ICE_CREAM_FLAVOURS):
                print("Invalid flavour.")
                continue

            flavour = ICE_CREAM_FLAVOURS[flavour_choice - 1]

        cart.append({
            "name": selected["name"],
            "price": selected["price"],
            "quantity": quantity,
            "flavour": flavour
        })

        print(selected["name"], "added to cart!")

        another = input(
            "\nAdd another item? (y/n): "
        ).lower()

        if another != "y":
            break

    if not cart:
        print("No items were added to the order.")
        return

    checkout(cart)


# ==========================================
#               DISPLAY CART
# ==========================================

def display_cart(cart):
    print("\n                  YOUR ORDER")
    line()

    subtotal = 0

    for item in cart:
        amount = item["price"] * item["quantity"]
        subtotal += amount

        item_name = item["name"]

        if item["flavour"]:
            item_name += " - " + item["flavour"]

        print(item_name)
        print(
            "Rs.", item["price"],
            "x", item["quantity"],
            "=", "Rs.", amount
        )

    line()
    print("Subtotal: Rs.", subtotal)

    return subtotal


# ==========================================
#                COUPON SYSTEM
# ==========================================

def apply_coupon(subtotal):
    coupon = input(
        "\nEnter coupon code (or press Enter to skip): "
    ).strip().upper()

    if coupon == "":
        return 0

    if coupon not in COUPONS:
        print("Invalid coupon code.")
        return 0

    if coupon == "BTECH25":
        print("\nBTECH25 is for B.Tech students only.")
        verified = input(
            "Has the student's B.Tech ID card been checked? (y/n): "
        ).lower()

        if verified != "y":
            print("Coupon not applied.")
            return 0

    elif coupon == "KRMU30":
        print("\nKRMU30 is for K.R. Mangalam University students only.")
        verified = input(
            "Has the student's KRMU ID card been checked? (y/n): "
        ).lower()

        if verified != "y":
            print("Coupon not applied.")
            return 0

    discount_percent = COUPONS[coupon]
    discount = subtotal * discount_percent / 100

    print(
        "\nCoupon applied successfully!",
        discount_percent,
        "% discount"
    )

    return discount


# ==========================================
#              BILL GENERATION
# ==========================================

def checkout(cart):
    subtotal = display_cart(cart)

    discount = apply_coupon(subtotal)

    final_amount = subtotal - discount

    print("\n              BILL SUMMARY")
    line()

    print("Subtotal:       Rs.", round(subtotal, 2))
    print("Discount:       Rs.", round(discount, 2))
    print("Final Amount:   Rs.", round(final_amount, 2))

    line()

    confirm = input(
        "Confirm this order? (y/n): "
    ).lower()

    if confirm != "y":
        print("Order cancelled.")
        return

    customer_name = input(
        "Enter customer name: "
    ).strip()

    if not customer_name:
        customer_name = "Walk-in Customer"

    order = {
        "customer": customer_name,
        "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "items": cart,
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "total": round(final_amount, 2)
    }

    save_order(order)

    generate_receipt(order)


# ==========================================
#              RECEIPT GENERATION
# ==========================================

def generate_receipt(order):
    print("\n")
    line()
    print("                 THE CODE VIBES")
    print("              CAFE BILL RECEIPT")
    print("               Owner: Ayush Shukla")
    line()

    print("Customer:", order["customer"])
    print("Date:", order["date"])

    line()

    for item in order["items"]:
        name = item["name"]

        if item["flavour"]:
            name += " (" + item["flavour"] + ")"

        amount = item["price"] * item["quantity"]

        print(name)
        print(
            item["quantity"], "x Rs.", item["price"],
            " = Rs.", amount
        )

    line()

    print("Subtotal:      Rs.", order["subtotal"])
    print("Discount:      Rs.", order["discount"])
    print("TOTAL:         Rs.", order["total"])

    line()
    print("          THANK YOU FOR VISITING!")
    print("             VISIT AGAIN :)")
    line()


# ==========================================
#               VIEW PAST ORDERS
# ==========================================

def view_orders():
    if not os.path.exists(ORDERS_FILE):
        print("No previous orders found.")
        return

    try:
        with open(ORDERS_FILE, "r") as file:
            orders = json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Could not read previous orders.")
        return

    if not orders:
        print("No previous orders found.")
        return

    print("\n              PREVIOUS ORDERS")
    line()

    for i, order in enumerate(orders, start=1):
        print("\nOrder Number:", i)
        print("Customer:", order["customer"])
        print("Date:", order["date"])
        print("Total: Rs.", order["total"])
        line()


# ==========================================
#                MAIN PROGRAM
# ==========================================

def main():
    while True:
        welcome()

        print("\n               MAIN MENU")
        line()

        print("1. View Cafe Menu")
        print("2. Menu Management")
        print("3. Place New Order")
        print("4. View Previous Orders")
        print("5. Exit")

        line()

        choice = input("Enter your choice: ")

        if choice == "1":
            display_menu()

        elif choice == "2":
            menu_management()

        elif choice == "3":
            place_order()

        elif choice == "4":
            view_orders()

        elif choice == "5":
            print("\nThank you for visiting THE CODE VIBES!")
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


# Start the application
if __name__ == "__main__":
    main()
