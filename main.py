from app import App
from config import Config
import sys


def main() -> None:
    """Parse the command line, load the config, and start the app."""

    if len(sys.argv) != 2:
        print("Usage: python main.py <map_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not filepath.endswith(".json"):
        print(f"Error: '{filepath}' must be a .json file", file=sys.stderr)
        sys.exit(1)

    settings = Config(filepath).load()

    app = App(2100, 1500, settings)
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("program interupted by the user")
