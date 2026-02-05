class Student:
    valid_courses: set[str] = {
        "Computer Science",
        "Software Engineering",
        "Networks and Security",
        "Data Science",
        "Cybersecurity",
        "Computing",
    }

    def __init__(self, up_number: str, course: str) -> None:
        self._up_number: str = up_number
        self._course: str = course
        self._year: int = 1

    def __str__(self) -> str:
        return f"Student {self.up_number} studying {self.course} in year {self._year}"

    @property
    def up_number(self) -> str:
        return self._up_number

    @property
    def course(self) -> str:
        return self._course

    @course.setter
    def course(self, new_course: str) -> None:
        if new_course in self.valid_courses:
            self._course = new_course

    @property
    def year(self) -> int:
        return self._year

    def progress(self) -> None:
        pass


class PlacementStudent(Student):
    def __init__(self, up_number: str, course: str, company: str) -> None:
        super().__init__(up_number, course)
        self._year = 3
        self._company = company

    def __str__(self) -> str:
        return f"Placement student {self.up_number} working at {self.company}"

    @property
    def company(self) -> str:
        return self._company


def test_student_classes() -> None:
    s1 = Student("UP123456", "Computer Science")
    print(s1)

    # Access properties
    print("UP number:", s1.up_number)
    print("Course:", s1.course)
    print("Year:", s1.year)

    # Attempt to change course to a valid course
    s1.course = "Data Science"
    print("Updated course:", s1.course)

    # Attempt to change course to an invalid course (should have no effect)
    s1.course = "History"
    print("After invalid update attempt:", s1.course)

    print("-" * 40)

    # Create a placement student
    ps = PlacementStudent("UP654321", "Software Engineering", "OpenAI")
    print(ps)

    # Access inherited and new properties
    print("UP number:", ps.up_number)
    print("Course:", ps.course)
    print("Year:", ps.year)
    print("Company:", ps.company)
