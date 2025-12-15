# 🏨 Hostel Management System

![Django](https://img.shields.io/badge/Django-4.x-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-orange)

A full-stack **Hostel Management System** built using **Django** that simplifies hostel operations like student enrollment, room allocation, notices, and payments. Designed with role-based access for **Admin, Warden, and Students**.

---

## ✨ Features

### 👨‍💼 Admin
- Approve or reject hostel registrations
- Post global notices
- View hostels and enrolled students

### 🧑‍🏫 Warden
- Approve/reject student requests
- Assign rooms to students
- Manage rooms and hostel details
- Send notices to students

### 🎓 Student
- Register and login
- Request hostel enrollment
- View notices and room details
- Access mess menu and hostel info
- Receive room assignment notifications

---

## 🛠️ Tech Stack

- **Backend:** Django
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite / PostgreSQL
- **Authentication:** Django Auth (Role-based)
- **Payments:** Django Payments module (extendable)

---

## 📂 Project Structure



## 📂 Project Structure

Hostel/
├── adminpanel/
├── hostelapp/
├── payments/
├── students/
├── users/
├── templates/
├── manage.py
├── requirements.txt


---

## ⚙️ Installation & Setup

```bash
git clone https://github.com/pranavvp00/hostel-management-system.git
cd hostel-management-system
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

