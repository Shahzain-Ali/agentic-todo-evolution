"""
Enhanced Rich CLI for Todo Console Application
"""
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text
from rich import print
from rich.layout import Layout
from rich.panel import Panel
from rich.tree import Tree
from rich.progress import Progress, SpinnerColumn, TextColumn
import pyfiglet
from typing import Optional
import sys
import colorama
from .models import TodoStorage
from .operations import (
    add_todo, list_todos, complete_todo, incomplete_todo,
    update_todo, delete_todo
)
from .validators import (
    validate_title, validate_description, validate_todo_id,
    validate_status_filter, validate_update_fields
)


class RichTodoApp:
    def __init__(self):
        self.storage = TodoStorage()
        self.console = Console()
        colorama.init()  # Initialize colorama for cross-platform colored output

    def display_welcome(self):
        """Display welcome screen with ASCII art"""
        self.console.clear()
        # Create ASCII art title
        ascii_art = pyfiglet.figlet_format("TODO APP", font="slant")
        print(f"[bold blue]{ascii_art}[/bold blue]")

        # Display welcome message
        welcome_panel = Panel(
            "[green]Welcome to the Todo Console Application![/green]\n\n"
            "[cyan]Manage your tasks efficiently with this beautiful interface.[/cyan]",
            title="[bold yellow]🎉 Welcome![/bold yellow]",
            border_style="bright_blue"
        )
        self.console.print(welcome_panel)

    def display_menu(self):
        """Display the main menu with colorful options"""
        self.console.clear()
        self.display_welcome()

        menu_tree = Tree("[bold bright_cyan]📋 Main Menu[/bold bright_cyan]")
        menu_tree.add("[bold yellow]1. ➕ Add Todo[/bold green]")
        menu_tree.add("[bold yellow]2. 📋 List Todos[/bold blue]")
        menu_tree.add("[bold yellow]3. ✅ Complete Todo[/bold yellow]")
        menu_tree.add("[bold yellow]4. ↩️  Mark Incomplete[/bold magenta]")
        menu_tree.add("[bold cyan]5. ✏️  Update Todo[/bold cyan]")
        menu_tree.add("[bold orange_red1]6. 🗑️  Delete Todo[/bold red]")
        menu_tree.add("[bold yellow]7. 📊 View Stats[/bold purple]")
        menu_tree.add("[bold red]8. 🚪 Exit[/bold orange_red1]")

        self.console.print(menu_tree)
        self.console.print("\n[yellow]Choose an option (1-8):[/yellow]")

    def display_todos_table(self, todos):
        """Display todos in a rich table format with color coding"""
        if not todos:
            self.console.print(Panel("[italic dim]No todos found. Add your first task! 🎉[/italic dim]",
                                   title="Empty List", border_style="yellow"))
            return

        # Create table with color headers
        table = Table(
            title="📋 Your Todos",
            show_header=True,
            header_style="bold bright_magenta",
            border_style="blue",
            title_style="bold cyan"
        )
        table.add_column("🆔 ID", style="dim", width=8)
        table.add_column(">Status", width=12)
        table.add_column("📝 Title", min_width=20)
        table.add_column("💬 Description", min_width=30)
        table.add_column("📅 Created", width=18)

        for todo in todos:
            if todo.status == "completed":
                status_symbol = "✅ [green]Completed[/green]"
                title_style = "strikethrough dim"
            else:
                status_symbol = "⏳ [yellow]Pending[/yellow]"
                title_style = "normal"

            table.add_row(
                f"[bold]{todo.id}[/bold]",
                status_symbol,
                f"[{title_style}]{todo.title}[/{title_style}]",
                todo.description if todo.description else "[italic dim]No description[/italic dim]",
                todo.created_at.strftime("%Y-%m-%d %H:%M")
            )

        self.console.print(table)

    def display_stats(self):
        """Display statistics about todos with visual elements"""
        todos = self.storage.get_all()
        total = len(todos)
        completed = len([t for t in todos if t.status == "completed"])
        pending = total - completed

        # Calculate completion percentage
        completion_rate = (completed / total * 100) if total > 0 else 0

        # Create progress bar visualization
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(description="Calculating stats...", total=100)
            for i in range(100):
                progress.update(task, advance=1)

        # Create stats panel with visual elements
        stats_content = f"""
[bright_green]📊 Your Todo Statistics[/bright_green]

[yellow]• Total Todos:[/yellow] [bold]{total}[/bold]
[yellow]• Completed:[/yellow] [green]{completed}[/green]
[yellow]• Pending:[/yellow] [yellow]{pending}[/yellow]
[yellow]• Completion Rate:[/yellow] [bold]{completion_rate:.1f}%[/bold]

Progress Bar: [{"█" * int(completion_rate // 5)}{"░" * int((100 - completion_rate) // 5)}] {int(completion_rate)}%
        """

        stats_panel = Panel(
            stats_content.strip(),
            title="[bold magenta]📈 Todo Stats[/bold magenta]",
            border_style="green"
        )
        self.console.print(stats_panel)

    def add_todo_interactive(self):
        """Interactive add todo with validation feedback"""
        self.console.clear()
        self.console.print(Panel("[bold cyan]➕ Adding New Todo[/bold cyan]", border_style="green"))

        # Get title with validation
        while True:
            title = Prompt.ask("\n[bold]Enter title[/bold] 📝")
            is_valid, error = validate_title(title)
            if is_valid:
                break
            else:
                self.console.print(f"[red]❌ {error}[/red]")

        # Get description
        description = Prompt.ask("[bold]Enter description (optional)[/bold] 💬", default="")

        is_valid, error = validate_description(description)
        if not is_valid:
            self.console.print(f"[red]❌ {error}[/red]")
            return

        # Show loading indicator while adding
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(description="Adding your todo...", total=100)
            for i in range(100):
                progress.update(task, advance=1)

        todo = add_todo(self.storage, title, description)
        if todo:
            self.console.print(f"[green]✅ Todo added successfully![/green]")
            self.display_todos_table([todo])
        else:
            self.console.print("[red]❌ Failed to add todo.[/red]")

    def list_todos_interactive(self):
        """Interactive list todos with filtering options"""
        self.console.clear()
        self.console.print(Panel("[bold blue]📋 Listing Todos[/bold blue]", border_style="blue"))

        # Filter options
        filter_tree = Tree("[bold cyan]Filter Options:[/bold cyan]")
        filter_tree.add("[bold]1. 📋 All todos[/bold]")
        filter_tree.add("[bold]2. ⏳ Pending only[/bold]")
        filter_tree.add("[bold]3. ✅ Completed only[/bold]")

        self.console.print(filter_tree)

        choice = Prompt.ask("\n[bold]Choose filter (1-3)[/bold]", choices=["1", "2", "3"], default="1")

        status_filter = None
        if choice == "2":
            status_filter = "pending"
        elif choice == "3":
            status_filter = "completed"

        todos = list_todos(self.storage, status_filter)
        self.display_todos_table(todos)

    def complete_todo_interactive(self):
        """Interactive complete todo with validation"""
        self.console.clear()
        self.console.print(Panel("[bold yellow]✅ Completing Todo[/bold yellow]", border_style="yellow"))

        todos = self.storage.get_all()
        if not todos:
            self.console.print(Panel("[italic dim]No todos to complete.[/italic dim]", border_style="yellow"))
            return

        self.display_todos_table(todos)
        todo_id_str = Prompt.ask("\n[bold]Enter ID of todo to complete[/bold] 🆔")

        is_valid, error, todo_id = validate_todo_id(todo_id_str, self.storage)
        if not is_valid:
            self.console.print(f"[red]❌ {error}[/red]")
            return

        # Check if already completed
        todo = self.storage.get_by_id(todo_id)
        if todo.status == "completed":
            self.console.print(f"[yellow]⚠️  Todo #{todo_id} is already completed.[/yellow]")
            return

        # Show loading while processing
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(description="Completing your todo...", total=100)
            for i in range(100):
                progress.update(task, advance=1)

        success = complete_todo(self.storage, todo_id)
        if success:
            updated_todo = self.storage.get_by_id(todo_id)
            self.console.print(f"[green]✅ Todo #{todo_id} marked as completed![/green]")
            self.display_todos_table([updated_todo])
        else:
            self.console.print(f"[red]❌ Failed to update todo #{todo_id}[/red]")

    def incomplete_todo_interactive(self):
        """Interactive mark incomplete with validation"""
        self.console.clear()
        self.console.print(Panel("[bold magenta]↩️  Marking Todo Incomplete[/bold magenta]", border_style="magenta"))

        todos = self.storage.get_all()
        if not todos:
            self.console.print(Panel("[italic dim]No todos to mark incomplete.[/italic dim]", border_style="yellow"))
            return

        # Only show completed todos
        completed_todos = [t for t in todos if t.status == "completed"]
        if not completed_todos:
            self.console.print(Panel("[italic dim]No completed todos to mark as pending.[/italic dim]", border_style="yellow"))
            return

        self.console.print("\n[bold magenta]✅ Completed Todos:[/bold magenta]")
        self.display_todos_table(completed_todos)

        todo_id_str = Prompt.ask("\n[bold]Enter ID of todo to mark as pending[/bold] 🆔")

        is_valid, error, todo_id = validate_todo_id(todo_id_str, self.storage)
        if not is_valid:
            self.console.print(f"[red]❌ {error}[/red]")
            return

        # Check if already pending
        todo = self.storage.get_by_id(todo_id)
        if todo.status == "pending":
            self.console.print(f"[yellow]⚠️  Todo #{todo_id} is already pending.[/yellow]")
            return

        # Show loading while processing
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(description="Updating your todo...", total=100)
            for i in range(100):
                progress.update(task, advance=1)

        success = incomplete_todo(self.storage, todo_id)
        if success:
            updated_todo = self.storage.get_by_id(todo_id)
            self.console.print(f"[green]✅ Todo #{todo_id} marked as pending![/green]")
            self.display_todos_table([updated_todo])
        else:
            self.console.print(f"[red]❌ Failed to update todo #{todo_id}[/red]")

    def update_todo_interactive(self):
        """Interactive update todo with validation"""
        self.console.clear()
        self.console.print(Panel("[bold cyan]✏️  Updating Todo[/bold cyan]", border_style="cyan"))

        todos = self.storage.get_all()
        if not todos:
            self.console.print(Panel("[italic dim]No todos to update.[/italic dim]", border_style="yellow"))
            return

        self.display_todos_table(todos)
        todo_id_str = Prompt.ask("\n[bold]Enter ID of todo to update[/bold] 🆔")

        is_valid, error, todo_id = validate_todo_id(todo_id_str, self.storage)
        if not is_valid:
            self.console.print(f"[red]❌ {error}[/red]")
            return

        todo = self.storage.get_by_id(todo_id)
        self.console.print(f"\n[bold cyan]Updating Todo #{todo.id}[/bold cyan]")
        self.console.print(f"[bold]Current title:[/bold] {todo.title}")
        self.console.print(f"[bold]Current description:[/bold] {todo.description}")

        # Get new title with validation
        new_title = Prompt.ask("[bold]Enter new title (leave blank to keep current)[/bold] 📝", default=todo.title)
        if new_title != todo.title:
            is_valid, error = validate_title(new_title)
            if not is_valid:
                self.console.print(f"[red]❌ {error}[/red]")
                return

        # Get new description with validation
        new_description = Prompt.ask("[bold]Enter new description (leave blank to keep current)[/bold] 💬", default=todo.description)
        if new_description != todo.description:
            is_valid, error = validate_description(new_description)
            if not is_valid:
                self.console.print(f"[red]❌ {error}[/red]")
                return

        # Check if any changes were made
        if new_title == todo.title and new_description == todo.description:
            self.console.print("[yellow]⚠️  No changes made.[/yellow]")
            return

        # Show loading while processing
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(description="Updating your todo...", total=100)
            for i in range(100):
                progress.update(task, advance=1)

        success = update_todo(self.storage, todo_id, new_title, new_description)
        if success:
            updated_todo = self.storage.get_by_id(todo_id)
            self.console.print(f"[green]✅ Todo #{todo_id} updated successfully![/green]")
            self.display_todos_table([updated_todo])
        else:
            self.console.print(f"[red]❌ Failed to update todo #{todo_id}[/red]")

    def delete_todo_interactive(self):
        """Interactive delete todo with confirmation"""
        self.console.clear()
        self.console.print(Panel("[bold red]🗑️  Deleting Todo[/bold red]", border_style="red"))

        todos = self.storage.get_all()
        if not todos:
            self.console.print(Panel("[italic dim]No todos to delete.[/italic dim]", border_style="yellow"))
            return

        self.display_todos_table(todos)
        todo_id_str = Prompt.ask("\n[bold]Enter ID of todo to delete[/bold] 🆔")

        is_valid, error, todo_id = validate_todo_id(todo_id_str, self.storage)
        if not is_valid:
            self.console.print(f"[red]❌ {error}[/red]")
            return

        todo = self.storage.get_by_id(todo_id)
        confirm = Confirm.ask(f"\n[bold red]Are you sure you want to delete todo #[/bold red][bold]{todo_id}[/bold][bold red]: '[/bold red][bold]{todo.title}[/bold][bold red]'?[/bold red]")

        if confirm:
            # Show loading while processing
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                task = progress.add_task(description="Deleting your todo...", total=100)
                for i in range(100):
                    progress.update(task, advance=1)

            success = delete_todo(self.storage, todo_id)
            if success:
                self.console.print(f"[green]✅ Todo #{todo_id} deleted successfully![/green]")
            else:
                self.console.print(f"[red]❌ Failed to delete todo #{todo_id}[/red]")
        else:
            self.console.print("[yellow]↩️  Deletion cancelled.[/yellow]")

    def run(self):
        """Run the interactive application with enhanced UX"""
        try:
            self.display_welcome()

            # Wait for user to press enter before showing menu
            self.console.print("\n[bold yellow]Press Enter to continue to the main menu...[/bold yellow]")
            Prompt.ask("")

            while True:
                self.display_menu()
                choice = Prompt.ask("\n[bold]Enter your choice[/bold] 🎯", choices=["1", "2", "3", "4", "5", "6", "7", "8"], default="8")

                if choice == "1":
                    self.add_todo_interactive()
                elif choice == "2":
                    self.list_todos_interactive()
                elif choice == "3":
                    self.complete_todo_interactive()
                elif choice == "4":
                    self.incomplete_todo_interactive()
                elif choice == "5":
                    self.update_todo_interactive()
                elif choice == "6":
                    self.delete_todo_interactive()
                elif choice == "7":
                    self.display_stats()
                elif choice == "8":
                    self.console.clear()
                    goodbye_ascii = pyfiglet.figlet_format("GOODBYE!", font="slant")
                    print(f"[bold red]{goodbye_ascii}[/bold red]")
                    self.console.print(Panel("[green bold]Thank you for using Todo Console App![/green bold]\n[cyan]Come back soon! 😊[/cyan]",
                                           title="[bold yellow]👋 See you later![/bold yellow]"))
                    break

                # Pause before returning to menu
                self.console.print("\n[bold yellow]Press Enter to return to main menu...[/bold yellow]")
                Prompt.ask("")

        except KeyboardInterrupt:
            self.console.clear()
            self.console.print("\n[bold red]👋 Goodbye![/bold red]")
        except Exception as e:
            self.console.print(f"[red]❌ An unexpected error occurred: {str(e)}[/red]")


def main():
    """Main entry point for the rich CLI"""
    app = RichTodoApp()
    app.run()


if __name__ == "__main__":
    main()