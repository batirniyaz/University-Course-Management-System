# 🧠 Project Name: University Course Management System

## 🧾 Project Summary
A basic system where:  
- Teachers can create and manage courses.  
- Students can browse and enroll in courses.  
- Services communicate over REST and gRPC.

## 🏗️ Microservices Overview

### 1. User Service (REST)
Handles user registration, login, and role management.  
**Endpoints:**  
- `POST /register` – Register a student or teacher  
- `POST /login` – Get JWT token  
- `GET /me` – Get user profile  
- `GET /users/{user_id}` – (Used internally by gRPC for identity lookup)  

**Key Features:**  
- JWT authentication  
- Role-based access: student or teacher  

### 2. Course Service (gRPC)
Manages course creation and retrieval. Only accessible to authenticated teachers.  
**gRPC Methods:**  
- `CreateCourse(CreateCourseRequest)` returns `(CourseResponse)`  
- `ListCourses(Empty)` returns `(CourseList)`  
- `GetCourse(GetCourseRequest)` returns `(CourseResponse)`  
- `GetCourseTeacher(GetCourseRequest)` returns `(UserInfo)` (via gRPC call to User Service)  

### 3. Enrollment Service (gRPC)
Handles student enrollment in courses.  
**gRPC Methods:**  
- `EnrollStudent(EnrollRequest)` returns `(EnrollResponse)`  
- `ListStudentsByCourse(CourseRequest)` returns `(StudentList)`  
- `ListCoursesByStudent(StudentRequest)` returns `(CourseList)`  

**Behavior:**  
- On enrollment, the service must:  
  - Verify the student exists via User Service  
  - Verify the course exists via Course Service  

## ⚙️ Tech Stack

| **Layer**          | **Technology**                          |
|---------------------|-----------------------------------------|
| API / Services     | Python (FastAPI or Flask)              |
| gRPC               | grpcio, grpcio-tools                   |
| Auth               | JWT (pyjwt or fastapi-jwt-auth)        |
| DB                 | PostgreSQL / SQLite (via SQLAlchemy or Tortoise ORM) |
| Containerization   | Docker + docker-compose (optional)     |
