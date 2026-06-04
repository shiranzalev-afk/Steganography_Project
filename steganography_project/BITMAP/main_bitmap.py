from bitmap import hide_bitmap, extract_bitmap


def main():
    print("1 - Hide message")
    print("2 - Extract message")

    choice = input("Choose: ")

    if choice == "1":
        path = input("Enter BMP image path: ")
        message = input("Enter secret message: ")

        hide_bitmap(path, message, "output.bmp")

        print("Message hidden successfully!")

    elif choice == "2":
        path = input("Enter stego BMP path: ")

        message = extract_bitmap(path)

        print("Hidden message:", message)

    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()