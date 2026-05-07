#  Mini Employee Management API

A lightweight RESTful backend built with **FastAPI** and **SQLAlchemy** to manage employee records in **MS SQL Server**.

##  Tech Stack
*   **Framework:** FastAPI
*   **ORM:** SQLAlchemy (with pyodbc)
*   **Database:** MS SQL Server
*   **Validation:** Pydantic 

##  Features
*   **Full CRUD**: Create, Read, Update, and Delete employees.
*   **Partial Updates**: Toggle `isActive` status via **PATCH**.
*   **Data Validation**:
    *   Strict **EmailStr** format validation.
    *   Salary must be **greater than 0**.
    *   **String length constraints** for names and departments (min 2, max 100).
*   **Robust Error Handling**:
    *   **404 Not Found**: For missing employee IDs.
    *   **409 Conflict**: For duplicate email registrations.
    *   **422 Unprocessable Entity**: For invalid Pydantic input.
    *   **500 Internal Server Error**: For database connection or unhandled server issues.


