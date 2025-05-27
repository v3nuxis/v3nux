## Lesson 10


Knowledge Base\
Overview\
The Digital Journal Application is designed to manage student data, including their grades and additional information. It also provides analytical reports and sends them via email on a daily, monthly, and yearly basis. The application is built with modularity and asynchronous processing in mind, ensuring scalability and efficiency.

Key Features
Student Management:
Add new students with names, grades, and additional information.
Search for students by ID.
Update student details (name, information).
Delete students.
Add grades to students, with each grade timestamped to the current date.
Analytics:
Calculate the total number of students.
Compute the average grade for a specific day (only grades from that day are included).
Automated Reporting:
Daily reports:
Average grade for the day.
Total number of students.
Monthly reports:
Total number of students.
Yearly reports:
Total number of students for the entire year.
Asynchronous Email Delivery:
Reports are sent asynchronously to avoid blocking the main application flow.
Emails are sent to a predefined admin address (admin@example.com).
Technical Details
Data Storage:
Student data is stored in a students.csv file.
Each grade is saved with a creation date in the format YYYY-MM-DD.
Asynchronous Processing:
The asyncio library is used to schedule tasks for sending reports.
Email delivery is handled asynchronously using the smtplib library.
Modular Design:
The application is divided into several layers:
Infrastructure: Handles data storage (Repository class).
Domain Logic: Manages student data and analytics (StudentService, Analytics classes).
User Interface: Provides a console-based interface for user interaction (handle_user_input function).
Reporting: Asynchronous tasks for daily, monthly, and yearly reports.
Scalability:
The modular architecture allows for easy addition of new features or modifications to existing ones.
How to Use the Application
Launching the Application:
Run the work.py file.
A welcome message will display the available commands.
Available Commands:
show: Display all students.
add: Add a new student.
search: Find a student by ID.
delete: Remove a student.
update: Update student details.
add_mark: Add a grade to a student.
help: Display available commands.
quit: Exit the application.
Automated Reports:
Daily, monthly, and yearly reports are sent to admin@example.com.
Reports include analytical data such as:
Average grade for the day.
Total number of students.
Example Usage
Adding a Student:
Input format: John Doe;1,2,3,4,5
Where John Doe is the name, and [1,2,3,4,5] are the grades.
Adding a Grade:
Enter the student ID and the grade.
