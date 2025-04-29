Lesson 2

Code Overview
This application is designed to manage student data. It provides commands for interacting with a list of students, which is stored in a JSON file. Here’s a breakdown of the main functionality:

Load student data from a JSON file:

When the program starts, it attempts to load student data from a file called students.json.

If the file is not found or is corrupted, it uses a set of default students.

Add new students:

You can add new students to the system by entering their name and marks in the format: Name;marks, where the marks are separated by commas.

After a new student is added, the data is saved to the students.json file.

Show student data:

The application can display all the students currently in the storage.

Search for a student by ID:

You can search for a student by their unique ID. If the student is found, their information is displayed.

JSON File Handling
The student data is saved and loaded from a file called students.json. The file is used to persist the data, so when the application is restarted, it can still access the previous data.

Default data: If the students.json file is not found or is corrupted, the application will use default student data. This is stored in the default_students list.

Saving data: Every time a new student is added to the list, the updated list of students is saved back to the students.json file, ensuring that data persists between sessions.

File structure: The students.json file contains a list of student records. Each record is a dictionary with:

id: A unique identifier for each student.

name: The student's full name.

marks: A list of marks (scores) for that student.

info: Additional information about the student.

from: The location the student is from (e.g., "USA.New York").

How the Program Works:
Loading Data:

When you start the program, it calls the load_storage_from_file() function.

This function attempts to open and read the students.json file. If the file exists and is valid, the data is loaded into the storage variable. If the file doesn’t exist or is corrupted, the program will use the default_students list instead.

Adding a Student:

You can add a student by entering the command add and providing the data in the format: Name;marks, where the marks are separated by commas.

Once the student is added, the storage list is updated, and the new list is saved back into the students.json file using the save_storage_to_file() function.

Displaying Students:

The show command displays all the students in the system.

Searching for a Student:

You can search for a student by their ID using the search command. If a student with the provided ID exists, their details will be displayed.
