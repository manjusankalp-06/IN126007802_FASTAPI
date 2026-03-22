# 🎬 Movie Ticket Booking API

## About the Project
This project is developed as part of my **FastAPI internship final assignment**.  
The main goal is to build a **complete backend system** instead of just simple APIs.

It represents a **Movie Ticket Booking system**, where users can check movies, manage bookings, and handle seat availability.

---

## What This API Does

Using this API, a user can:

- View all movies
- Get details of a specific movie
- Book tickets for a movie
- Hold seats before confirming booking
- Confirm or cancel seat holds
- Search and filter movies
- Sort and paginate results

---

## Technologies Used

- Python  
- FastAPI  
- Pydantic (for validation)  
- Uvicorn (server)  
- Swagger UI (for testing APIs)

---

## Main Functionalities

### 🎬 Movie Management
- Add new movies  
- Update movie details  
- Delete movies  
- View all movies and individual movie  

### Booking System
- Create booking  
- View bookings  
- Search bookings  

### Seat Handling (Workflow)
- Hold seats temporarily  
- Confirm booking using hold ID  
- Release seats if not needed  

### Advanced Features
- Search movies using keyword  
- Filter movies based on conditions  
- Sort movies (price, seats, etc.)  
- Pagination for large data  
- Combined browsing (search + filter + sort + pagination)  

---

## 📂 Project Structure
