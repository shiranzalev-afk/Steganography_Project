from LSB.encrypt import Encryptor
from LSB.decrypt import Decryptor
import imageio.v2 as imageio

def main():
    print("1 - Hide message")
    print("2 - Extract message")

    choice = input("Choose: ")

    if choice == "1":
        path = input("Enter image path: ")
        message = input("Enter secret.txt message: ")
        password = input("Enter password: ")

        im = imageio.imread(path).astype('uint8')  # להבטיח שהפיקסלים הם מסוג uint8

        enc = Encryptor(password)
        enc.encrypt(im, message, "output.png")

        print("Message hidden successfully!")

    elif choice == "2":
        path = input("Enter image path: ")
        password = input("Enter password: ")

        im = imageio.imread(path)

        dec = Decryptor(password)
        message = dec.decrypt(im)

        print("Hidden message:", message)

    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()