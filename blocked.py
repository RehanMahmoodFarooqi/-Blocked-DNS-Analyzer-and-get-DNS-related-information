import socket
import dns.resolver
from rich.console import Console
from rich.table import Table
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def check_website_status(domain):
    """
    Check if a website is accessible and return its status and IP addresses.
    Returns only 'Accessible', 'Blocked', or 'Error' as status.
    """
    resolver = dns.resolver.Resolver()
    resolver.timeout = 2
    resolver.lifetime = 2

    try:
        answers = resolver.resolve(domain, "A")
        ip_addresses = [str(rdata) for rdata in answers]

        try:
            response = requests.get(f"http://{domain}", timeout=3)
            if response.status_code == 200:
                return {
                    "domain": domain,
                    "status": "Accessible",
                    "details": f"HTTP {response.status_code}, IPs: {', '.join(ip_addresses)}"
                }
            else:
                return {
                    "domain": domain,
                    "status": "Blocked",
                    "details": f"HTTP {response.status_code}, IPs: {', '.join(ip_addresses)}"
                }
        except requests.exceptions.RequestException:
            return {
                "domain": domain,
                "status": "Blocked",
                "details": f"Connection failed, IPs: {', '.join(ip_addresses)}"
            }

    except dns.resolver.NXDOMAIN:
        return {
            "domain": domain,
            "status": "Blocked",
            "details": "DNS resolution failed - Domain does not exist"
        }
    except dns.resolver.NoAnswer:
        return {
            "domain": domain,
            "status": "Blocked",
            "details": "DNS resolution failed - No A records"
        }
    except dns.exception.Timeout:
        return {
            "domain": domain,
            "status": "Blocked",
            "details": "DNS resolution timeout"
        }
    except Exception as e:
        return {
            "domain": domain,
            "status": "Error",
            "details": str(e)
        }


def check_blocked_websites():
    """
    Check a comprehensive list of websites for blocking status.
    Returns a list of results with each site's domain and status.
    """
    domains_to_check = [
        "facebook.com", "twitter.com", "instagram.com", "tiktok.com",
        "youtube.com", "netflix.com", "spotify.com",
        "telegram.org", "whatsapp.com", "discord.com",
        "twitch.tv", "roblox.com",
        "pornhub.com", "xvideos.com",
        "nordvpn.com", "expressvpn.com",
        "bbc.com", "cnn.com", "wikipedia.org",
        "mega.nz", "mediafire.com"
    ]

    results = []
    console = Console()
    console.print(
        "\n[yellow]Checking website accessibility status...[/yellow]")

    table = Table(title="Website Accessibility Report")
    table.add_column("Domain", style="cyan", no_wrap=True)
    table.add_column("Status", style="green", no_wrap=True)
    table.add_column("Details", style="white")

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_domain = {executor.submit(
            check_website_status, domain): domain for domain in domains_to_check}

        for future in as_completed(future_to_domain):
            result = future.result()
            status_style = {
                "Accessible": "green",
                "Blocked": "red",
                "Error": "red"
            }.get(result["status"], "white")

            table.add_row(result["domain"], f"[{status_style}]{
                          result['status']}[/{status_style}]", result["details"])
            results.append(result)

    console.print(table)
    console.print("\n[cyan]Scan completed[/cyan]")

    return results
