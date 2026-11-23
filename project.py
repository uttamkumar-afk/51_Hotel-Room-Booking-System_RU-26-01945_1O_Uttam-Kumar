rooms = {
    101: {"type": "Single", "rate": 2000},
    102: {"type": "Double", "rate": 3500},
    201: {"type": "Suite", "rate": 6000}
}

bookings = []


def load_bookings():
    """Load saved bookings from bookings.txt when the program starts."""
    try:
        file = open("bookings.txt", "r")
        for line in file:
            data = line.strip().split("|")
            if len(data) == 3:
                booking = {
                    "room": int(data[0]),
                    "guest": data[1],
                    "nights": int(data[2])
                }
                bookings.append(booking)
        file.close()
    except FileNotFoundError:
        pass
    except ValueError:
        print("Warning: Some booking data in the file is invalid.")


def save_bookings():
    """Save all bookings in the text file."""
    file = open("bookings.txt", "w")
    for booking in bookings:
        line = str(booking["room"]) + "|" + booking["guest"] + "|" + str(booking["nights"])
        file.write(line + "\n")
    file.close()


def view_available_rooms():
    """Display rooms that are not currently booked."""
    print("\n--- AVAILABLE ROOMS ---")
    found = False

    for room_number in rooms:
        booked = False

        for booking in bookings:
            if booking["room"] == room_number:
                booked = True

        if not booked:
            print("Room:", room_number,
                  "| Type:", rooms[room_number]["type"],
                  "| Rate per night: Rs.", rooms[room_number]["rate"])
            found = True

    if not found:
        print("Sorry, no rooms are available.")


def generate_bill(room_number, guest_name, nights):
    """Calculate and display the room bill with 12% GST."""
    rate = rooms[room_number]["rate"]
    amount = rate * nights
    gst = amount * 12 / 100
    total = amount + gst

    print("\n--- HOTEL BILL ---")
    print("Guest:", guest_name)
    print("Room:", room_number)
    print("Number of nights:", nights)
    print("Room charge: Rs.", amount)
    print("GST (12%): Rs.", int(gst))
    print("Total bill: Rs.", int(total))


def book_room():
    """Take booking details and book a room if it is available."""
    print("\n--- BOOK A ROOM ---")
    guest_name = input("Enter guest name: ").strip()

    if guest_name == "" or "|" in guest_name:
        print("Invalid guest name.")
        return

    try:
        room_number = int(input("Enter room number (101, 102, 201): "))
        nights = int(input("Enter number of nights (1 to 30): "))
    except ValueError:
        print("Please enter numbers correctly.")
        return

    if room_number not in rooms:
        print("Invalid room number. Please choose 101, 102 or 201.")
        return

    if nights < 1 or nights > 30:
        print("Number of nights must be between 1 and 30.")
        return

    for booking in bookings:
        if booking["room"] == room_number:
            print("Room", room_number, "is already booked. Please choose another room.")
            return

    new_booking = {
        "room": room_number,
        "guest": guest_name,
        "nights": nights
    }

    bookings.append(new_booking)
    save_bookings()

    print("\nRoom", room_number, "booked for", guest_name, "|", nights, "nights")
    generate_bill(room_number, guest_name, nights)
    print("Booking saved successfully.")


def cancel_booking():
    """Cancel a booking using the room number."""
    print("\n--- CANCEL BOOKING ---")

    try:
        room_number = int(input("Enter room number to cancel: "))
    except ValueError:
        print("Please enter a valid room number.")
        return

    for booking in bookings:
        if booking["room"] == room_number:
            bookings.remove(booking)
            save_bookings()
            print("Booking for room", room_number, "cancelled.")
            print("Room", room_number, "is now available.")
            return

    print("No booking found for this room.")


def show_bill():
    """Generate the bill for an existing booking."""
    print("\n--- GENERATE BILL ---")

    try:
        room_number = int(input("Enter room number: "))
    except ValueError:
        print("Please enter a valid room number.")
        return

    for booking in bookings:
        if booking["room"] == room_number:
            generate_bill(room_number, booking["guest"], booking["nights"])
            return

    print("No booking found for this room.")


def main():
    load_bookings()

    while True:
        print("\n========== HOTEL ROOM BOOKING SYSTEM ==========")
        print("1. View Available Rooms")
        print("2. Book a Room")
        print("3. Generate Bill")
        print("4. Cancel Booking")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_available_rooms()
        elif choice == "2":
            book_room()
        elif choice == "3":
            show_bill()
        elif choice == "4":
            cancel_booking()
        elif choice == "5":
            print("Thank you for using Hotel Room Booking System.")
            break
        else:
            print("Invalid choice. Please select from 1 to 5.")


if __name__ == "__main__":
    main()
