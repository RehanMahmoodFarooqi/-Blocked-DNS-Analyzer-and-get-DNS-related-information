from rich.console import Console
from rich.table import Table
import tkinter as tk
import webbrowser
import argparse
from blocked import check_blocked_websites
from dns_utils import dns_analyzer


class WebsiteAnalyzer:
    def __init__(self):
        self.console = Console()

    def display_dns_info(self, domain, dns_info):
        """Display DNS information in console"""
        table = Table(title=f"DNS Information for {domain}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("IP Address", dns_info['ip_address'])
        table.add_row("Ping Time", f"{dns_info['ping_time']} ms")
        table.add_row("A Records", "\n".join(dns_info['records']['A']))
        table.add_row("CNAME Records", "\n".join(dns_info['records']['CNAME']))
        table.add_row("MX Records", "\n".join(dns_info['records']['MX']))
        table.add_row("NS Records", "\n".join(dns_info['records']['NS']))
        table.add_row("TXT Records", "\n".join(dns_info['records']['TXT']))

        if dns_info['creation_date']:
            table.add_row("Creation Date", str(dns_info['creation_date']))
        if dns_info['expiration_date']:
            table.add_row("Expiration Date", str(dns_info['expiration_date']))

        self.console.print(table)

    def run_cli(self):
        """Run the command-line interface"""
        self.console.print("[yellow]Website Analysis Tool[/yellow]")
        self.console.print("[cyan]Choose an option:[/cyan]")

        while True:
            self.console.print("\n1. Check Blocked Websites")
            self.console.print("2. Get Domain Information")
            self.console.print("3. Launch GUI")
            self.console.print("4. Exit")

            choice = input("\nEnter your choice (1-4): ").strip()

            match choice:
                case "1":
                    check_blocked_websites()
                case "2":
                    self.console.print(
                        "\n[cyan]Enter 'back' to return to main menu[/cyan]")
                    while True:
                        domain = input("\nEnter domain name: ").lower().strip()
                        if domain == 'back':
                            break
                        if not domain:
                            self.console.print(
                                "[red]Please enter a valid domain name[/red]")
                            continue
                        success, dns_info = dns_analyzer.get_dns_info(domain)
                        if success:
                            self.display_dns_info(domain, dns_info)
                            open_browser = input(
                                "\nWould you like to open this website in browser? (y/n): ").lower()
                            if open_browser == 'y':
                                webbrowser.open(f'http://{domain}')
                case "3":
                    self.run_gui()
                case "4":
                    self.console.print("[yellow]Goodbye![/yellow]")
                    break
                case _:
                    self.console.print(
                        "[red]Invalid choice. Please enter 1, 2, 3, or 4[/red]")

    def run_gui(self):
        """Run the graphical user interface"""
        from gui import WebsiteAnalysisTool
        root = tk.Tk()
        app = WebsiteAnalysisTool(root)
        root.mainloop()


def main():
    """Main entry point of the application"""
    parser = argparse.ArgumentParser(description="Website Analysis Tool")
    parser.add_argument('--gui', action='store_true',
                        help='Launch in GUI mode')
    parser.add_argument('--cli', action='store_true',
                        help='Launch in CLI mode')
    args = parser.parse_args()

    analyzer = WebsiteAnalyzer()

    if args.gui:
        analyzer.run_gui()
    else:
        analyzer.run_cli()


if __name__ == "__main__":
    main()
