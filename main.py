import typer
from rich.console import Console
from rich.table import Table
import dateparser
import database

app = typer.Typer(help="Smart To-Do List Application")
console = Console()

def parse_date(date_string):
    if not date_string:
        return None
    GLOBAL_LANGS = ['en', 'hi', 'bn', 'ta', 'te', 'mr', 'gu', 'kn', 'ml', 'pa', 'ur', 'fr', 'de', 'it', 'es', 'ja', 'zh']
    # Use dateparser to magically find the date based on natural language
    parsed = dateparser.parse(date_string, languages=GLOBAL_LANGS)
    if parsed:
        return parsed.strftime("%Y-%m-%d %H:%M")
    return None

def get_priority_color(priority):
    if priority.lower() == 'high':
        return "red"
    elif priority.lower() == 'medium':
        return "yellow"
    else:
        return "green"

def get_status_icon(status):
    if status.lower() == 'completed':
        return "[green]✓[/green]"
    return "[red]✗[/red]"

@app.command()
def add(
    description: str, 
    due: str = typer.Option(None, help="Natural language due date (e.g., 'tomorrow at 5pm')"), 
    priority: str = typer.Option("Medium", help="Priority: High, Medium, Low")
):
    """Add a new task."""
    due_date = parse_date(due) if due else None
    
    if due and not due_date:
        console.print(f"[bold red]Error:[/bold red] Could not understand the due date '{due}'")
        raise typer.Exit(code=1)
        
    task_id = database.add_task(description, due_date, priority.capitalize())
    console.print(f"[bold green]Task added[/bold green] (ID: {task_id})")

@app.command()
def list(all: bool = typer.Option(False, "--all", "-a", help="Show all tasks, including completed ones")):
    """List tasks. Shows pending tasks by default."""
    status = None if all else "Pending"
    tasks = database.get_tasks(status)
    
    if not tasks:
        console.print("[dim]No tasks found.[/dim]")
        return
        
    table = Table(title="To-Do List")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    table.add_column("Due Date", style="blue")
    table.add_column("Priority")
    table.add_column("Status", justify="center")
    
    for task in tasks:
        priority_color = get_priority_color(task['priority'])
        status_icon = get_status_icon(task['status'])
        due_str = task['due_date'] if task['due_date'] else "-"
        
        table.add_row(
            str(task['id']),
            task['description'],
            due_str,
            f"[{priority_color}]{task['priority']}[/{priority_color}]",
            status_icon
        )
        
    console.print(table)

@app.command()
def done(task_id: int):
    """Mark a task as completed."""
    database.complete_task(task_id)
    console.print(f"[bold green]Task {task_id} marked as completed![/bold green]")

@app.command()
def delete(task_id: int):
    """Delete a task."""
    database.delete_task(task_id)
    console.print(f"[bold yellow]Task {task_id} deleted.[/bold yellow]")

@app.command()
def search(keyword: str):
    """Search for tasks by keyword."""
    tasks = database.search_tasks(keyword)
    
    if not tasks:
        console.print(f"[dim]No tasks found matching '{keyword}'.[/dim]")
        return
        
    table = Table(title=f"Search Results for '{keyword}'")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    table.add_column("Due Date", style="blue")
    table.add_column("Priority")
    table.add_column("Status", justify="center")
    
    for task in tasks:
        priority_color = get_priority_color(task['priority'])
        status_icon = get_status_icon(task['status'])
        due_str = task['due_date'] if task['due_date'] else "-"
        
        table.add_row(
            str(task['id']),
            task['description'],
            due_str,
            f"[{priority_color}]{task['priority']}[/{priority_color}]",
            status_icon
        )
        
    console.print(table)

@app.command()
def edit(
    task_id: int, 
    desc: str = typer.Option(None, "--desc", "-d", help="New description"),
    due: str = typer.Option(None, "--due", "-t", help="New natural language due date"),
    priority: str = typer.Option(None, "--priority", "-p", help="New Priority: High, Medium, Low")
):
    """Edit an existing task."""
    due_date = parse_date(due) if due else None
    
    if due and not due_date:
        console.print(f"[bold red]Error:[/bold red] Could not understand the due date '{due}'")
        raise typer.Exit(code=1)
        
    prio = priority.capitalize() if priority else None
    
    database.edit_task(task_id, description=desc, due_date=due_date, priority=prio)
    console.print(f"[bold green]Task {task_id} updated![/bold green]")

@app.command()
def daemon():
    """Start the background notification daemon to receive alarms."""
    import notifier
    notifier.run_daemon()

if __name__ == "__main__":
    app()
