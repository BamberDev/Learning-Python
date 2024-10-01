# Baza szkolna

class School:
    def __init__(self):
        self.students = []
        self.teachers = []
        self.homeroom_teachers = []

    def create_new_user(self):
        while True:
            print("\nWybierz opcje: uczen, nauczyciel, wychowawca, koniec")
            option = input("Co chcesz zrobic?: ").lower()

            if option == "uczen":
                self.add_student()
            elif option == "nauczyciel":
                self.add_teacher()
            elif option == "wychowawca":
                self.add_homeroom_teacher()
            elif option == "koniec":
                break
            else:
                print("Niepoprawna opcja!")

    def add_student(self):
        name = input("Podaj imie i nazwisko ucznia: ")
        class_name = input("Podaj klase (np. '3C'): ")
        self.students.append({"name": name, "class": class_name})
        print(f"Uczen {name} dodany do klasy {class_name}.")

    def add_teacher(self):
        name = input("Podaj imie i nazwisko nauczyciela: ")
        subject = input("Podaj przedmiot, ktory prowadzi nauczyciel: ")
        classes = []
        print("Podaj klasy, ktore prowadzi nauczyciel (wpisz pusta linie, aby zakonczyc):")
        while True:
            class_name = input("Klasa: ")
            if class_name == "":
                break
            classes.append(class_name)
        self.teachers.append({"name": name, "subject": subject, "classes": classes})
        print(f"Nauczyciel {name}, przedmiot {subject}, klasy: {', '.join(classes)}.")

    def add_homeroom_teacher(self):
        name = input("Podaj imie i nazwisko wychowawcy: ")
        class_name = input("Podaj klase, ktorej wychowawca jest nauczyciel: ")
        self.homeroom_teachers.append({"name": name, "class": class_name})
        print(f"Wychowawca {name}, klasa {class_name}.")

    def manage_school_data(self):
        while True:
            print("\nWybierz opcje: klasa, uczen, nauczyciel, wychowawca, koniec")
            option = input("Co chcesz zrobic?: ").lower()

            if option == "klasa":
                self.show_class()
            elif option == "uczen":
                self.show_student_schedule()
            elif option == "nauczyciel":
                self.show_teacher_classes()
            elif option == "wychowawca":
                self.show_homeroom_students()
            elif option == "koniec":
                break
            else:
                print("Niepoprawna opcja!")

    def show_class(self):
        class_name = input("Podaj nazwe klasy (np. '3C'): ")
        students_in_class = [student['name'] for student in self.students if student['class'] == class_name]
        homeroom_teacher = next((t for t in self.homeroom_teachers if t['class'] == class_name), None)

        if students_in_class:
            print(f"\nKlasa {class_name}:")
            print("Uczniowie:")
            for student in students_in_class:
                print(f" - {student}")
            if homeroom_teacher:
                print(f"Wychowawca: {homeroom_teacher['name']}")
            else:
                print("Brak wychowawcy dla tej klasy.")
        else:
            print(f"Brak uczniow w klasie {class_name}.")

    def show_student_schedule(self):
        name = input("Podaj imie i nazwisko ucznia: ")
        student = next((s for s in self.students if s['name'] == name), None)
        
        if not student:
            print(f"Brak ucznia o imieniu {name}.")
            return
        
        class_name = student['class']
        student_classes = [t for t in self.teachers if class_name in t['classes']]

        if student_classes:
            print(f"\nLekcje ucznia {student['name']} (klasa {class_name}):")
            for teacher in student_classes:
                print(f" - {teacher['subject']} z nauczycielem: {teacher['name']}")
        else:
            print(f"Brak lekcji dla ucznia {name}.")

    def show_teacher_classes(self):
        name = input("Podaj imie i nazwisko nauczyciela: ")
        teacher = next((t for t in self.teachers if t['name'] == name), None)

        if teacher:
            print(f"Nauczyciel {teacher['name']} prowadzi klasy: {', '.join(teacher['classes'])}")
        else:
            print(f"Brak nauczyciela o imieniu {name}.")

    def show_homeroom_students(self):
        name = input("Podaj imie i nazwisko wychowawcy: ")
        homeroom_teacher = next((t for t in self.homeroom_teachers if t['name'] == name), None)

        if homeroom_teacher:
            students_in_class = [student['name'] for student in self.students if student['class'] == homeroom_teacher['class']]
            print(f"Wychowawca {homeroom_teacher['name']}, klasa {homeroom_teacher['class']}, uczniowie:")
            for student in students_in_class:
                print(f" - {student}")
        else:
            print(f"Brak wychowawcy o imieniu {name}.")

school = School()

while True:
    print("\nDostepne komendy: utworz, zarzadzaj, koniec")
    command = input("Podaj komende: ").lower()

    if command == "utworz":
        school.create_new_user()
    elif command == "zarzadzaj":
        school.manage_school_data()
    elif command == "koniec":
        print("Zakonczono program.")
        break
    else:
        print("Nieznana komenda!")


