import csv
from pathlib import Path
from datetime import datetime
import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

STORAGE_FILE_NAME = Path(__file__).parent / "students.csv"

class Repository:
    def __init__(self):
        self.file_path = STORAGE_FILE_NAME
        self.students = self.load_storage()

    def load_storage(self):
        students = []
        if self.file_path.exists():
            with open(self.file_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file, delimiter=";")
                for row in reader:
                    try:
                        raw_marks = row["marks"].split("|")
                        row["marks"] = []
                        for mark in raw_marks:
                            if ":" in mark:
                                row["marks"].append(
                                    {"mark": int(mark.split(":")[0]), "creation_date": mark.split(":")[1]})
                            else:
                                row["marks"].append(
                                    {"mark": int(mark), "creation_date": datetime.now().strftime("%Y-%m-%d")})
                        row["id"] = int(row["id"])
                        students.append(row)
                    except Exception as e:
                        print(f"Ошибка при загрузке данных для студента {row.get('name', 'UNKNOWN')}: {e}")
        return students

    def save_storage(self):
        try:
            with open(self.file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["id", "name", "marks", "info"], delimiter=";")
                writer.writeheader()
                for student in self.students:
                    student_copy = student.copy()
                    student_copy["marks"] = "|".join(
                        [f"{mark['mark']}:{mark['creation_date']}" for mark in student_copy["marks"]]
                    )
                    writer.writerow(student_copy)
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")

    def add_student(self, student: dict):
        next_id = max([s["id"] for s in self.students], default=0) + 1
        student["id"] = next_id
        student["marks"] = []
        self.students.append(student)
        self.save_storage()
        return student

    def get_student(self, id_: int):
        for student in self.students:
            if student["id"] == id_:
                return student
        return None

    def update_student(self, id_: int, data: dict):
        for student in self.students:
            if student["id"] == id_:
                student.update(data)
                self.save_storage()
                return student
        return None

    def delete_student(self, id_: int):
        self.students = [s for s in self.students if s["id"] != id_]
        self.save_storage()

    def add_mark(self, id_: int, mark: int):
        for student in self.students:
            if student["id"] == id_:
                student["marks"].append({"mark": mark, "creation_date": datetime.now().strftime("%Y-%m-%d")})
                self.save_storage()
                return student
        return None

class AnalyticsService:
    def __init__(self, repository: Repository):
        self.repository = repository

    def calculate_total_students(self) -> int:
        return len(self.repository.students)

    def calculate_daily_average_marks(self, date: str) -> float:
        total_marks = 0
        total_count = 0
        for student in self.repository.students:
            for mark in student["marks"]:
                if mark["creation_date"] == date:
                    total_marks += mark["mark"]
                    total_count += 1
        return total_marks / total_count if total_count > 0 else 0

class EmailService:
    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    async def send_email(self, recipient_email: str, subject: str, body: str):
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            print("Email отправлен успешно!")
        except Exception as e:
            print(f"Ошибка при отправке email: {e}")

async def daily_report_task(analytics_service: AnalyticsService, email_service: EmailService):
    while True:
        today = datetime.now().strftime("%Y-%m-%d")
        average_mark = analytics_service.calculate_daily_average_marks(today)
        total_students = analytics_service.calculate_total_students()
        subject = f"Ежедневный отчет за {today}"
        body = f"Средняя оценка за день: {average_mark}\nОбщее количество студентов: {total_students}"
        await email_service.send_email("admin@example.com", subject, body)
        await asyncio.sleep(86400)

async def monthly_report_task(analytics_service: AnalyticsService, email_service: EmailService):
    while True:
        today = datetime.now().strftime("%Y-%m")
        total_students = analytics_service.calculate_total_students()
        subject = f"Ежемесячный отчет за {today}"
        body = f"Общее количество студентов: {total_students}"
        await email_service.send_email("admin@example.com", subject, body)
        await asyncio.sleep(2592000)

async def year_report_task(analytics_service: AnalyticsService, email_service: EmailService):
    while True:
        today = datetime.now().strftime("%Y")
        total_students = analytics_service.calculate_total_students()
        subject = f"Ежегодный отчет за {today}"
        body = f"Общее количество студентов за весь год учебы: {total_students}"
        await email_service.send_email("admin@example.com", subject, body)
        await asyncio.sleep(31556926)

class StudentService:
    def __init__(self):
        self.repository = Repository()

    @staticmethod
    def inject_repository(func):
        def inner(*args, **kwargs):
            repo = Repository()
            return func(*args, repo=repo, **kwargs)
        return inner

    @inject_repository
    def show_students(self, repo: Repository):
        print("=========================")
        for student in repo.students:
            print(f"{student['id']}. Student {student['name']}")
        print("=========================")

    def show_student(self, student: dict):
        print("=========================")
        print(f"Student {student['name']}")
        print(f"Marks: {student['marks']}")
        print(f"Info: {student['info']}")
        print("=========================")

    @inject_repository
    def add_student(self, student: dict, repo: Repository):
        if not student.get("name"):
            return None
        repo.add_student(student)
        return student

    @inject_repository
    def update_student(self, id_: int, raw_input: str, repo: Repository):
        parsing_result = raw_input.split(";")
        if len(parsing_result) != 2:
            return None
        new_name, new_info = parsing_result
        data = {"name": new_name, "info": new_info}
        return repo.update_student(id_, data)

    @inject_repository
    def delete_student(self, id_: int, repo: Repository):
        repo.delete_student(id_)

    @inject_repository
    def add_mark(self, id_: int, mark: int, repo: Repository):
        repo.add_mark(id_, mark)

def ask_student_payload() -> dict:
    ask_prompt = (
        "Введите данные студента в формате: "
        "John Doe;1,2,3,4,5\n"
        "где 'John Doe' — имя, а [1,2,3,4,5] — оценки.\n"
        "Данные должны быть разделены ';'.\n"
    )
    user_data = input(ask_prompt)
    name, raw_marks = user_data.split(";")
    return {
        "name": name.strip(),
        "marks": [{"mark": int(item), "creation_date": datetime.now().strftime("%Y-%m-%d")} for item in
                  raw_marks.replace(" ", "").split(",")],
        "info": "",
    }

def student_management_command_handle(command: str):
    student_service = StudentService()
    if command == "show":
        student_service.show_students()
    elif command == "add":
        data = ask_student_payload()
        student = student_service.add_student(data)
        if student:
            print(f"Студент {student['name']} успешно добавлен.")
        else:
            print("Ошибка при добавлении студента.")
    elif command == "search":
        student_id = input("Введите ID студента: ")
        if not student_id.isdigit():
            print("ID должен быть числом.")
            return
        student = student_service.get_student(int(student_id))
        if student:
            student_service.show_student(student)
        else:
            print(f"Студент с ID {student_id} не найден.")
    elif command == "delete":
        student_id = input("Введите ID студента для удаления: ")
        if not student_id.isdigit():
            print("ID должен быть числом.")
            return
        student_service.delete_student(int(student_id))
        print(f"Студент с ID {student_id} удален.")
    elif command == "update":
        student_id = input("Введите ID студента для обновления: ")
        if not student_id.isdigit():
            print("ID должен быть числом.")
            return
        print("Введите новые данные в формате: Имя;Информация")
        user_input = input("Введите: ")
        updated_student = student_service.update_student(int(student_id), user_input)
        if updated_student:
            print(f"Данные студента {updated_student['name']} обновлены.")
        else:
            print("Ошибка при обновлении данных.")
    elif command == "add_mark":
        student_id = input("Введите ID студента: ")
        mark = input("Введите оценку: ")
        if not student_id.isdigit() or not mark.isdigit():
            print("ID и оценка должны быть числами.")
            return
        student_service.add_mark(int(student_id), int(mark))
        print(f"Оценка добавлена студенту с ID {student_id}.")

def handle_user_input():
    OPERATIONAL_COMMANDS = ("quit", "help")
    STUDENT_MANAGEMENT_COMMANDS = ("show", "add", "search", "delete", "update", "add_mark")
    AVAILABLE_COMMANDS = (*OPERATIONAL_COMMANDS, *STUDENT_MANAGEMENT_COMMANDS)
    HELP_MESSAGE = (
        "Добро пожаловать в журнал 'Сквазимабзабзаб'! Используйте меню для взаимодействия с приложением.\n"
        f"Доступные команды: {AVAILABLE_COMMANDS}"
    )
    print(HELP_MESSAGE)
    while True:
        command = input("\nВведите команду: ").strip().lower()
        if command == "quit":
            print("Спасибо за использование журнала!")
            break
        elif command == "help":
            print(HELP_MESSAGE)
        elif command in STUDENT_MANAGEMENT_COMMANDS:
            student_management_command_handle(command)
        else:
            print("Неизвестная команда. Введите 'help' для просмотра доступных команд.")


def send_test_email():
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"
    recipient_email = "recipient_email@example.com"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Test Email"
    message.attach(MIMEText("This is a test email.", "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print("Test email sent successfully!")
    except Exception as e:
        print(f"Error sending test email: {e}")

send_test_email()

async def tasks():
    repository = Repository()
    analytics_service = AnalyticsService(repository)
    email_service = EmailService(
        smtp_server="smtp.example.com",
        smtp_port=587,
        sender_email="admin@gmail.com",
        sender_password="123456789"
    )

    await asyncio.gather(
        daily_report_task(analytics_service, email_service),
        monthly_report_task(analytics_service, email_service),
        year_report_task(analytics_service, email_service)
    )

if __name__ == "__main__":
    asyncio.run(tasks())