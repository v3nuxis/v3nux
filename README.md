Lesson 7

Notification System in Python
Project Description
This project is a simple notification system that allows sending notifications to users with different roles (e.g., students and teachers). Notifications can be formatted based on the user's role and may include additional information, such as attachments.

The project demonstrates the use of:

Classes and inheritance.
String formatting methods.
Pattern matching with match-case (Python 3.10+).
Logging and data output.
Project Structure
The project consists of the following classes and functions:

1. Class Role
Defines user roles using an enumeration (enum.StrEnum):
STUDENT
TEACHER
2. Class User
Represents a user with the following attributes:
name — the user's name.
email — the user's email.
role — the user's role.
Includes the method send_notification, which sends a notification to the user. The notification can be printed to the console or logged, depending on the specified output method.
3. Class Notification
Represents a basic notification with the following attributes:
subject — the subject of the notification.
message — the main message of the notification.
attachment — an optional attachment (e.g., a file).
Includes the format method, which formats the notification into a readable string.
4. Subclasses of Notification
StudentNotification :
Adds the phrase "Sent via Student Portal" to the formatted message.
TeacherNotification :
Adds the phrase "Teacher's Desk Notification" to the formatted message.
5. Function main
Demonstrates the functionality of the system by:
Creating users with different roles.
Creating notifications for students and teachers.
Sending notifications to users.
6. Sending notifications...
Notification for noname (STUDENT):
Subject: Python
Message: Don't forget to submit your homework before Thursday!
Attachment: homework.py
Sent via Student Portal

Notification for Zahar cramble cookie (TEACHER):
Subject: Meeting;Python
Message: Python Course.
Teacher's Desk Notification