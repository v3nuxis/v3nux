Lesson 3
# Student Journal CLI Application

A simple console application to manage your student journal with support:
- Adding students with grades and additional information
- Adding grades to existing students
- Smart updating of student data
- Automatic saving to JSON file

## Main features
- **Data Storage**: All changes are saved to the `students.json` file
- **Validation**: Checks for correctness of input data
- **Average Score**: Automatically calculate and display the average grade
- **Smart Update**: 
  - If new information contains previous information - replacement occurs
  - If the information is new, it is added to the existing information
