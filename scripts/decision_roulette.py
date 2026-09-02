import secrets
import time
import subprocess
import sys

if sys.platform == "win32":
    subprocess.run("", shell=True)

def render_box(item: str, frame_type: int, content_width: int) -> str:
    """Renders an adaptive marquee-style box with clean line clearing."""
    borders = [
        ("╔", "═", "╗", "║", "╚", "╝", "★"),
        ("┌", "─", "┐", "│", "└", "┘", "☆"),
    ]
    tl, h, tr, v, bl, br, star = borders[frame_type % 2]

    # # Dynamic width to align frame borders with the longest option
    inner_width = content_width + 21
    inner_width = content_width + 20
    
    top_line = f"   {tl}{h * inner_width}{tr}\033[K"
    mid_line = f"   {v} {star}  SPINNING: [ {item:^{content_width}} ] {star} {v}\033[K"
    bot_line = f"   {bl}{h * inner_width}{br}\033[K"

    return f"{top_line}\n{mid_line}\n{bot_line}"


def spin_box(options: list[str]) -> str:
    """Spins options inside an animated marquee box with deceleration."""
    n = len(options)
    content_width = max(max(len(opt) for opt in options), 15)
    winning_idx = secrets.randbelow(n)
    total_steps = 32 + (winning_idx - (32 % n)) % n

    delay = 0.05
    print("\n" + "=" * 46)
    print("         🎰 DECISION ROULETTE 🎰")
    print("=" * 46 + "\n")

    first_frame = render_box(options[0], 0, content_width)
    print(first_frame)
    num_lines = len(first_frame.split("\n"))

    for step in range(total_steps + 1):
        current_idx = step % n
        current_item = options[current_idx]

        print(f"\033[{num_lines}F", end="")
        print(render_box(current_item, step, content_width), flush=True)

        time.sleep(delay)

        if step > total_steps - 10:
            delay *= 1.30
        elif step > total_steps - 18:
            delay *= 1.10

    winner = options[winning_idx]

    # Winner flash effect
    for i in range(8):
        time.sleep(0.4)
        print(f"\033[{num_lines}F", end="")
        print(render_box(winner, i, content_width), flush=True)

    print(f"\n\a¡ WINNER: [ {winner} ] :) !\n")
    return winner

# CLI UI
def main():
    raw = input("Enter options separated by comma [Enter for default]: ").strip()
    if raw:
        options = [opt.strip() for opt in raw.split(",") if opt.strip()]
    else:
        options = ["Pizza", "Burgers", "Sushi", "Tacos", "Arepas"]

    if len(options) < 2:
        print("❌ Please enter at least 2 options.")
        main()

    spin_box(options)
    input("Press Enter to continue...")
    

if __name__ == "__main__":
    main()