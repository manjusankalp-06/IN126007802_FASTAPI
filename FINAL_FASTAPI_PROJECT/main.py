from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# ───────── DATA ─────────
movies = [
    {"id": 1, "title": "Inception", "genre": "Action", "language": "English", "duration_mins": 148, "ticket_price": 200, "seats_available": 50},
    {"id": 2, "title": "Interstellar", "genre": "Drama", "language": "English", "duration_mins": 169, "ticket_price": 250, "seats_available": 30},
    {"id": 3, "title": "Get Out", "genre": "Horror", "language": "English", "duration_mins": 104, "ticket_price": 180, "seats_available": 20},
    {"id": 4, "title": "3 Idiots", "genre": "Comedy", "language": "Hindi", "duration_mins": 171, "ticket_price": 150, "seats_available": 60},
    {"id": 5, "title": "RRR", "genre": "Action", "language": "Telugu", "duration_mins": 182, "ticket_price": 230, "seats_available": 40},
    {"id": 6, "title": "Joker", "genre": "Drama", "language": "English", "duration_mins": 122, "ticket_price": 190, "seats_available": 25}
]

bookings = []
booking_counter = 1

holds = []
hold_counter = 1

# ───────── MODELS ─────────
class BookingRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    movie_id: int = Field(..., gt=0)
    seats: int = Field(..., gt=0, le=10)
    phone: str = Field(..., min_length=10)
    seat_type: str = "standard"
    promo_code: str = ""

class NewMovie(BaseModel):
    title: str = Field(..., min_length=2)
    genre: str = Field(..., min_length=2)
    language: str = Field(..., min_length=2)
    duration_mins: int = Field(..., gt=0)
    ticket_price: int = Field(..., gt=0)
    seats_available: int = Field(..., gt=0)

# ───────── HELPERS ─────────
def find_movie(movie_id: int):
    return next((m for m in movies if m["id"] == movie_id), None)

def calculate_ticket_cost(base_price, seats, seat_type, promo_code=""):
    multiplier = 1
    if seat_type == "premium":
        multiplier = 1.5
    elif seat_type == "recliner":
        multiplier = 2

    original = base_price * seats * multiplier

    discount = original
    if promo_code == "SAVE10":
        discount = original * 0.9
    elif promo_code == "SAVE20":
        discount = original * 0.8

    return int(original), int(discount)

def filter_movies_logic(genre=None, language=None, max_price=None, min_seats=None):
    result = movies
    if genre is not None:
        result = [m for m in result if m["genre"].lower() == genre.lower()]
    if language is not None:
        result = [m for m in result if m["language"].lower() == language.lower()]
    if max_price is not None:
        result = [m for m in result if m["ticket_price"] <= max_price]
    if min_seats is not None:
        result = [m for m in result if m["seats_available"] >= min_seats]
    return result

# ───────── Q1 ─────────
@app.get("/")
def home():
    return {"message": "Welcome to Cineplex Booking"}

# ───────── Q2 ─────────
@app.get("/movies")
def get_movies():
    return {
        "movies": movies,
        "total": len(movies),
        "total_seats_available": sum(m["seats_available"] for m in movies)
    }

# ───────── Q5 (BEFORE /{id}) ─────────
@app.get("/movies/summary")
def summary():
    genres = {}
    for m in movies:
        genres[m["genre"]] = genres.get(m["genre"], 0) + 1

    return {
        "total_movies": len(movies),
        "most_expensive": max(movies, key=lambda x: x["ticket_price"]),
        "cheapest": min(movies, key=lambda x: x["ticket_price"]),
        "total_seats": sum(m["seats_available"] for m in movies),
        "genre_count": genres
    }

# ───────── Q10 ─────────
@app.get("/movies/filter")
def filter_movies(
    genre: Optional[str] = None,
    language: Optional[str] = None,
    max_price: Optional[int] = None,
    min_seats: Optional[int] = None
):
    result = filter_movies_logic(genre, language, max_price, min_seats)
    return {"results": result, "count": len(result)}

# ───────── Q16 ─────────
@app.get("/movies/search")
def search_movies(keyword: str):
    result = [m for m in movies if keyword.lower() in m["title"].lower()
              or keyword.lower() in m["genre"].lower()
              or keyword.lower() in m["language"].lower()]
    if not result:
        return {"message": "No movies found"}
    return {"results": result, "total_found": len(result)}

# ───────── Q17 ─────────
@app.get("/movies/sort")
def sort_movies(sort_by: str = "ticket_price"):
    if sort_by not in ["ticket_price", "title", "duration_mins", "seats_available"]:
        raise HTTPException(400, "Invalid sort field")
    return sorted(movies, key=lambda x: x[sort_by])

# ───────── Q18 ─────────
@app.get("/movies/page")
def paginate(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    total_pages = (len(movies) + limit - 1) // limit
    return {
        "total": len(movies),
        "total_pages": total_pages,
        "data": movies[start:start + limit]
    }
# ───────── Q20 ─────────
@app.get("/movies/browse")
def browse(
    keyword: Optional[str] = None,
    genre: Optional[str] = None,
    language: Optional[str] = None,
    sort_by: str = "ticket_price",
    order: str = "asc",
    page: int = 1,
    limit: int = 3
):
    result = movies

    if keyword:
        result = [m for m in result if keyword.lower() in m["title"].lower()]

    if genre:
        result = [m for m in result if m["genre"].lower() == genre.lower()]

    if language:
        result = [m for m in result if m["language"].lower() == language.lower()]

    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x.get(sort_by, 0), reverse=reverse)

    start = (page - 1) * limit
    return result[start:start + limit]

# ───────── Q3 (KEEP AFTER ABOVE) ─────────
@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(404, "Movie not found")
    return movie

# ───────── Q4 ─────────
@app.get("/bookings")
def get_bookings():
    total_revenue = sum(b["discounted_cost"] for b in bookings)
    return {
        "bookings": bookings,
        "total": len(bookings),
        "total_revenue": total_revenue
    }

# ───────── Q8 + Q9 ─────────
@app.post("/bookings")
def book_ticket(req: BookingRequest):
    global booking_counter

    movie = find_movie(req.movie_id)
    if not movie:
        raise HTTPException(404, "Movie not found")

    if movie["seats_available"] < req.seats:
        raise HTTPException(400, "Not enough seats")

    original, discounted = calculate_ticket_cost(
        movie["ticket_price"], req.seats, req.seat_type, req.promo_code
    )

    movie["seats_available"] -= req.seats

    booking = {
        "booking_id": booking_counter,
        "customer_name": req.customer_name,
        "movie": movie["title"],
        "seats": req.seats,
        "seat_type": req.seat_type,
        "original_cost": original,
        "discounted_cost": discounted
    }

    bookings.append(booking)
    booking_counter += 1

    return booking

# ───────── Q11 ─────────
@app.post("/movies", status_code=201)
def create_movie(m: NewMovie):
    for movie in movies:
        if movie["title"].lower() == m.title.lower():
            raise HTTPException(400, "Duplicate title")

    new_movie = m.dict()
    new_movie["id"] = len(movies) + 1
    movies.append(new_movie)
    return new_movie

# ───────── Q12 ─────────
@app.put("/movies/{movie_id}")
def update_movie(movie_id: int,
                 ticket_price: Optional[int] = None,
                 seats_available: Optional[int] = None):

    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(404, "Movie not found")

    if ticket_price is not None:
        movie["ticket_price"] = ticket_price
    if seats_available is not None:
        movie["seats_available"] = seats_available

    return movie

# ───────── Q13 ─────────
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    global movies

    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(404, "Movie not found")

    for b in bookings:
        if b["movie"] == movie["title"]:
            raise HTTPException(400, "Movie has bookings")

    movies = [m for m in movies if m["id"] != movie_id]
    return {"message": "Deleted"}

# ───────── Q14 ─────────
@app.post("/seat-hold")
def hold_seats(customer_name: str, movie_id: int, seats: int):
    global hold_counter

    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(404, "Movie not found")

    if movie["seats_available"] < seats:
        raise HTTPException(400, "Not enough seats")

    movie["seats_available"] -= seats

    hold = {
        "hold_id": hold_counter,
        "customer_name": customer_name,
        "movie_id": movie_id,
        "seats": seats
    }

    holds.append(hold)
    hold_counter += 1

    return hold

@app.get("/seat-hold")
def get_holds():
    return holds

# ───────── Q15 ─────────
@app.post("/seat-confirm/{hold_id}")
def confirm_hold(hold_id: int):
    global booking_counter, holds

    for h in holds:
        if h["hold_id"] == hold_id:
            movie = find_movie(h["movie_id"])

            booking = {
                "booking_id": booking_counter,
                "customer_name": h["customer_name"],
                "movie": movie["title"],
                "seats": h["seats"],
                "seat_type": "standard",
                "original_cost": movie["ticket_price"] * h["seats"],
                "discounted_cost": movie["ticket_price"] * h["seats"]
            }

            bookings.append(booking)
            booking_counter += 1
            holds = [x for x in holds if x["hold_id"] != hold_id]

            return booking

    raise HTTPException(404, "Hold not found")

@app.delete("/seat-release/{hold_id}")
def release_hold(hold_id: int):
    global holds

    for h in holds:
        if h["hold_id"] == hold_id:
            movie = find_movie(h["movie_id"])
            movie["seats_available"] += h["seats"]

            holds = [x for x in holds if x["hold_id"] != hold_id]
            return {"message": "Released"}

    raise HTTPException(404, "Hold not found")

# ───────── Q19 ─────────
@app.get("/bookings/search")
def search_bookings(customer_name: str):
    return [b for b in bookings if customer_name.lower() in b["customer_name"].lower()]

@app.get("/bookings/sort")
def sort_bookings(by: str = "discounted_cost"):
    if by not in ["discounted_cost", "seats"]:
        raise HTTPException(400, "Invalid sort field")
    return sorted(bookings, key=lambda x: x[by])

@app.get("/bookings/page")
def paginate_bookings(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    return bookings[start:start + limit]