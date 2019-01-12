# Purpose

The purpose of this application is to provide a convenient way for students to track their grades for multiple courses.  Version 1.0 is nearly complete - it should be released within the week.  As of right now, the application is fully functional.  I still want to make some aesthetic changes and there isn't any input validation at the moment, but it works when used correctly.  Input validation will be added in the coming days.

# Application Description
The application was created using PyQT5.  The application consists of a single window containing a menubar and a tree table widget.

## How to use the Application
Run the gui.py file with a python 3 interpretter (3.6.7 was used for the development of the application).

### Adding a Course
To add a course, right click anywhere blank area in the table or an existing course and select "Add New Course."  Alternatively, press the "Insert" key while not touching any tree items.  Double click the new item to edit its name, or select the item and press the "F2" key.  The Grade Section for the course will be updated automatically as assignments are added and/or removed.

### Removing a Course
To remove a course, right click the course and select "Remove Selected Course." Double click the new item to edit its name.  Alternatively, select the course and press the "Delete" key.

### Adding an Assignment Type (Exams, HW, etc)
To add an Assignment Type for a course, right click the course and select "Add New Assignment Type." Alternatively, select the course and press the "Insert" key. Double click the new item to edit its name, or press the "F2" key. You should put a percent weight in "Weight" column following one of the following formats:
- decimal format (ex: 10% becomes .1 or 0.1)
- fractional format (ex: insert 1/5, 55/100, etc)

### Removing an Assignment Type
To remove an assignment type, right click the assignment type and select "Remove Selected Assignment Type." Alternatively, select the assignment type and press the "Delete" key.

### Adding an Assignment
To add an assignment for an assignment type, right click the assignment type and select "Add New Assignment."  Alternatively, select the assignment type and press the "Insert" key.  You should put a percent value for the grade received on the assignment in the "Grade" column.  If the assignment has not yet been graded, simply leave the "Grade" column blank.  The grade value should be one of the following formats:
- decimal format (ex: 96.5% becomes .965 or 0.965)
- fractional format (ex: insert 49/50, 112.5/139, etc)

### Removing an Assignment
To remove an assignment, right click the assignment type and select "Remove Selected Assignment."  Alternatively, select the assignment and press the "Delete" key.

### Saving files, opening files, and similar
It basically works the same as any other software.  Just go to the File menubar or use common shortcuts (Ctrl+S is save, etc).  The extension for the application is .grdb, short for gradebook.

## Current Features
- File saving and opening
- Adding courses, assignment types, assignments, weights, and grades

## Features to Implement before version 1.0 release
- ~~Grade calculation~~
- Input validation.
    - Don't allow the user to type where they shouldn't (ex, they shouldn't be able to enter a weight for an assignment, as all assignments within an assignment type are assumed to have equal weight.)
    - Don't allow the user to enter invalid strings anywhere (ex, don't let the user enter "A" in the grade column)

## Features to implement in the future
- Undo/Redo functionality
- Allow User to choose a style (css for the technically savy users or premade options for anyone else)
- ~~Bind the delete key to allow for the deleting of selected rows~~
- ~~Bind the insert key to allow for inserting rows~~
