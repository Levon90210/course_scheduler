import argparse
import sys
from src.scheduler import Scheduler
from src.utils.load_utils import load_scheduler

def terminal_ui(scheduler: Scheduler) -> None:
    print("╔════════════════════════╗")
    print("║    COURSE SCHEDULER    ║")
    print("╚════════════════════════╝")

    while True:
        try:
            print("\nOptions:")
            print("1. Generate Schedule")
            print("2. View Schedule")
            print("3. Save to JSON")
            print("4. Exit")
            choice = input("> ")

            if choice == "1":
                if scheduler.solve() == "Optimal":
                    print("\nSchedule generated!")
                else:
                    print("\nSchedule not generated")
            elif choice == "2":
                scheduler.print_schedule()
            elif choice == "3":
                scheduler.save_schedule()
                print("\nSaved to output.json")
            elif choice == "4":
                sys.exit(0)
            else:
                print("Invalid choice")

        except KeyboardInterrupt:
            print("Use option 4 to exit properly")

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", type=str,
                            default="data/complex_input.json", help="Input JSON file path")
        args = parser.parse_args()
        scheduler = load_scheduler(args.input)
        terminal_ui(scheduler)

    except FileNotFoundError:
        print(f"Error: Input file not found at {args.input}")
        sys.exit(1)

    except Exception as e:
        print(f"Fatal error: {str(e)}", file=sys.stderr)
        sys.exit(1)