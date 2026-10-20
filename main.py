from app import App
import sys


def main():

    if len(sys.argv) != 2:
        print("Usage: python main.py <map_file>")
        sys.exit(1)

    filepath = sys.argv[1]

    app = App(2100, 1500)
    app.run()


if __name__ == "__main__":
    main()
