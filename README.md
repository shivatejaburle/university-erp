# University Enterprise Resource Planning System
 University ERP system created using the Django framework, facilitating smooth interactions between students and teachers. Its core features include managing attendance, tracking marks, and organizing a timetable.

## Functionality
- ### Login
    - Common login page for Student, Teacher and Admin
- ### Admin
    - Manage Departments, Courses, Classes and Marks
    - Manage Student and Teacher profiles
    - Schedule Classes (Timetable)
    - Reset Attendance
    - All the above operations can also be done using Django Administration
- ### Teacher
    - Manage Attendance
    - Manage Marks
    - View Timetable
    - Reports
- ### Student
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
- **Teacher**: 
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