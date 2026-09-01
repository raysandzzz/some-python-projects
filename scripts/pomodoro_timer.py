import time


def format_time(seconds: int) -> str:
    """Formats seconds into MM:SS format."""
    mins, secs = divmod(seconds, 60)    # Return a tuple like: (quotient: mins, remainder: secs)
    return f"{mins:02d}:{secs:02d}"


def run_timer(total_seconds: int, label: str = "Focus"):
    """Runs a countdown timer with an in-place progress bar."""
    bar_length = 40
    print(f"\n▶ Starting {label} session ({format_time(total_seconds)})\n")

    try:
        for elapsed in range(total_seconds + 1):
            remaining = total_seconds - elapsed
            progress = elapsed / total_seconds
            filled_len = int(bar_length * progress)

            bar = "█" * filled_len + "░" * (bar_length - filled_len)
            percent = progress * 100
            time_str = format_time(remaining)

            # \r overwrites the same line, flush=True ensures real-time rendering
            print(
                f"\r[{bar}] {percent:5.1f}% | Remaining: {time_str} | {label}. ",
                end="",
                flush=True
            )

            if remaining > 0:
                time.sleep(1)

        # Bell alert (\a) and completion message
        print("\a\n\n✔ Time is up!")

    # When user inputs Ctrl+C the timer stops
    except KeyboardInterrupt:
        print("\n\n[!] Timer paused")


def get_positive_int(prompt: str, default: int) -> int:
    """Helper to ask for integer inputs with defaults and error handling."""
    while True:
        raw_val = input(f"{prompt} [default: {default}]: ").strip()
        if not raw_val:
            return default
        if raw_val.isdigit() and int(raw_val) > 0:
            return int(raw_val)
        print("[!] Please enter a positive whole number.")


def main():
    print("=" * 45)
    print("         CLI Pomodoro Timer ⏱")
    print("=" * 45)
    print("1. Standard Pomodoro (25m work / 5m break)")
    print("2. Short Sprint (15m work / 3m break)")
    print("3. Custom Timer")
    print("4. Exit")
    print("-" * 45)

    choice = input("Select an option (1-4) [default: 1]: ").strip()

    if choice == "2":
        work_sec = 15 * 60
        break_sec = 3 * 60
    elif choice == "3":
        work_min = get_positive_int("Enter work duration in minutes", default=25)
        break_min = get_positive_int("Enter break duration in minutes", default=5)
        work_sec = work_min * 60
        break_sec = break_min * 60
    elif choice == "4":
        print("Goodbye! :)")
        return
    else:
        work_sec = 25 * 60
        break_sec = 5 * 60

    # 1. Work Session
    run_timer(work_sec, label="Study Session")

    # 2. Break Session prompt
    if break_sec > 0:
        print("-" * 45)
        input("💤 Press Enter to start your break...")
        run_timer(break_sec, label="Break Time")

    print("\n" + "=" * 45)
    print("Session complete! Great job.")
    print("=" * 45)
    input("\nPress Enter to exit...")
    time.sleep(1)
    print("Goodbye! :)")


if __name__ == "__main__":
    main()