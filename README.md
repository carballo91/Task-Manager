# Task Manager Application

## Overview

This Task Manager application is a command-line interface (CLI) tool designed to help users manage their daily tasks efficiently. It is built using Python and makes use of several third-party libraries like `csv`, `pyfiglet`, `rich`, and `plyer` to enhance functionality and user experience. Tasks are stored in a CSV file, making it easy to read, write, and manipulate task data over time. The app supports features like adding tasks, updating tasks, and notifying users of upcoming deadlines.

## Features

- **Task Management**: Users can create, view, update, and delete tasks.
- **CSV-based Storage**: Tasks are stored in a CSV file, making data easy to manage.
- **Task Deadline Tracking**: The app automatically calculates the number of days remaining for each task.
- **Customizable File Path**: Users can specify a custom CSV file for storing tasks.
- **Rich Console Output**: The application uses the `rich` library for a visually appealing command-line experience, including colored text, tables, and panels.
- **Notifications**: Integrated with `plyer`, the app provides desktop notifications for upcoming tasks.
- **Error Handling**: The app has built-in mechanisms to handle missing files and other exceptions gracefully.

### Required Dependencies:
- **` Python 3.6+`**
- **` pyfiglet`**
- **` rich`**
- **` plyer`**

## How to Use
### Clone the Repository
First, clone this repository to your local machine:

```bash
git clone https://github.com/carballo91/Task-Manager.git
cd Task-Manager
```

### Set Up a Virtual Environment

It is recommended to use a virtual environment to manage dependencies. Create and activate a virtual environment using the following commands:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
### Requirements

To run this project, you'll need the dependencies listed in the `requirements.txt` file. You can install them using the following command:

```bash
pip install -r requirements.txt
```

### Run the Application
To start the task manager, run:

```bash
python main.py
```
This will launch the application and provide you with an interactive interface for managing tasks.

### Add a Task
Follow the prompts to enter details such as task description, due date, and more.

### View Tasks
The application will display tasks in a visually appealing table format, showing the task ID, description, creation date, due date, and the number of days remaining until the deadline.

### Update Tasks
You can update existing tasks, including changing the description, due date, or status.

### Delete a Task
To delete a task, simply enter the task ID and confirm the deletion.

## Testing

The project includes a test_main.py file for testing the functionality of the task manager. To run the tests, you can use pytest, which is a testing framework for Python.

To install pytest:

```bash
pip install pytest
```
### Running Tests
To run the tests, execute the following command from the project directory:

```bash
pytest test_main.py
```
This will run all the unit tests defined in test_main.py, ensuring that the key functions of the Task Manager work as expected.

## File Structure
```bash
├── main.py             # Main script to run the Task Manager
├── tasks1.csv          # Default CSV file for storing tasks
├── README.md           # Project documentation
├── requirements.txt    # List of dependencies
├── test_main.py        # Tests for main.py

```
## Methods and Functionality
### TaskManager Class
- def __init__(self, file="tasks1.csv"):
    
    Initializes the Task Manager with the default CSV file. If the file does not exist, it creates one. It also checks if the file is empty and initializes a list of field names for the CSV.
- def remaining_days(self):
    
    Calculates the number of days left to complete each task based on the due date.
- def add_task(self, description, due_date):
    
    Adds a new task to the CSV file. It automatically generates a unique task ID and calculates the number of days to finish the task.
- def delete_task(self, id):
    
    Deletes a task from the CSV file based on the task ID.
- def view(self):
   
    Displays all tasks in a table format using the rich library.
- def task_notification(self):
    
    Sends a desktop notification to remind users of upcoming tasks using the plyer library.

## Error Handling
This application includes robust error handling to manage issues like:

- FileNotFoundError: If the specified file is missing, the program will gracefully exit with a helpful error message.
- Invalid Date Format: When entering dates, the program will validate input and prompt the user for correct date formatting.
- CSV Parsing Errors: The app can handle corrupted CSV data by skipping over problematic entries and continuing normal operation.