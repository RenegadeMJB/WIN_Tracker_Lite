import argparse
import re

class Student:
    def __init__ (self, student_id: str):
        self._studentID: str = student_id
        self._lastName: str = ""
        self._firstName: str = ""
        self._winTasks: list [str] = []

    def addWinTasks(self, tasks: list [str]):
        for task in tasks:
            self._winTasks.append(task.strip("'"))

    @property
    def lastName(self):
        return self._lastName
    @lastName.setter
    def lastName(self, newLastName: str):
        self._lastName = newLastName

    @property
    def firstName(self):
        return self._firstName
    @firstName.setter
    def firstName(self, newFirstName: str):
        self._firstName = newFirstName

    @property
    def studentID(self):
        return self._studentID
    
    def __str__(self):
        return f"{self._studentID}: {self._lastName}, {self._firstName}"
    
#splits the input strings from the class output files from nebsis
def cSplit(inString: str) -> list:
    outList = []

    word = ''
    recording = False
    for c in inString:
        if recording:
            word += c
        if c == '"' and not recording:
            recording = True
        elif c == '"' and recording:
            recording = False
            outList.append(word.strip('"'))
            word = ''
    return outList

parser = argparse.ArgumentParser(description="WIN Tracker, the right way. (Spending way too much time to do something a spreadsheet can handle)")

parser.add_argument(
    "-init",
    "--init", 
    nargs=2, 
    metavar=("File Name", "File Path"), 
    help="Enter the file name to be created and the file path"
)

parser.add_argument(
    "-a",
    "--add",
    nargs=2,
    metavar=("File In", "File Out"),
    help="Enter the input file and the path to the output file"
)

parser.add_argument(
    "-s",
    "--student",
    nargs=1,
    metavar=("Student"),
    help="Enter the student to check"
)

def init(file_name, file_path):
    file_path += file_name
    try:
        with open(file_path, "w") as f:
            f.write('""\n')
        print(f"File '{file_path}' successfully created")
    except Exception as e:
        print(f"Error creating file '{file_path}': {e}")


def add(file_name, file_path):
    students: dict [Student] = {}
    with open(file_path, 'r') as f:
        sectionLine = f.readline()
        studentLines = f.readlines()

    sections: list [str] = sectionLine.split(',')
    sections.pop() #takes the last comma off

    for student in studentLines:
        student = student.strip()
        student = student.strip('{')
        student = student.strip('}')
        student = student.replace("'", "")
        winTasks = re.findall(r"\[(.*)\]",student)
        winTasks = winTasks[0].split(',')
        newStudentVals: list [str] = student.split(',')
        #print(newStudentVals)
        ID = newStudentVals[0].split(':')
        ID[1] = ID[1].strip()
        lastName = newStudentVals[1].split(':')
        lastName[1] = lastName[1].strip()
        firstName = newStudentVals[2].split(':')
        firstName[1] = firstName[1].strip()
        newStudent = Student(ID[1])
        newStudent.lastName = lastName[1]
        newStudent.firstName = firstName[1]
        newStudent.addWinTasks(winTasks)
        students[newStudent.studentID] = newStudent

    with open(file_name, 'r') as f:
        file_lines = f.readlines()

    file_lines.pop(0)

    for line in file_lines:
        studentList = cSplit(line)
        currentStudent = Student(studentList[0])
        currentStudent.lastName = studentList[3]
        currentStudent.firstName = studentList[1]
        students[currentStudent.studentID] = currentStudent
        #print(currentStudent)

    with open(file_path, 'w') as f:
        for section in sections:
            f.write(f'{section},')
        f.write('\n')
        for student in students.values():
            studentString = str(student.__dict__)
            f.write(studentString)
            f.write('\n')

def checkStudent(student):
    pass

def main():
    args = parser.parse_args()

    if args.init:
        file_name, file_path = args.init
        init(file_name, file_path)
    elif args.add:
        file_name, file_path = args.add
        add(file_name, file_path)
    elif args.student:
        student = args.student
        checkStudent(student)
    else:
        print("Win Tracker Lite v0.0.0")
        print("Initate a file with Command: wt -init File_Name File_Path")

if __name__ == "__main__":
    main()