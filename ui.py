from colorama import Fore, Style
from rich.console import Console
from rich.table import Table

console = Console()

def print_banner():
    banner = f"""{Fore.CYAN}
    ████████╗ █████╗ ███████╗██╗  ██╗    ███╗   ███╗ █████╗ ███████╗███╗   ██╗ █████╗  ██████╗ ███████╗██████╗ 
    ╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝    ████╗ ████║██╔══██╗██╔════╝████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗
       ██║   ███████║███████╗█████╔╝     ██╔████╔██║███████║███████╗██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝
       ██║   ██╔══██║╚════██║██╔═██╗     ██║╚██╔╝██║██╔══██║╚════██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗
       ██║   ██║  ██║███████║██║  ██╗    ██║ ╚═╝ ██║██║  ██║███████║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║
       ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
    {Style.RESET_ALL}"""
    print(banner)
    print(f"{Fore.YELLOW}{'='*105}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}\t\t\t🚀 WELCOME TO THE ULTIMATE TASK MANAGEMENT SYSTEM 🚀{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*105}{Style.RESET_ALL}\n")

def display_tasks_table(tasks):
    if not tasks:
        console.print("[yellow]No tasks found! Your list is empty.[/yellow]")
        return

    table = Table(title="📋 Your Task Dashboard", title_style="bold magenta", header_style="bold cyan")
    table.add_column("ID", justify="center", style="dim", width=4)
    table.add_column("Task Title", style="bold white", width=30)
    table.add_column("Priority", justify="center", width=12)
    table.add_column("Status", justify="center", width=12)
    table.add_column("Due Date", justify="center", width=15)
    table.add_column("Created At", justify="center", width=18)

    for t in tasks:
        prio = t.priority
        if prio == "High":
            prio_styled = f"[red]🔴 {prio}[/red]"
        elif prio == "Medium":
            prio_styled = f"[yellow]🟡 {prio}[/yellow]"
        else:
            prio_styled = f"[green]🟢 {prio}[/green]"

        status = t.status
        status_styled = f"[green]✔ {status}[/green]" if status == "Done" else f"[yellow]⏳ {status}[/yellow]"

        table.add_row(
            str(t.id),
            t.title,
            prio_styled,
            status_styled,
            t.due_date,
            t.created_at
        )

    console.print(table)

def show_dashboard(total, completed, pending, high_priority):
    percent = int((completed / total) * 100) if total > 0 else 0
    bar_length = 20
    filled_length = int(bar_length * completed // total) if total > 0 else 0
    bar = "█" * filled_length + "░" * (bar_length - filled_length)

    print(f"\n{Fore.CYAN}╔══════════════════════════════════════╗")
    print(f"║          📊 SYSTEM DASHBOARD         ║")
    print(f"╚══════════════════════════════════════╝{Style.RESET_ALL}")
    print(f" 📂 Total Tasks      : {Fore.WHITE}{total}")
    print(f" ✔ Completed Tasks   : {Fore.GREEN}{completed}")
    print(f" ⏳ Pending Tasks    : {Fore.YELLOW}{pending}")
    print(f" 🔴 High Priority    : {Fore.RED}{high_priority}")
    print(f" 📈 Completion Rate  : {Fore.CYAN}[{bar}] {percent}%\n")