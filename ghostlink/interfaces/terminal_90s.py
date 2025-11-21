"""90s Terminal Interface for GhostLink"""

import os
import time


def print_banner():
    """Print the retro 90s banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    GHOSTLINK AI ECOSYSTEM                    ║
║                      RETRO TERMINAL v1.0                     ║
║                                                              ║
║  ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗██╗     ██╗███╗   ██╗██╗  ██╗  ║
║ ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝██║     ██║████╗  ██║██║ ██╔╝  ║
║ ██║  ███╗███████║██║   ██║███████╗   ██║   ██║     ██║██╔██╗ ██║█████╔╝   ║
║ ██║   ██║██╔══██║██║   ██║╚════██║   ██║   ██║     ██║██║╚██╗██║██╔═██╗   ║
║ ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ███████╗██║██║ ╚████║██║  ██╗  ║
║  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝  ║
║                                                              ║
║                    [ CYBERPUNK EDITION ]                     ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def loading_sequence():
    """Show loading animation"""
    messages = [
        "INITIALIZING NEURAL NETWORKS...",
        "CONNECTING TO AI PROVIDERS...",
        "LOADING FREE API CATALOG...",
        "DEPLOYING AUTONOMOUS AGENTS...",
        "CALIBRATING CYBERPUNK INTERFACE...",
        "SYSTEM READY - WELCOME TO GHOSTLINK",
    ]

    for i, message in enumerate(messages):
        print(f"\r{message}", end="", flush=True)
        time.sleep(0.5)

        # Progress bar
        progress = "█" * (i + 1) + "░" * (len(messages) - i - 1)
        print(f" [{progress}] {i+1}/{len(messages)}", end="", flush=True)
        time.sleep(0.5)

    print("\n" + "=" * 60)


def main_menu():
    """Main interactive menu"""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print_banner()

        print("\n╭─[ MAIN MENU ]────────────────────────────────────────────╮")
        print("│  1. 🤖 AI CONVERSATION      Query AI providers           │")
        print("│  2. 🌐 FREE API ACCESS      Browse public APIs           │")
        print("│  3. 🧠 AUTONOMOUS AGENTS    Deploy intelligent agents    │")
        print("│  4. 📊 SYSTEM ANALYSIS      View system status           │")
        print("│  5. 📡 LIVE DATA STREAMS    Real-time data feeds         │")
        print("│  6. ⚙️  CONFIGURATION       System settings              │")
        print("│  0. ◢◤ EMERGENCY DISCONNECT                             │")
        print("╰──────────────────────────────────────────────────────────╯")

        try:
            choice = input("\nSELECT COMMAND > ").strip()
        except EOFError:
            break

        if choice == "1":
            print("\n🤖 AI CONVERSATION")
            print("-" * 17)
            question = input("Your question: ").strip()
            if question:
                print("Querying AI providers...")
                print(f"[Simulated] AI Response to: {question}")
            input("\nPress Enter to continue...")

        elif choice == "2":
            print("\n🌐 FREE API ACCESS")
            print("-" * 17)
            api_name = input("API name (jokes, advice, iss_location): ").strip()
            if api_name:
                print(f"Fetching data from {api_name}...")
                print(f"[Simulated] Data from {api_name}")
            input("\nPress Enter to continue...")

        elif choice == "3":
            print("\n🧠 AUTONOMOUS AGENTS")
            print("-" * 20)
            task = input("Task description: ").strip()
            if task:
                print("Deploying autonomous agent...")
                print(f"[Simulated] Agent executing: {task}")
            input("\nPress Enter to continue...")

        elif choice == "4":
            print("\n📊 SYSTEM ANALYSIS")
            print("-" * 18)
            print("AI Providers: 4 available")
            print("Free APIs: 10 available")
            print("Active Agents: 0")
            input("\nPress Enter to continue...")

        elif choice == "5":
            print("\n📡 LIVE DATA STREAMS")
            print("-" * 20)
            print("╭─[ LIVE DATA STREAM ]─")
            data_types = ["ISS.COORDS", "CRYPTO.BTC", "WEATHER.SF", "JOKE.RAND"]
            for _ in range(8):
                data_type = data_types[_ % len(data_types)]
                value = f"{1000 + _ * 10}.{10 + _}"
                status = ["OK", "SYNC", "LOAD"][_ % 3]
                print(f"│ {data_type:12} │ {value:8} │ {status:4} │")
                time.sleep(0.2)
            print("╰─────────────────────")
            input("\nPress Enter to continue...")

        elif choice == "6":
            print("\n⚙️  CONFIGURATION")
            print("-" * 15)
            print("Current configuration loaded from config.yaml")
            input("\nPress Enter to continue...")

        elif choice == "0":
            print("\n◢◤ EMERGENCY DISCONNECT ◥◣")
            break
        else:
            print("❌ Invalid command. Try again...")
            time.sleep(1)


def launch_90s_terminal():
    """Launch the 90s terminal interface"""
    os.system("cls" if os.name == "nt" else "clear")
    print_banner()
    loading_sequence()

    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n◢◤ EMERGENCY DISCONNECT ◥◣")
    except Exception as e:
        print(f"\n❌ SYSTEM ERROR: {e}")
