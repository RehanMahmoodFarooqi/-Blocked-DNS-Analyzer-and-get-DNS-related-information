import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import webbrowser
from blocked import check_blocked_websites
from dns_utils import dns_analyzer


class WebsiteAnalysisTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Website Analysis Tool")
        self.root.geometry("800x600")

        # Configure style
        style = ttk.Style()
        style.configure('TButton', padding=5, font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'))

        self.create_main_screen()

    def create_main_screen(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main header
        header = ttk.Label(
            self.root,
            text="Website Analysis Tool",
            style='Header.TLabel'
        )
        header.pack(pady=20)

        # Frame for buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(expand=True)

        # Domain Info Button
        domain_btn = ttk.Button(
            button_frame,
            text="Get Domain Information",
            command=self.show_domain_screen,
            width=30
        )
        domain_btn.pack(pady=10)

        # Blocked Sites Button
        blocked_btn = ttk.Button(
            button_frame,
            text="Check Blocked Websites",
            command=self.show_blocked_sites,
            width=30
        )
        blocked_btn.pack(pady=10)

        # Exit Button
        exit_btn = ttk.Button(
            button_frame,
            text="Exit",
            command=self.root.quit,
            width=30
        )
        exit_btn.pack(pady=10)

    def format_dns_info(self, domain, dns_info):
        """Format DNS information for display"""
        text = f"DNS Information for {domain}\n"
        text += "=" * 50 + "\n\n"

        text += f"IP Address: {dns_info['ip_address']}\n"
        text += f"Ping Time: {dns_info['ping_time']} ms\n\n"

        for record_type, records in dns_info['records'].items():
            text += f"{record_type} Records:\n"
            for record in records:
                text += f"  {record}\n"
            text += "\n"

        if dns_info['creation_date']:
            text += f"Creation Date: {dns_info['creation_date']}\n"
        if dns_info['expiration_date']:
            text += f"Expiration Date: {dns_info['expiration_date']}\n"

        return text

    def show_domain_screen(self):
        # Clear main screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create domain analysis interface
        ttk.Label(
            self.root,
            text="Domain Information",
            style='Header.TLabel'
        ).pack(pady=20)

        # Domain entry
        entry_frame = ttk.Frame(self.root)
        entry_frame.pack(pady=10)

        ttk.Label(
            entry_frame,
            text="Enter Domain:"
        ).pack(side=tk.LEFT, padx=5)

        domain_entry = ttk.Entry(entry_frame, width=40)
        domain_entry.pack(side=tk.LEFT, padx=5)

        # Results display
        result_text = scrolledtext.ScrolledText(
            self.root,
            height=20,
            width=70,
            font=('Courier', 10)
        )
        result_text.pack(pady=20, padx=20)

        def fetch_dns_info():
            domain = domain_entry.get().strip()
            if not domain:
                messagebox.showerror("Error", "Please enter a domain name")
                return

            result_text.delete(1.0, tk.END)
            result_text.insert(
                tk.END, f"Fetching information for {domain}...\n\n")
            result_text.update()

            # Get DNS information
            success, dns_info = dns_analyzer.get_dns_info(domain)
            if success:
                result_text.delete(1.0, tk.END)
                result_text.insert(
                    tk.END, self.format_dns_info(domain, dns_info))
                if messagebox.askyesno("Open Website",
                                       f"Would you like to open {domain} in browser?"):
                    webbrowser.open(f"http://{domain}")
            else:
                result_text.delete(1.0, tk.END)
                result_text.insert(
                    tk.END, f"Failed to fetch DNS information for {domain}")

        # Buttons frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Check Domain",
            command=fetch_dns_info
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Back to Main Menu",
            command=self.create_main_screen
        ).pack(side=tk.LEFT, padx=5)

    def show_blocked_sites(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Blocked Websites",
                  style='Header.TLabel').pack(pady=20)

        result_text = scrolledtext.ScrolledText(
            self.root, height=20, width=70, font=('Courier', 10))
        result_text.pack(pady=20, padx=20)

        blocked_sites = check_blocked_websites()
        result_text.delete(1.0, tk.END)
        if blocked_sites:
            for site_info in blocked_sites:
                result_text.insert(tk.END, f"{site_info['domain']}: {
                                   site_info['status']}\nDetails: {site_info['details']}\n\n")
        else:
            result_text.insert(tk.END, "No blocked websites found.")

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Back to Main Menu",
                   command=self.create_main_screen).pack(side=tk.LEFT, padx=5)

        # Check for blocked websites
        blocked_sites = check_blocked_websites()
        result_text.delete(1.0, tk.END)
        if blocked_sites:
            for site in blocked_sites:
                result_text.insert(tk.END, f"- {site}\n")
        else:
            result_text.insert(tk.END, "No blocked websites found.")

        # Buttons frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Back to Main Menu",
            command=self.create_main_screen
        ).pack(side=tk.LEFT, padx=5)


# Only create root window if running directly
if __name__ == "__main__":
    root = tk.Tk()
    app = WebsiteAnalysisTool(root)
    root.mainloop()
