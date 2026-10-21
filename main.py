from app import App
from config import Config
import sys


def main():

    if len(sys.argv) != 2:
        print("Usage: python main.py <map_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not filepath.endswith(".json"):
        print(f"Error: '{filepath}' must be a .json file", file=sys.stderr)
        sys.exit(1)

    settings = Config(filepath).load()
    print("Settings:", settings.pacgum)

    app = App(1000, 800)
    # setting infos
    app.settings = settings

    app.run()


if __name__ == "__main__":
    main()
