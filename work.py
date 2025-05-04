import json

STORAGE_FILE = "students.json"

default_students = []

storage = {}


def load_storage_from_file():
    global storage
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            storage = {student['id']: student for student in data}
    except (FileNotFoundError, json.JSONDecodeError):
        storage = {student['id']: student for student in default_students}


def save_storage_to_file():
    data = list(storage.values())
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def add_student(student: dict) -> bool:
    if not student.get("name") or not student.get("marks"):
        return False

    next_id = max(storage, key=operator.itemgetter("id"))["id"] + 1
    student["id"] = next_id
    storage[new_id] = student
    save_storage_to_file()
    return True


def add_mark(id_: int, mark: int) -> bool:
    if id_ not in storage:
        return False
    storage[id_]['marks'].append(mark)
    save_storage_to_file()
    return True


def show_students():
    print("=========================")
    if not storage:
        print("No students found")
        return
    for student_id in sorted(storage.keys()):
        student = storage[student_id]
        avg = sum(student['marks']) / len(student['marks'])
        print(f"{student_id}. {student['name']} | Avg: {avg:.1f} Info: {'info'})
    print("=========================")


def show_student(student: dict):
    if not student:
        return
    print(f"""
=========================
Name: {student['name']}
Marks: {student['marks']}
Info: {student.get('info', 'No info')}
=========================
""")


def ask_student_payload() -> dict:
    while True:
        try:
            data = input("Введите студента (имя;оценки;[инфо]): ").strip()
            parts = data.split(';')
            if len(parts) < 2:
                raise ValueError("Нужно минимум имя и оценки")

            name = parts[0].strip()
            marks = [int(m) for m in parts[1].split(',')]
            info = parts[2].strip() if len(parts) > 2 else None

            return {"name": name, "marks": marks, "info": info}

        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте снова")


def student_management_command_handle(command: str):
    if command == "show":
        show_students()
    elif command == "add":
        data = ask_student_payload()
        if add_student(data):
            print(f"Student {data['name']} добавлен")
        else:
            print("Ошибка: проверьте ввод")
    elif command == "mark":
        try:
            id_ = int(input("Введите ID студента: "))
            mark = int(input("Введите оценку (1-12): "))
            if 1 <= mark <= 12 and add_mark(id_, mark):
                print("Оценка добавлена")
            else:
                print("Ошибка: неверный ID или оценка")
        except ValueError:
            print("Ошибка: введите числовые значения")
    elif command == "search":
        try:
            id_ = int(input("Введите ID студента: "))
            student = storage.get(id_)
            if student:
                show_student(student)
            else:
                print("Студент не найден")
        except ValueError:
            print("Ошибка: введите числовой ID")
    elif command == "delete":
        try:
            id_ = int(input("Введите ID студента: "))
            if id_ in storage:
                del storage[id_]
                save_storage_to_file()
                print("Студент удален")
            else:
                print("Студент не найден")
        except ValueError:
            print("Ошибка: введите числовой ID")
    elif command == "update":
        try:
            id_ = int(input("Введите ID студента: "))
            if id_ not in storage:
                print("Студент не найден")
                return

            print("Введите новые данные (имя;[инфо]):")
            data = input().strip().split(';')
            student = storage[id_]

            if data[0].strip():
                student['name'] = data[0].strip()

            if len(data) > 1 and data[1].strip():
                existing = student.get('info', '')
                new_info = data[1].strip()
                student['info'] = new_info if existing in new_info else f"{existing} {new_info}"

            save_storage_to_file()
            print("Данные обновлены")
        except ValueError:
            print("Ошибка: неверный формат данных")
    else:
        print("Неизвестная команда")


def handle_user_input():
    commands = ("quit", "help", "show", "add", "search", "delete", "update", "mark")
    print(f"Доступные команды: {commands}")

    while True:
        command = input("\nВведите команду: ").strip().lower()

        if command == "quit":
            print("Выход из программы")
            break
        elif command == "help":
            print(f"Доступные команды: {commands}")
        elif command in commands:
            student_management_command_handle(command)
        else:
            print("Неизвестная команда")


if __name__ == "__main__":
    load_storage_from_file()
    handle_user_input()
