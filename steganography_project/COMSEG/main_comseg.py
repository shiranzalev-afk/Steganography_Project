from comseg import hide_comseg, extract_comseg


def main():
    print("1 - Hide message")
    print("2 - Extract message")

    choice = input("Choose: ")

    if choice == "1":
        path = input("Enter JPG path: ")
        message = input("Enter secret message: ")

        hide_comseg(path, message, "output.jpg")

        print("Message hidden successfully!")

    elif choice == "2":
        path = input("Enter stego JPG path: ")

        message = extract_comseg(path)

        print("Hidden message:", message)

    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()