import csv
import sys
import os
import re
import time
from pyfiglet import Figlet, figlet_format
from datetime import date, datetime
from plyer import notification
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel

console = Console()


class TaskManager:
    def __init__(self, file="tasks1.csv"):
        # CSV file
        self.file = file
        # Checks if file/path exists and if file is empty
        if not os.path.exists(self.file):
            try:
                with open(self.file, "w", newline="") as file:
                    pass
            except Exception as e:
                self.__handle_exception(e)
        self.file_isempty = os.stat(self.file).st_size == 0

        # Sets headers for the CSV file
        self._fieldnames = [
            "ID",
            "Description",
            "Created On",
            "Due Date",
            "Days To Finish",
        ]
        self._id = self.get_last_task_id()

    def __str__(self):
        return f"Name of file is {self.file.split(".")[0]}"

    # Method that handles file errors
    def __handle_exception(self, exception):
        if isinstance(exception, FileNotFoundError):
            sys.exit("File or directory not found")
        sys.exit(f"An unexpected error occurred {exception}")

    # Updates number of days left to finish a task
    def remaining_days(self):
        try:
            # Reads CSV file and fill tasks list with data if any
            with open(self.file) as file:
                reader = csv.DictReader(file)
                tasks = [
                    {
                        **row,
                        "Days To Finish": (
                            datetime.strptime(row["Due Date"], "%Y-%m-%d").date()
                            - date.today()
                        ).days,
                    }
                    for row in reader
                ]
            # If tasks are empty skips the writing to file
            if tasks:
                # Opens file and writes to file with updated data
                with open(self.file, "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=self._fieldnames)
                    writer.writeheader()
                    for task in tasks:
                        writer.writerow(task)
        except Exception as e:
            self.__handle_exception(e)

    # Gets the id of the last task in the csv file
    def get_last_task_id(self):
        try:
            id = 0
            if not self.file_isempty:
                with open(self.file) as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        id = row["ID"]
            return int(id)
        except Exception as e:
            self.__handle_exception(e)

    # Method that creates tasks to file
    def add_task(self, description, due_date):
        # Substracts due date with current date
        days_remaining = (due_date - date.today()).days
        try:
            with open(self.file, "a") as file:
                writer = csv.DictWriter(file, fieldnames=self._fieldnames)
                if self.file_isempty:
                    writer.writeheader()
                # Add new task to csv file
                writer.writerow(
                    {
                        "ID": self._id + 1,
                        "Description": description,
                        "Created On": date.today(),
                        "Due Date": due_date,
                        "Days To Finish": days_remaining,
                    }
                )
                console.print("New Task Added!", style="Green")
        except Exception as e:
            self.__handle_exception(e)

    # Deletes tasks by id
    def delete_task(self, id):
        try:
            with open(self.file) as file:
                reader = csv.DictReader(file)
                # Stores tasks except for the task to be deleted
                tasks = []
                for row in reader:
                    if row["ID"] != str(id):
                        row["ID"] = len(tasks) + 1
                        tasks.append(row)
            with open(self.file, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self._fieldnames)
                writer.writeheader()
                # Writes the tasks not deleted back into csv file
                writer.writerows(tasks)
            console.print("Task deleted succesfully\n", style="green")
            time.sleep(1)
        except Exception as e:
            self.__handle_exception(e)

    # Edit tasks by id
    def edit_task(self, id, description, due_date):
        try:
            with open(self.file) as file:
                reader = csv.DictReader(file)
                # Updates task description, due date and id and it stored in tasks
                if due_date is None:
                    tasks = [
                        (
                            {**row, "Description": description}
                            if row["ID"] == str(id)
                            else row
                        )
                        for row in reader
                    ]
                else:
                    tasks = [
                        (
                            {**row, "Description": description, "Due Date": due_date}
                            if row["ID"] == str(id)
                            else row
                        )
                        for row in reader
                    ]

            with open(self.file, "w", newline="") as file:
                writer = csv.DictWriter(file, self._fieldnames)
                writer.writeheader()
                # Writes the updated tasks into the csv file
                writer.writerows(tasks)
            console.print("Task edited successfully\n", style="green")
            time.sleep(1)
        except Exception as e:
            self.__handle_exception(e)

    # View all tasks in file
    def view(self):
        try:
            with open(self.file) as file:
                reader = csv.DictReader(file)
                table = Table(show_header=True, header_style="bold magenta")
                headers = reader.fieldnames
                for header in headers:
                    table.add_column(header)

                for row in reader:
                    table.add_row(
                        row["ID"],
                        row["Description"],
                        row["Created On"],
                        row["Due Date"],
                        f'{row["Days To Finish"]} days',
                    )
                console.print(table)
                # tasks = [{**row, "Days To Finish":f'{row["Days To Finish"]} days'} for row in reader]
                # print()
                # print(tabulate(tasks, headers="keys",tablefmt="fancy_grid"))
        except Exception as e:
            self.__handle_exception(e)

    # Sorts tasks by Days to finish in ascending order
    def sorted_view(self):
        try:
            with open(self.file) as file:
                reader = csv.DictReader(file)
                table = Table(show_header=True, header_style="bold magenta")
                headers = reader.fieldnames
                for header in headers:
                    table.add_column(header)
                tasks = [
                    {**row, "Days To Finish": f'{row["Days To Finish"]} days'}
                    for row in sorted(
                        reader, key=lambda days: int(days["Days To Finish"])
                    )
                ]
                for row in tasks:
                    table.add_row(
                        row["ID"],
                        row["Description"],
                        row["Created On"],
                        row["Due Date"],
                        row["Days To Finish"],
                    )
                console.print(table)
        except Exception as e:
            self.__handle_exception(e)

    # Asks user for a valid task id
    def get_task_id(self):
        while True:
            try:
                id = int(console.input("\n[cyan]Choose a task ID: [/cyan]"))
                if 0 < id <= self._id:
                    return id
                raise ValueError
            except ValueError:
                console.print("Please enter a valid id number", style="red")
                continue

    def task_notification(self):
        try:
            with open(self.file) as file:
                reader = csv.DictReader(file)
                tasks = [
                    {**row} for row in reader if 0 <= int(row["Days To Finish"]) < 2
                ]
                file.seek(0)
                reader = csv.DictReader(file)
                expired = [{**row} for row in reader if int(row["Days To Finish"]) < 0]
        except Exception as e:
            self.__handle_exception(e)
        for row in tasks:
            notification.notify(
                title=row["Description"],
                message=f"It expires in {row["Days To Finish"]} days, make sure to finish",
                timeout=1,
            )
        for row in expired:
            # print(f"\n{row["Description"]} is past its due date {row["Due Date"]}, please delete the task")
            console.print(
                f"[red]{row["Description"]}[/red] is past its due date [red]{row["Due Date"]}[/red], please delete the task"
            )


# Formats date (YYYY-MM-DD)
def format_date(d):
    try:
        f_date = datetime.strptime(d, "%Y-%m-%d").date()
        if f_date < date.today():
            console.print("Date cannot be before today", style="red")
            return False
        return f_date
    except ValueError:
        console.print(
            "Invalid date format. Please enter date in this format: '2024-12-31' ",
            style="red",
        )
        return False


# Validates strings so they cannot be empty
def validate_strings(str):
    pattern = r"^[^ \n].*"
    match = re.search(pattern, str)
    return True if match else False


# Asks user for task description until validated
def get_task_description():
    description = console.input("\n[cyan]Task Description: [/cyan]").strip()
    while not validate_strings(description):
        console.print("Please enter a task description", style="red")
        description = console.input("\n[cyan]Task Description: [/cyan]").strip()
    return description


# Asks user for date until validated
def get_date():
    d_date = console.input("\n[cyan]Due Date (YYYY-MM-DD): [/cyan]")
    while not format_date(d_date):
        d_date = console.input("\n[cyan]Due Date (YYYY-MM-DD): [/cyan]")
    return format_date(d_date)


# Function to get menu options
def main_menu(options):
    for i, option in enumerate(options, 1):
        text_option = Text(str(i) + " " + option, style="bold white")
        console.print(text_option)


# Function to get menu border
def menu_border(width, char="*"):
    if isinstance(char, int):
        char = "*"
    return char * width


def main():
    # Create a figlet object
    f = Figlet(width=150)

    # Get the width of the text created by figlet
    lines = f.renderText("Task Manager").splitlines()
    width = max(len(line) for line in lines)

    # Prints the stylized name of the app and creates border on top and bottom
    console.print(menu_border(width), style="cyan")
    ascii_art = figlet_format("Task Manager")
    styled_title = Text(ascii_art, style="bold bright_cyan")
    console.print(styled_title)
    console.print(menu_border(width), style="cyan")

    # Menu options
    options = ["Add Task", "Delete Task", "Edit Task", "View Tasks", "Exit"]
    # Create TaskManager object
    task_manager = TaskManager()
    # Notifies user of tasks that have 0 or 1 day left
    task_manager.task_notification()

    while True:
        # Updates remaining days of a task everytime the program starts
        task_manager.remaining_days()
        # Menu title
        menu_title = Text("Main Menu", style="bold bright_cyan")
        # Display menu title
        console.print(Panel(menu_title))
        # Prints menu
        main_menu(options)

        while True:
            try:
                option = int(
                    console.input("[bold cyan]\nChoose an option: [/bold cyan]")
                )
                if 1 <= option <= len(options):
                    break
                raise ValueError
            except ValueError:
                console.print("Please enter a valid option", style="red")
                continue

        # Option to add tasks
        if option == 1:
            # Display add task title
            add_task = Text("Add Task", style="bold bright_cyan")
            console.print(Panel(add_task))

            description = get_task_description()

            due_date = get_date()

            task_manager.add_task(description, due_date)
        # Option to delete tasks
        elif option == 2:
            if task_manager._id == 0:
                print("No tasks in file")
                time.sleep(1)
                continue

            # Display delete task title
            delete_task = Text("Delete Task", style="bold bright_cyan")
            console.print(Panel(delete_task))

            task_manager.view()

            id = task_manager.get_task_id()

            task_manager.delete_task(id)
        # Option to edit tasks
        elif option == 3:
            if task_manager._id == 0:
                print("No tasks in file")
                time.sleep(1)
                continue

            # Display edit task title
            edit_task = Text("Edit Task", style="bold bright_cyan")
            console.print(Panel(edit_task))

            task_manager.view()

            id = task_manager.get_task_id()

            description = get_task_description()

            while True:
                change_date = console.input(
                    "\n[cyan]Would you like to change the date? y/n [/cyan]"
                ).lower()
                if change_date != "y" and change_date != "n":
                    console.print("Please enter y or n", style="red")
                    continue
                if change_date == "y":
                    due_date = get_date()
                else:
                    due_date = None
                break

            task_manager.edit_task(id, description, due_date)
        # Option to view tasks
        elif option == 4:
            if task_manager._id == 0:
                print("No tasks in file")
                time.sleep(1)
                continue
            # Display view tasks title
            view_tasks = Text("View Tasks", style="bold bright_cyan")
            console.print(Panel(view_tasks))

            task_manager.view()
            sort_view = console.input(
                "\n[cyan]Would you like to sort your tasks by Days to finish? y/n [/cyan]"
            ).lower()
            while sort_view != "y" and sort_view != "n":
                console.print("Please enter y or n", style="red")
                sort_view = console.input(
                    "\n[cyan]Would you like to sort your tasks by Days to finish? y/n [/cyan]"
                ).lower()
            if sort_view == "y":
                task_manager.sorted_view()

            console.input("[cyan]Press any key to go back to menu[/cyan] ")
            time.sleep(1)
        # Option to exit application
        elif option == 5:
            console.print("Thanks for using Task Manager!", style="green")
            sys.exit(1)


if __name__ == "__main__":
    main()
