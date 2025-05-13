import csv
from pathlib import Path

# ─────────────────────────────────────────────────────────
# STORAGE SIMULATION
# ─────────────────────────────────────────────────────────
STORAGE_FILE_NAME = Path(__file__).parent / "students.csv"

# ─────────────────────────────────────────────────────────
# INFRASTRUCTURE
# ─────────────────────────────────────────────────────────






@property
def representation(self):
        return (
            "=========================\n"
            f"Student {self.name}\n"
            f"Marks: {self.marks}\n"
            f"Info: {self.info}\n"
            "=========================\n"
        )

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
                    row["marks"] = [int(mark) for mark in row["marks"].split(",")]
                    row["id"] = int(row["id"])
                    students.append(row)
        return students

    def save_storage(self):
        try:
            with open(self.file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["id", "name", "marks", "info"], delimiter=";")
                writer.writeheader()
                for student in self.students:
                    student_copy = student.copy()
                    student_copy["marks"] = ",".join(map(str, student_copy["marks"]))
                    writer.writerow(student_copy)
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")

    def add_student(self, student: dict):
        next_id = max([s["id"] for s in self.students], default=0) + 1
        student["id"] = next_id
        self.students.append(student)
        self.save_storage()

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
                student["marks"].append(mark)
                self.save_storage()
                return student
        return None


# ─────────────────────────────────────────────────────────
# DOMAIN (student, users, notification)
# ─────────────────────────────────────────────────────────
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
        print(
            "=========================\n"
            f"Student {student['name']}\n"
            f"Marks: {student['marks']}\n"
            f"Info: {student['info']}\n"
            "========================="
        )

    @inject_repository
    def add_student(self, student: dict, repo: Repository):
        if not student.get("name") or not student.get("marks"):
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


# ─────────────────────────────────────────────────────────
# OPERATIONAL (APPLICATION) LAYER
# ─────────────────────────────────────────────────────────
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
        "marks": [int(item) for item in raw_marks.replace(" ", "").split(",")],
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


# ─────────────────────────────────────────────────────────
# PRESENTATION LAYER
# ─────────────────────────────────────────────────────────
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


# ─────────────────────────────────────────────────────────
# ENTRYPOINT
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    handle_user_input()