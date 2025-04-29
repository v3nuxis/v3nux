import json

STORAGE_FILE = "students.json"

default_students = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "marks": [7, 8, 9, 10, 6, 7, 8],
        "info": "Alice Johnson is 18 y.o. Interests: math",
        "from": "USA.New York"
    },
    {
        "id": 2,
        "name": "Michael Smith",
        "marks": [6, 5, 7, 8, 7, 9, 10],
        "info": "Michael Smith is 19 y.o. Interests: science",
        "from": "United Kingdom.Manchester"
    },
    {
        "id": 3,
        "name": "Emily Davis",
        "marks": [9, 8, 8, 7, 6, 7, 7],
        "info": "Emily Davis is 17 y.o. Interests: literature",
        "from": "Nigeria.Abuja"
    },
    {
        "id": 4,
        "name": "James Wilson",
        "marks": [5, 6, 7, 8, 9, 10, 11],
        "info": "James Wilson is 20 y.o. Interests: sports",
        "from": "United Kingdom.London"
    },
    {
        "id": 5,
        "name": "Olivia Martinez",
        "marks": [10, 9, 8, 7, 6, 5, 4],
        "info": "Olivia Martinez is 18 y.o. Interests: art",
        "from": "Spain.Madrid"
    },
    {
        "id": 6,
        "name": "Daniel Brown",
        "marks": [4, 5, 6, 7, 8, 9, 10],
        "info": "Daniel Brown is 19 y.o. Interests: music",
        "from": "Ukraine.Kyiv"
    },
    {
        "id": 7,
        "name": "Sophia Taylor",
        "marks": [11, 10, 9, 8, 7, 6, 5],
        "info": "Sophia Taylor is 20 y.o. Interests: physics",
        "from": "Belarus.Minsk"
    },
    {
        "id": 8,
        "name": "William Anderson",
        "marks": [7, 7, 7, 7, 7, 7, 7],
        "info": "William Anderson is 18 y.o. Interests: chemistry",
        "from": "Romania.Buharest"
    },
    {
        "id": 9,
        "name": "Isabella Thomas",
        "marks": [8, 8, 8, 8, 8, 8, 8],
        "info": "Isabella Thomas is 19 y.o. Interests: biology",
        "from": "USA.Ohio"
    },
    {
        "id": 10,
        "name": "Benjamin Jackson",
        "marks": [9, 9, 9, 9, 9, 9, 9],
        "info": "Benjamin Jackson is 20 y.o. Interests: history",
        "from": "United Kingdom.London"
    },
]

def load_storage_from_file():
    global storage
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            storage = json.load(f)
    except FileNotFoundError:
        # Если файл не найден, используем дефолтных студентов
        print("Storage file not found. Using default students.")
        storage = default_students
    except json.JSONDecodeError:
        # Если файл поврежден, используем дефолтных студентов
        print("Storage file is corrupted. Using default students.")
        storage = default_students

def save_storage_to_file():
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(storage, f, indent=4, ensure_ascii=False)

# CRUD
def add_student(student: dict) -> dict | None:
    if len(student) != 2:
        return None

    if not student.get("name") or not student.get("marks"):
        return None
    else:
        new_id = max([s['id'] for s in storage], default=0)+1
        student["id"] = new_id
        student["info"] = ""
        storage.append(student)
        save_storage_to_file() 
        return student

def show_students():
    print("=========================\n")
    for student in storage:
        print(f"{student['id']}. Student {student['name']} id: {student['id']}\n")
    print("=========================\n")

def search_student(student_id: int) -> None:
    for student in storage:
        info = (
            "=========================\n"
            f"[{student['id']}] Student {student['name']}\n"
            f"Marks: {student['marks']}\n"
            f"Info: {student['info']}\n"
            "=========================\n"
        )

        if student["id"] == student_id:
            print(info)
            return

    print(f"Student with ID {student_id} not found")

def ask_student_payload() -> dict:
    ask_prompt = (
        "Enter student's payload data using text template: "
        "John Doe;1,2,3,4,5\n"
        "where 'John Doe' is a full name and [1,2,3,4,5] are marks.\n"
        "The data must be separated by ';'"
    )

    def parse(data) -> dict:
        name, raw_marks = data.split(";")

        return {
            "name": name,
            "marks": [int(item) for item in raw_marks.replace(" ", "").split(",")],
        }

    user_data: str = input(ask_prompt)
    return parse(user_data)

def student_management_command_handle(command: str):
    if command == "show":
        show_students()
    elif command == "add":
        data = ask_student_payload()
        if data:
            student: dict | None = add_student(data)
            print(f"Student: {student['name']} is added")
        else:
            print("The student's data is NOT correct. Please try again")
    elif command == "search":
        student_id: str = input("\nEnter student's ID: ")
        if student_id:
            search_student(student_id=int(student_id))
        else:
            print("Student's ID is required to search")

def handle_user_input():
    OPERATIONAL_COMMANDS = ("quit", "help")
    STUDENT_MANAGEMENT_COMMANDS = ("show", "add", "search")
    AVAILABLE_COMMANDS = (*OPERATIONAL_COMMANDS, *STUDENT_MANAGEMENT_COMMANDS)

    HELP_MESSAGE = (
        "Hello in the Journal! User the menu to interact with the application.\n"
        f"Available commands: {AVAILABLE_COMMANDS}"
    )

    print(HELP_MESSAGE)

    while True:

        command = input("\n Select command: ")

        if command == "quit":
            print("\nThanks for using the Journal application")
            break
        elif command == "help":
            print(HELP_MESSAGE)
        else:
            student_management_command_handle(command)

if __name__ == "__main__":
    load_storage_from_file() 
    handle_user_input()
