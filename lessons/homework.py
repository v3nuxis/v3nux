import enum
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Role(enum.StrEnum):
    STUDENT = enum.auto()
    TEACHER = enum.auto()

class User:
    def __init__(self, name: str, email: str, role: Role) -> None:
        self.name = name
        self.email = email
        self.role = role

    def send_notification(self, notification, output_method="print"):
        formatted_message = notification.format()
        match output_method:
            case "print":
                print(f"Notification for {self.name} ({self.role}):\n{formatted_message}")
            case "log":
                logging.info(f"Notification for {self.name} ({self.role}):\n{formatted_message}")
            case _:
                raise ValueError(f"Unknown output method: {output_method}")

class Notification:
    def __init__(self, subject: str, message: str, attachment: str = "") -> None:
        self.subject = subject
        self.message = message
        self.attachment = attachment

    def format(self) -> str:
        formatted_message = f"Subject: {self.subject}\nMessage: {self.message}"
        if self.attachment:
            formatted_message += f"\nAttachment: {self.attachment}"
        return formatted_message

class StudentNotification(Notification):
    def format(self) -> str:
        base_message = super().format()
        return f"{base_message}\nSent via Student Portal"

class TeacherNotification(Notification):
    def format(self) -> str:
        base_message = super().format()
        return f"{base_message}\nTeacher's Desk Notification"

def main():
    student = User(name="noname", email="noname@email.com", role=Role.STUDENT)
    teacher = User(name="Zahar cramble cookie", email="example@example.com", role=Role.TEACHER)

    student_notification = StudentNotification(
        subject="Python",
        message="Don't forget to submit your homework before Thursday!",
        attachment="homework.py"
    )
    teacher_notification = TeacherNotification(
        subject="Meeting;Python",
        message="Python Course."
    )

    print("Sending notifications...")
    student.send_notification(student_notification, output_method="print")
    teacher.send_notification(teacher_notification, output_method="print")

if __name__ == "__main__":
    main()