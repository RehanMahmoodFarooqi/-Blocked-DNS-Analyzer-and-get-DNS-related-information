import socket
import webbrowser
import dns.resolver
import whois
from datetime import datetime
import subprocess
import platform
from rich.console import Console
from rich.table import Table
import re


class DNSAnalyzer:
    def __init__(self):
        self.console = Console()

    def validate_domain(self, domain):
        """Validate domain name format"""
        pattern = re.compile(
            r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        )
        return bool(pattern.match(domain))

    def get_ping_time(self, hostname):
        """Get ping time to the host"""
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', hostname]
        try:
            output = subprocess.check_output(command).decode().strip()
            if platform.system().lower() == 'windows':
                if 'Average' in output:
                    return output.split('Average = ')[-1].split('ms')[0]
            else:
                if 'time=' in output:
                    return output.split('time=')[-1].split(' ms')[0]
        except:
            return 'N/A'
        return 'N/A'

    def get_dns_info(self, domain):
        """Get DNS records for the domain"""
        if not self.validate_domain(domain):
            self.console.print("[red]Invalid domain format[/red]")
            return False, None

        try:
            self.console.print(f"\n[yellow]Resolving {domain}...[/yellow]")
            ip_address = socket.gethostbyname(domain)

            resolver = dns.resolver.Resolver()
            resolver.timeout = 5
            resolver.lifetime = 5

            records = {
                'A': [],
                'MX': [],
                'NS': [],
                'TXT': [],
                'CNAME': []
            }

            for record_type in records.keys():
                try:
                    answers = resolver.resolve(domain, record_type)
                    for rdata in answers:
                        records[record_type].append(str(rdata))
                except dns.resolver.NoAnswer:
                    records[record_type].append('No record found')
                except dns.resolver.NXDOMAIN:
                    self.console.print(
                        f"[red]Domain {domain} does not exist[/red]")
                    return False, None
                except dns.exception.Timeout:
                    records[record_type].append(
                        'Timeout while fetching record')
                except Exception as e:
                    records[record_type].append(f'Error: {str(e)}')

            try:
                w = whois.whois(domain)
                creation_date = w.creation_date[0] if isinstance(
                    w.creation_date, list) else w.creation_date
                expiration_date = w.expiration_date[0] if isinstance(
                    w.expiration_date, list) else w.expiration_date
            except:
                creation_date = expiration_date = None

            ping_time = self.get_ping_time(domain)

            dns_info = {
                'ip_address': ip_address,
                'ping_time': ping_time,
                'records': records,
                'creation_date': creation_date,
                'expiration_date': expiration_date
            }

            return True, dns_info

        except socket.gaierror:
            self.console.print(f"[red]Could not resolve domain {
                               domain}. Please check if the domain exists.[/red]")
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")
        return False, None


# Create a global instance
dns_analyzer = DNSAnalyzer()
