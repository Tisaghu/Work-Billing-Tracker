

# Work Billing Tracker: Main CLI and high-level flow
# Now imports logic from models.py, storage.py, and calculations.py for clarity and maintainability

from datetime import date, datetime
from models import WorkChunk
from storage import save_chunks_to_csv, load_chunks_from_csv
from calculations import (
    get_week_range, get_month_range, get_weekdays_in_range,
    get_total_minutes_for_range, get_total_minutes_for_day
)

def main():
    """
    Main loop for the billing tracker. Handles user interaction and high-level flow.
    All business logic, data models, and storage are imported from separate modules.
    """
    print("Welcome to the Work Billing Tracker!")
    chunks = load_chunks_from_csv()
    while True:
        print("\nMenu:")
        print("1. Add minutes for a day")
        print("2. View all entries for a day")
        print("3. Delete an entry")
        print("4. Show total minutes for a day")
        print("5. Show week/month progress")
        print("6. Exit")
        choice = input("Select an option (1-6): ").strip()

        if choice == '1':
            date_str = input("Enter date (YYYY-MM-DD, blank for today): ").strip()
            if not date_str:
                chunk_date = date.today()
            else:
                try:
                    chunk_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    print("Invalid date format.")
                    continue
            try:
                minutes = int(input("Enter minutes to add: ").strip())
                if minutes <= 0:
                    print("Minutes must be positive.")
                    continue
            except ValueError:
                print("Invalid number of minutes.")
                continue
            description = input("Optional description (ticket, etc): ").strip()
            new_chunk = WorkChunk(chunk_date, minutes, description)
            chunks.append(new_chunk)
            save_chunks_to_csv(chunks)
            print(f"Added {minutes} minutes for {chunk_date}.")

        elif choice == '2':
            date_str = input("Enter date to view (YYYY-MM-DD, blank for today): ").strip()
            if not date_str:
                target_date = date.today()
            else:
                try:
                    target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    print("Invalid date format.")
                    continue
            print(f"\nEntries for {target_date}:")
            found = False
            for idx, chunk in enumerate(chunks):
                if chunk.chunk_date == target_date:
                    print(f"{idx+1}. {chunk.minutes} min - {chunk.description}")
                    found = True
            if not found:
                print("No entries for this date.")

        elif choice == '3':
            date_str = input("Enter date to delete from (YYYY-MM-DD, blank for today): ").strip()
            if not date_str:
                target_date = date.today()
            else:
                try:
                    target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    print("Invalid date format.")
                    continue
            entries = [ (i, c) for i, c in enumerate(chunks) if c.chunk_date == target_date ]
            if not entries:
                print("No entries for this date.")
                continue
            print(f"Entries for {target_date}:")
            for idx, (real_idx, chunk) in enumerate(entries, 1):
                print(f"{idx}. {chunk.minutes} min - {chunk.description}")
            try:
                del_choice = int(input("Enter entry number to delete: ").strip())
                if not (1 <= del_choice <= len(entries)):
                    print("Invalid entry number.")
                    continue
            except ValueError:
                print("Invalid input.")
                continue
            del_idx = entries[del_choice-1][0]
            removed = chunks.pop(del_idx)
            save_chunks_to_csv(chunks)
            print(f"Deleted {removed.minutes} min entry for {removed.chunk_date}.")

        elif choice == '4':
            date_str = input("Enter date to total (YYYY-MM-DD, blank for today): ").strip()
            if not date_str:
                target_date = date.today()
            else:
                try:
                    target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    print("Invalid date format.")
                    continue
            total = get_total_minutes_for_day(chunks, target_date)
            print(f"Total minutes billed for {target_date}: {total} (Target: 480)")

        elif choice == '5':
            # --- Show week/month progress ---
            print("\n1. Show week progress")
            print("2. Show month progress")
            sub_choice = input("Select (1-2, blank for week): ").strip()
            today = date.today()
            if sub_choice == '2':
                # Month progress
                start, end = get_month_range(today)
                period = 'month'
            else:
                # Default to week progress
                start, end = get_week_range(today)
                period = 'week'
            weekdays = get_weekdays_in_range(start, end)
            required = len(weekdays) * 480
            billed = get_total_minutes_for_range(chunks, start, end)
            remaining = required - billed
            print(f"\n{period.capitalize()} {start} to {end}:")
            print(f"  Required: {required} min ({required/60:.2f} hrs)")
            print(f"  Billed:   {billed} min ({billed/60:.2f} hrs)")
            print(f"  Remaining:{remaining} min ({remaining/60:.2f} hrs)")

        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please select 1-6.")


if __name__ == "__main__":
    main()
