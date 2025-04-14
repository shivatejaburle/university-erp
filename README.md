# University Enterprise Resource Planning System
 **U**niversity **E**nterprise **R**esource **P**lanning **S**ystem (**UERPS**) created using the Django framework, facilitating smooth interactions between students and teachers. **UERPS** core features include managing attendance, tracking marks, and organizing a timetable.

- **Department**
    - A department serves as an educational sub-unit within the college, offering a variety of programmes and courses. Each department is overseen by a Head of the Department (HOD), who manages its operations and ensures effective functioning.

- **Course**
    - A course refers to a subject offered by a department during a semester, which students are required to complete to qualify for the Semester Final Examination (SFE) and, ultimately, the award of a Bachelor's Degree.

- **Semester**
    - A semester is a time period of five months during which a department offers a set of courses to students. Each academic year is composed of three semesters, including two regular semesters and one supplementary semester.
- **Continuous Internal Evaluation**
    - Continuous Internal Evaluation (CIE) is a system of ongoing assessments conducted throughout the semester to evaluate a student's academic performance. It typically consists of five events or examinations. At the end of the semester, the results from these evaluations are summed up and reduced to a total of 50 marks. 

- **Semester Final Examination**
    - The Semester Final Examination (SFE) is held at the conclusion of each semester to evaluate a student's academic performance. It is conducted for a total of 100 marks, which are then scaled down to 50 marks in the final assessment.

## UERPS Features
- ### Login
    - Common login page for Student, Teacher HOD and Admin
    - Django Allauth Authentication
- ### Admin Dashboard
    - Manage Departments, Courses, Classes and Marks
    - Manage Student and Teacher profiles
    - Schedule Classes (Timetable)
    - Reset Attendance
    - All the above operations can also be done using Django Administration
- ### HOD Dashboard
    - Manage Courses and Classes
    - Manage Student and Teacher profiles
    - Schedule Classes (Timetable)
    - View whole Department Timetable
    - View Student Marks
    - Manage Student Attendance
    - Reports
- ### Teacher Dashboard
    - Manage Attendance
    - Manage Marks
    - View Timetable
    - Reports
    - **View as HOD** is visible if teacher is HOD (for switching to HOD Dashboard)
- ### Student Dashboard
    - View Attendance
    - View Marks
    - View Timetable

## Installing
### Clone the project

```bash
git clone https://github.com/shivatejaburle/university-erp
cd university-erp
```

### Setup your Virtual Environment
```bash
pip install virtualenv
virtualenv venv
# For Windows
venv\Scripts\activate   
# For Mac
source venv/bin/activate 
```

### Install dependencies
```bash
pip install -r requirements.txt
```
### Collect static files (only on a production server)

```bash
python manage.py collectstatic
```

### Running a development server

Just run this command:

```bash
python manage.py runserver
```
Your application will be available @ http://127.0.0.1:8000/

### Login Information
- **Admin**: 
    - Username : admin
    - Password : Univ#12345
- **HOD and Teacher**: 
    - Username : aditi_t001
    - Password : aditi_1990
- **Student**: 
    - Username : neha_001
    - Password : neha_1990

## Screenshots
### Home Page
![Home Page](screenshots/Home-Page.jpg)
### Login Page
![Login Page](screenshots/Login-Page.jpg)
### Admin Dashboard
![Admin Dashboard](screenshots/A1-Admin-Home.jpg)
![Manage Data](screenshots/A2-Manage-Data.jpg)
![Edit Periods](screenshots/A3-Edit-Periods.jpg)
![Reset Attendance](screenshots/A4-Reset-Attendance.jpg)
    **Note:** This action removes all existing attendance records and generates new ones within the specified time range.
### HOD Dashboard
![Teacher Dashboard](screenshots/H1-Teacher-as-HOD.jpg)
![HOD Dashboard](screenshots/H2-HOD-Home.jpg)
![Department Courses](screenshots/H3-Courses.jpg)
![Department Classes](screenshots/H4-Classes.jpg)
![Department Teachers](screenshots/H5-Teachers.jpg)
![Department Students](screenshots/H6-Students.jpg)
![Department Timetable](screenshots/H7-Timetable.jpg)
![Department Reports](screenshots/H8-Reports.jpg)
![Department Report Details](screenshots/H9-Report-Details.jpg)
![Assign Course to Teachers](screenshots/H10-Assign-Teacher.jpg)
![Assign Period to Teachers](screenshots/H11-Assign-Period.jpg)
### Teacher Dashboard
![Teacher Dashboard](screenshots/T1-Teacher-Home.jpg)
![Classes](screenshots/T2-Classes.jpg)
![Attendance](screenshots/T3-Attendance.jpg)
![Mark Attendance](screenshots/T4-Mark-Attendance.jpg)
![Marks](screenshots/T5-Marks.jpg)
![Timetable](screenshots/T6-Timetable.jpg)
![Reports](screenshots/T7-Reports.jpg)
### Student Dashboard
![Student Dashboard](screenshots/S1-Student-Home.jpg)
![Attendance](screenshots/S2-Attendance.jpg)
![Attendance Details](screenshots/S3-Attendance-Details.jpg)
![Marks](screenshots/S4-Marks.jpg)
![Timetable](screenshots/S5-Timetable.jpg)
### Mobile View
&emsp;![Home Page](screenshots/M1-Home-Page.png)&emsp;&emsp;&emsp;![Admin Dashboard](screenshots/M2-Login.png)

&emsp;![Admin Dashboard](screenshots/M3-Admin-Dashboard.png)&emsp;&emsp;&emsp;![Manage Data](screenshots/M4-Manage-Data.png)

&emsp;![Enter Marks](screenshots/M5-Enter-Marks.png)&emsp;&emsp;&emsp;![Timetable](screenshots/M6-Timetable.png)

**Note:** All pages are responsive with small, medium and large devices.