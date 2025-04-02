from src.utils.load_units import load_scheduler

def terminal_ui():
    print("╔════════════════════════╗")
    print("║    COURSE SCHEDULER    ║")
    print("╚════════════════════════╝")

    while True:
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
                print("\nSchedule not generated!")
        elif choice == "2":
            scheduler.print_schedule()
        elif choice == "3":
            scheduler.save_schedule()
            print("\nSaved to output.json")
        elif choice == "4":
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    scheduler = load_scheduler('data/sample_input.json')
    terminal_ui()