from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "instock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "instock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "instock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "instock": True},
    {"id": 5, "name": "Laptop Stand", "price": 200, "category": "Electronics", "instock": False},
    {"id": 6, "name": "Mechanical Keyboard", "price": 800, "category": "Electronics", "instock": True},
    {"id": 7, "name": "Webcam", "price": 1500, "category": "Electronics", "instock": True},
]
# Temporary data acting as our database for now


# Endpoint 0 - Home
@app.get("/")
def home():
    return {"message": "Welcome to our E-commerce API"}


# Endpoint 1 - Return all products
@app.get("/products")
def get_all_products():
    return {"products": products, "total": len(products)}


# Endpoint 2 - Return instock products
@app.get("/products/instocks")
def products_instock():
    list_instock = [product for product in products if product["instock"] == True]
    return {"In stock Products": list_instock, "Total Instock": len(list_instock)}


# Endpoint 3 - Cheapest & Most Expensive Product (Deals)
@app.get("/products/deals")
def get_deals():
    cheapest = min(products, key=lambda p: p["price"])
    expensive = max(products, key=lambda p: p["price"])
    return {"best_deal": cheapest, "premium_pick": expensive}


# Endpoint 4 - Return one product by its ID
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {"product": product}
    return {"error": "Product not found"}


# Endpoint 5 - Return products by category
@app.get("/products/category/{category}")
def get_product_category(category: str):
    list_category = [product for product in products if product["category"] == category]
    if len(list_category) != 0:
        return {"category": category, "products": list_category, "total": len(list_category)}
    else:
        return {"error": "No products found in this category"}


# Endpoint 6 - Get Store Summary
@app.get("/store/summary")
def get_store_summary():
    total_products = len(products)
    instock_count = 0
    outstock_count = 0
    category_list = []
    for product in products:
        if product["instock"] == True:
            instock_count += 1
        else:
            outstock_count += 1
        if product["category"] not in category_list:
            category_list.append(product["category"])
    return {
        "Store Name": "My E-commerce Store",
        "Total products": total_products,
        "in_stock": instock_count,
        "out_of_stock": outstock_count,
        "categories": category_list
    }


# Endpoint 7 - Search Product by name
@app.get("/products/search/{keyword}")
def get_search_products(keyword: str):
    list_products = [product for product in products if keyword.lower() in product["name"].lower()]
    if len(list_products) != 0:
        return {"Keyword": keyword, "List Category of Search": list_products, "Total Matches": len(list_products)}
    else:
        return {"Message": "No products matched in search"}
