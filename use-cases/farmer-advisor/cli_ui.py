"""Rich terminal UI for Farmer Advisor. Reuses AK's AgentService (same engine as agentkernel.cli)."""

import asyncio
import logging
import sys

# Windows consoles may default to cp1252, which can't print emoji/box glyphs
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from agentkernel.core import AgentService
from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

console = Console()

ART = r"""
   .-.       .-.       .-.
  (   )     (   )     (   )
   \|/   __  \|/   __  \|/
    |   (__)  |   (__)  |
 ~~~+~~~~~+~~~+~~~~~+~~~+~~~
""".strip(
    "\n"
)

AGENTS = {
    "orchestrator": ("🧭", "Router", "Sends your question to the right specialist"),
    "crop_disease": ("🌱", "Plant Doctor", "Diagnoses crop diseases, treatment & prevention"),
    "market_price": ("💰", "Market Watch", "Live crop prices across markets"),
    "weather": ("⛅", "Sky Watch", "3-day forecast + spray & irrigation advice"),
}

HELP_ROWS = [
    ("!ls", "list agents"),
    ("!s <agent>", "talk to a specific agent"),
    ("!n", "new session"),
    ("!c", "clear session memory"),
    ("!h", "show help"),
    ("!q", "quit"),
]


def _header() -> Panel:
    art = Text(ART, style="green3")
    title = Text()
    title.append("FARMER ADVISOR\n", style="bold yellow1")
    title.append("Grow smart. Sell smart.\n\n", style="italic green3")
    title.append("🌱 diagnose diseases   💰 market prices   ⛅ weather advice", style="grey70")
    grid = Table.grid(padding=(0, 6))
    grid.add_column()
    grid.add_column(vertical="middle")
    grid.add_row(art, title)
    return Panel(Align.center(grid), box=box.HEAVY, border_style="green", padding=(1, 4))


def _agent_panel(service: AgentService) -> Panel:
    table = Table(box=box.SIMPLE_HEAD, header_style="bold green3", padding=(0, 2), expand=True)
    table.add_column("agent", style="bold white", no_wrap=True)
    table.add_column("role", style="yellow1", no_wrap=True)
    table.add_column("what it does", style="grey70")
    for name in service.runtime.agents():
        icon, role, desc = AGENTS.get(name, ("🤖", "", ""))
        table.add_row(f"{icon} {name}", role, desc)
    return Panel(table, title="[bold yellow1] your advisors [/]", box=box.ROUNDED, border_style="green")


def _help_panel() -> Panel:
    table = Table(box=None, show_header=False, padding=(0, 2))
    table.add_column(style="bold cyan", no_wrap=True)
    table.add_column(style="grey70")
    for cmd, desc in HELP_ROWS:
        table.add_row(cmd, desc)
    return Panel(table, title="[bold cyan] commands [/]", box=box.ROUNDED, border_style="cyan", expand=False)


def _reply_panel(agent_name: str, reply: str) -> Panel:
    icon, role, _ = AGENTS.get(agent_name, ("🤖", "", ""))
    return Panel(
        Markdown(str(reply)),
        title=f"[bold green3]{icon} {agent_name}[/] [dim]· {role}[/]",
        title_align="left",
        box=box.ROUNDED,
        border_style="green3",
        padding=(1, 2),
    )


def _welcome(service: AgentService) -> None:
    console.clear()
    console.print(_header())
    console.print(_agent_panel(service))
    console.print(Align.center(Text("Ask anything about your crops — type !h for commands, !q to quit", style="dim italic")))
    console.print()


async def run() -> None:
    service = AgentService()
    service.select()
    _welcome(service)

    while True:
        try:
            name = service.agent.name if service.agent else "none"
            prompt = console.input(f"[bold yellow1]🧑‍🌾 you[/][dim] → {name}[/] [bold green]❯[/] ")
            if not prompt.strip():
                continue
            if prompt.startswith("!"):
                tokens = prompt.lower().split()
                command, arg = tokens[0], tokens[1] if len(tokens) > 1 else None
                if command in ("!q", "!quit"):
                    console.print(Rule(style="green"))
                    console.print(Align.center(Text("Happy farming! 🌾", style="bold green")))
                    break
                elif command in ("!h", "!help"):
                    console.print(_help_panel())
                elif command in ("!ls", "!list"):
                    console.print(_agent_panel(service))
                elif command in ("!n", "!new"):
                    service.new()
                    _welcome(service)
                    console.print("[dim]✨ new session started[/]\n")
                elif command in ("!c", "!clear"):
                    service.clear()
                    console.print("[dim]🧹 session memory cleared[/]\n")
                elif command in ("!s", "!select") and arg:
                    service.select(name=arg, session_id=service.session.id if service.session else None)
                    console.print(f"[dim]now talking to[/] [bold green3]{arg}[/]\n")
                else:
                    console.print("[red]unknown command[/] — type [cyan]!h[/] for help\n")
                continue

            with console.status("[green3]consulting the field experts…[/]", spinner="dots", spinner_style="yellow1"):
                reply = await service.run(prompt=prompt)
            console.print(_reply_panel(service.agent.name, reply))
            console.print()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold green]Happy farming! 🌾[/]")
            break
        except Exception as e:  # keep the loop alive on agent/API errors
            console.print(f"[red]⚠ {e}[/]\n")


def main() -> None:
    logging.getLogger("ak").setLevel(logging.WARNING)  # keep the chat clean
    asyncio.run(run())
