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
FINAL_FASTAPI_PROJECT/
│
├── main.py
├── requirements.txt
├── README.md
│
└── screenshots/


---

## How to Run

### Install packages
pip install fastapi uvicorn

### Start server
uvicorn main:app --reload

### Open API Docs
http://127.0.0.1:8000/docs

---

## 🧪 API Categories

### Movies
- `http://127.0.0.1:8000/docs#/default/get_movies_movies_get`
- `http://127.0.0.1:8000/docs#/default/create_movie_movies_post`
- `http://127.0.0.1:8000/docs#/default/search_movies_movies_search_get`
- `http://127.0.0.1:8000/docs#/default/get_movie_movies__movie_id__get`
- `http://127.0.0.1:8000/docs#/default/update_movie_movies__movie_id__put`
- `http://127.0.0.1:8000/docs#/default/delete_movie_movies__movie_id__delete`

### Booking
- `http://127.0.0.1:8000/docs#/default/get_bookings_bookings_get`
- `http://127.0.0.1:8000/docs#/default/book_ticket_bookings_post`

### Seat Workflow
- `http://127.0.0.1:8000/docs#/default/hold_seats_seat_hold_post`
- `http://127.0.0.1:8000/docs#/default/get_holds_seat_hold_get`
- `http://127.0.0.1:8000/docs#/default/confirm_hold_seat_confirm__hold_id__post`
- `http://127.0.0.1:8000/docs#/default/release_hold_seat_release__hold_id__delete`

### Advanced APIs
- `http://127.0.0.1:8000/docs#/default/search_bookings_bookings_search_get`
- `http://127.0.0.1:8000/docs#/default/sort_bookings_bookings_sort_get`
- `http://127.0.0.1:8000/docs#/default/paginate_bookings_bookings_page_get`

---

## What I Learned

- How to build APIs using FastAPI  
- How to structure backend properly  
- CRUD operations  
- Validation using Pydantic  
- Real-world workflow design  
- Search, sorting, and pagination  

## Final Note

This project helped me understand how a real backend system works.  
It can be further improved by adding database, authentication, and payment features.

---

👨‍💻 Author

**Sankalp (Manju Sankalp)**
