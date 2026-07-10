"""Rich-based terminal UI for Farmer Advisor. Reuses AK's AgentService (same engine as agentkernel.cli)."""

import asyncio

from agentkernel.core import AgentService
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

console = Console()

BANNER = r"""
        _    _    _                                          [bold yellow]FARMER ADVISOR[/]
       (_)  (_)  (_)         __  __                          [green]Your farming assistant on WhatsApp & CLI[/]
      __|____|____|__       (  \/  )
     /               \       \    /   [dim]* Crop disease diagnosis[/]
    /  ~ ~ ~ ~ ~ ~ ~  \      _\  /_   [dim]* Market prices[/]
   /___________________\    (______)  [dim]* Weather & spraying advice[/]
"""

AGENT_ICONS = {"orchestrator": "🧭", "crop_disease": "🌱", "market_price": "💰", "weather": "🌦️"}
HELP = """[bold]Commands[/]
  [cyan]!ls[/]              list agents          [cyan]!s <agent>[/]  talk to a specific agent
  [cyan]!n[/]               new session          [cyan]!c[/]          clear session memory
  [cyan]!h[/]               this help            [cyan]!q[/]          quit"""


def _agent_table(service: AgentService) -> Table:
    table = Table(box=None, padding=(0, 2))
    table.add_column(style="bold green")
    table.add_column(style="dim")
    descriptions = {
        "orchestrator": "Routes your question to the right specialist",
        "crop_disease": "Diagnoses crop diseases, treatment & prevention",
        "market_price": "Current crop prices per market",
        "weather": "3-day forecast + spray/irrigation advice",
    }
    for name in service.runtime.agents():
        table.add_row(f"{AGENT_ICONS.get(name, '🤖')} {name}", descriptions.get(name, ""))
    return table


async def run() -> None:
    service = AgentService()
    console.print(BANNER, highlight=False)
    service.select()
    console.print(Panel(_agent_table(service), title="[bold]agents[/]", border_style="green"))
    console.print("[dim]Type your question, or !h for commands.[/]\n")

    while True:
        try:
            name = service.agent.name if service.agent else "none"
            prompt = console.input(f"[bold yellow]🧑‍🌾 you[/] [dim]({name})[/] [bold green]»[/] ")
            if not prompt.strip():
                continue
            if prompt.startswith("!"):
                tokens = prompt.lower().split()
                command, arg = tokens[0], tokens[1] if len(tokens) > 1 else None
                if command in ("!q", "!quit"):
                    console.print("[green]Happy farming! 🌾[/]")
                    break
                elif command in ("!h", "!help"):
                    console.print(Panel(HELP, border_style="dim"))
                elif command in ("!ls", "!list"):
                    console.print(Panel(_agent_table(service), title="[bold]agents[/]", border_style="green"))
                elif command in ("!n", "!new"):
                    service.new()
                    console.print("[dim]✨ new session started[/]")
                elif command in ("!c", "!clear"):
                    service.clear()
                    console.print("[dim]🧹 session memory cleared[/]")
                elif command in ("!s", "!select") and arg:
                    service.select(name=arg, session_id=service.session.id if service.session else None)
                    console.print(f"[dim]now talking to[/] [bold green]{arg}[/]")
                else:
                    console.print("[red]Unknown command.[/] Type [cyan]!h[/] for help.")
                continue

            with console.status("[green]consulting the field experts...[/]", spinner="earth"):
                reply = await service.run(prompt=prompt)
            icon = AGENT_ICONS.get(service.agent.name, "🤖")
            console.print(Panel(Markdown(str(reply)), title=f"{icon} [bold]{service.agent.name}[/]", border_style="green", padding=(1, 2)))
            console.print()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[green]Happy farming! 🌾[/]")
            break
        except Exception as e:  # keep the loop alive on agent/API errors
            console.print(f"[red]⚠ {e}[/]")


def main() -> None:
    asyncio.run(run())
