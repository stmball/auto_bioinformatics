"""Placeholder code to test things are working properly."""
import argparse


def main() -> bool:
    """Run a simple function that returns True."""
    return True

def run_with_cli(args: argparse.Namespace) -> None:
    """Run the program with a CLI interface."""
    print("Running with CLI interface.")

def run_with_ui(args: argparse.Namespace) -> None:
    """Run the program with a GUI interface."""
    print("Running with GUI interface.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Placeholder code to test things are working properly.")
    
    parser.add_argument("--cli", action="store_true", help="Run the CLI version of the program.")

    args = parser.parse_args()

    if args.cli:
        run_with_cli(args)
    else:
        run_with_ui(args)



    main()
