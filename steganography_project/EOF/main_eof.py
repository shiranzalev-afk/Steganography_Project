from eof import hide_eof, extract_eof


def main():
    print("1 - Hide file")
    print("2 - Extract file")

    choice = input("Choose: ")

    if choice == "1":
        carrier = input("Enter image path: ")
        secret = input("Enter secret file path: ")

        hide_eof(carrier, secret, "output.png")

        print("File hidden successfully!")

    elif choice == "2":
        stego = input("Enter stego image path: ")

        extract_eof(stego, "extracted_secret")

        print("Secret extracted successfully!")

    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()