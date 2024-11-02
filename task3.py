import re

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class StudentListProcessor:
    def __init__(self, group_number):
        self.group_number = group_number
        self.student_pattern = re.compile(
            r'([А-ЯЁ][а-яё]+(?:-[А-ЯЁ][а-яё]+)?)\s([А-ЯЁ])\.\s?([А-ЯЁ])\.\s+(\S+)',
            re.UNICODE
        )

    def process_list(self, text):
        all_students = []
        excluded_students = set()
        for match in self.student_pattern.finditer(text):
            full_entry = match.group()
            surname, initial1, initial2, group = match.groups()
            all_students.append(full_entry)
            if group == self.group_number and initial1 == initial2:
                excluded_students.add(full_entry)
        remaining_students = [student for student in all_students if student not in excluded_students]
        return remaining_students

if __name__ == "__main__":
    processor = StudentListProcessor("P0000")

    test_cases = [
        (
            "Петров П.П. P0000 "
            "Анищенко А.А. P33113 "
            "Примеров Е.В. P0000 "
            "Иванов И.И. P0000",
            [
                "Анищенко А.А. P33113",
                "Примеров Е.В. P0000"
            ]
        ),
        (
            "Сидоров С.С. P0000 "
            "Кузнецов К.К. P0000 "
            "Лебедев А.Б. P0000 "
            "Павлов П.П. P12345",
            [
                "Лебедев А.Б. P0000",
                "Павлов П.П. P12345"
            ]
        ),
        (
            "Орлов О.О. P0000 "
            "Зайцев З.З. P0000 "
            "Морозов М.М. P0000 "
            "Соколова С.А. P0000",
            [
                "Соколова С.А. P0000"
            ]
        ),
        (
            "Васильев В.В. P0000 "
            "Крылова К.К. P0000 "
            "Смирнов С.С. P0000 "
            "Иванова И.А. P0000",
            [
                "Иванова И.А. P0000"
            ]
        ),
        (
            "Федоров Ф.Ф. P0000 "
            "Петрова П.П. P0000 "
            "Николаев Н.Н. P0000 "
            "Григорьев Г.Г. P0000",
            []
        ),
    ]

    for idx, (text, expected_output) in enumerate(test_cases, 1):
        print(f"{bcolors.HEADER}Тест {idx}:{bcolors.ENDC}")
        print(text)
        result = processor.process_list(text)
        print(f"{bcolors.OKBLUE}Ожидаемый результат:{bcolors.ENDC}")
        print('\n'.join(expected_output))
        print(f"{bcolors.OKCYAN}Результат программы:{bcolors.ENDC}")
        print('\n'.join(result))
        if sorted(result) == sorted(expected_output):
            print(f"{bcolors.OKGREEN}Результаты совпадают.{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}Результаты не совпадают.{bcolors.ENDC}")
        print("-" * 50)

    user_text = input("Введите список студентов в одну строку:\n")
    result = processor.process_list(user_text)
    if result:
        print(f"{bcolors.OKGREEN}Оставшиеся студенты:{bcolors.ENDC}")
        print('\n'.join(result))
    else:
        print(f"{bcolors.WARNING}Все студенты вашей группы с одинаковыми инициалами были удалены.{bcolors.ENDC}")
