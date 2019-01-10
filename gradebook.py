"""
TODO:
2) Create a JTable to store the info in.  Each column name will be as follows: Assignment Type (weight).  Each column
value will be as follows: Assignment name (grade).  Grades will be displayed as percents, and a grade < 0 will be a dash.
    - JTable must be resizable, since adding a category type will change structure.  For now, I'll assume it won't change,
    since the user should be smart enough to add all of the types before the table is constructed.
    - I should add a scrollbar to the table.
    - Display a mean breakdown either below or above the table in a similar fashion to the CS 2150 gradebook.  Obviously
    display the current grade as well
    - Add a "what do I need for this grade" feature.
3) Find a way to switch between courses.  I might already have the code for this with some tweaking to the failed attempt
at a grade book.  In fact, I might have a lot of useful stuff their, since the biggest issue was with saving data.
4) To save data, simply scrape the table and save it into a dictionary with a format below.  Then, save it as a json file
or a file of my own devising.
"""





class gradebook:
    def __init__(self,name,year,semester):
        self.name = name
        self.year = year
        self.semester = semester
        self.gb = {}

    def add_assignment_type(self,assignment_type,weight):
        self.gb[assignment_type] = ({},weight)

    def modify_assignment_grade(self,assignment_type,name,grade=-1.0):
        self.gb[assignment_type][0][name] = grade

    def calculate_grade(self):
        grade = 0
        total_weight = 1
        for grades in self.gb.values():
            g = self.__positive_mean(grades[0].values())*grades[1]
            if g >= 0:
                grade += g
            else:
                total_weight -= grades[1]
        return grade/total_weight


    def __positive_mean(self,grades):
        m = 0
        n = len(grades)
        for grade in grades:
            if grade >= 0:
                m += grade
            else:
                n -= 1
        return m/n if n > 0 else -1


gb = gradebook("CS 2102",2018,"Spring")
gb.add_assignment_type("Participation",.1)
gb.add_assignment_type("Problem Sets",.3)
gb.add_assignment_type("Quizzes",.1)
gb.add_assignment_type("Midterm",.22)
gb.add_assignment_type("Final",.28)

gb.modify_assignment_grade("Participation","Participation",1)
gb.modify_assignment_grade("Problem Sets","Problem Set 1",.93)
gb.modify_assignment_grade("Problem Sets","Problem Set 2",.97)
gb.modify_assignment_grade("Problem Sets","Problem Set 3",1)
gb.modify_assignment_grade("Problem Sets","Problem Set 4",1)
gb.modify_assignment_grade("Problem Sets","Problem Set 5",1)
gb.modify_assignment_grade("Problem Sets","Problem Set 6",1)
gb.modify_assignment_grade("Problem Sets","Problem Set 7",1)
gb.modify_assignment_grade("Problem Sets","Problem Set 8",.97)
gb.modify_assignment_grade("Problem Sets","Problem Set 9",.99)
gb.modify_assignment_grade("Problem Sets","Problem Set 10",1)
gb.modify_assignment_grade("Quizzes","Quiz 1",1)
gb.modify_assignment_grade("Quizzes","Quiz 5",1)
gb.modify_assignment_grade("Quizzes","Quiz 3",.9)
gb.modify_assignment_grade("Quizzes","Quiz 4",.9)
gb.modify_assignment_grade("Midterm","Midterm",.89)
gb.modify_assignment_grade("Final","Final",.99)

print(gb.calculate_grade())