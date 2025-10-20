from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
from typing import Dict, List, Optional

app = FastAPI(title="EcoScan Test API")

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/scan")
def scan_get(barcode: str):
    """Test endpoint for barcode scanning"""
    # Simple mock response
    score = 75
    breakdown = {
        "carbon": 15,
        "water": 8,
        "other": 2
    }
    return {"barcode": barcode, "score": score, "breakdown": breakdown}

@app.get("/")
def root():
    return {"message": "EcoScan API is running!"}

def search_real_products(query: str) -> List[Dict]:
    """Search for real products using various APIs and web scraping"""
    products = []
    
    try:
        # 1. Always try OpenFoodFacts API first (most reliable)
        food_products = search_openfoodfacts(query)
        if food_products:
            products.extend(food_products)
        
        # 2. Search using Edamam API for food products (backup)
        if not products:
            edamam_products = search_edamam_foods(query)
            products.extend(edamam_products)
        
        # 3. Search using Spoonacular API for recipes/food
        if not products:
            spoonacular_products = search_spoonacular(query)
            products.extend(spoonacular_products)
        
        # 4. Generate dynamic products based on query if no real products found
        if not products:
            dynamic_products = generate_dynamic_products(query)
            products.extend(dynamic_products)
        
    except Exception as e:
        print(f"Error searching real products: {e}")
        # Fallback: generate dynamic products
        products = generate_dynamic_products(query)
    
    return products

def search_openfoodfacts(query: str) -> List[Dict]:
    """Search OpenFoodFacts database for food products"""
    try:
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&search_simple=1&action=process&json=1"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            products = []
            for item in data.get('products', [])[:3]:  # Limit to 3 results
                if item.get('product_name') and len(item.get('product_name', '')) > 2:
                    # Calculate sustainability score based on available data
                    score = calculate_food_sustainability_score(item)
                    products.append({
                        "id": f"off_{item.get('code', '')}",
                        "name": item.get('product_name', 'Unknown Product'),
                        "brand": item.get('brands', 'Unknown Brand'),
                        "category": "food",
                        "score": score,
                        "breakdown": {
                            "carbon": max(0, 50 - score),
                            "water": max(0, 30 - score),
                            "other": max(0, 20 - score)
                        },
                        "image": item.get('image_url', ''),
                        "alternatives": []
                    })
            return products
    except Exception as e:
        print(f"Error searching OpenFoodFacts: {e}")
    return []

def search_edamam_foods(query: str) -> List[Dict]:
    """Search Edamam API for food products"""
    try:
        # Free tier API (limited requests)
        app_id = "demo_id"  # You would need to register for a real API key
        app_key = "demo_key"
        url = f"https://api.edamam.com/api/food-database/v2/parser?app_id={app_id}&app_key={app_key}&ingr={query}"
        
        # For demo purposes, return mock data
        return []
    except Exception as e:
        print(f"Error searching Edamam: {e}")
    return []

def search_spoonacular(query: str) -> List[Dict]:
    """Search Spoonacular API for food products"""
    try:
        # Free tier API (limited requests)
        api_key = "demo_key"  # You would need to register for a real API key
        url = f"https://api.spoonacular.com/food/products/search?query={query}&apiKey={api_key}"
        
        # For demo purposes, return mock data
        return []
    except Exception as e:
        print(f"Error searching Spoonacular: {e}")
    return []

def generate_dynamic_products(query: str) -> List[Dict]:
    """Generate dynamic products based on query when no real products are found"""
    products = []
    query_lower = query.lower()
    
    # Create realistic product variations based on the search query
    variations = [
        f"{query} Original",
        f"{query} Premium",
        f"{query} Eco-Friendly",
        f"{query} Organic",
        f"{query} Sustainable"
    ]
    
    brands = ["Generic", "EcoBrand", "GreenChoice", "SustainableCo", "EcoFriendly"]
    
    for i, variation in enumerate(variations[:3]):
        # Generate realistic sustainability score based on keywords
        score = calculate_query_sustainability_score(query_lower)
        
        # Adjust score based on variation
        if "eco" in variation.lower() or "sustainable" in variation.lower() or "organic" in variation.lower():
            score = min(100, score + 20)
        elif "premium" in variation.lower():
            score = min(100, score + 10)
        
        products.append({
            "id": f"dynamic_{i}",
            "name": variation,
            "brand": brands[i % len(brands)],
            "category": determine_category(query_lower),
            "score": score,
            "breakdown": {
                "carbon": max(0, 50 - score),
                "water": max(0, 30 - score),
                "other": max(0, 20 - score)
            },
            "image": "",
            "alternatives": []
        })
    
    return products

def calculate_query_sustainability_score(query: str) -> int:
    """Calculate sustainability score based on query keywords"""
    score = 50  # Base score
    
    # Positive keywords
    positive_keywords = [
        'organic', 'eco', 'green', 'sustainable', 'recycled', 'biodegradable',
        'renewable', 'fair trade', 'local', 'natural', 'plant-based', 'vegan'
    ]
    
    # Negative keywords
    negative_keywords = [
        'plastic', 'disposable', 'single-use', 'toxic', 'chemical', 'synthetic',
        'artificial', 'processed', 'industrial', 'mass-produced'
    ]
    
    for keyword in positive_keywords:
        if keyword in query:
            score += 15
    
    for keyword in negative_keywords:
        if keyword in query:
            score -= 20
    
    return min(100, max(0, score))

def determine_category(query: str) -> str:
    """Determine product category based on query"""
    if any(keyword in query for keyword in ['food', 'drink', 'beverage', 'snack', 'cereal', 'organic']):
        return 'food'
    elif any(keyword in query for keyword in ['phone', 'computer', 'laptop', 'tablet', 'electronic']):
        return 'electronics'
    elif any(keyword in query for keyword in ['clothes', 'shoes', 'shirt', 'pants', 'dress']):
        return 'clothing'
    elif any(keyword in query for keyword in ['car', 'vehicle', 'automotive', 'tesla']):
        return 'automotive'
    else:
        return 'general'

def get_products_by_category(category: str) -> List[Dict]:
    """Get all products in a specific category"""
    category_products = {
        'electronics': [
            {"id": "elec_1", "name": "iPhone 15 Pro", "brand": "Apple", "category": "electronics", "score": 85, "breakdown": {"carbon": 12, "water": 6, "other": 3}, "image": "", "alternatives": []},
            {"id": "elec_2", "name": "Samsung Galaxy S24", "brand": "Samsung", "category": "electronics", "score": 72, "breakdown": {"carbon": 15, "water": 8, "other": 5}, "image": "", "alternatives": []},
            {"id": "elec_3", "name": "MacBook Pro M3", "brand": "Apple", "category": "electronics", "score": 68, "breakdown": {"carbon": 20, "water": 7, "other": 5}, "image": "", "alternatives": []},
            {"id": "elec_4", "name": "iPad Air", "brand": "Apple", "category": "electronics", "score": 75, "breakdown": {"carbon": 14, "water": 6, "other": 5}, "image": "", "alternatives": []},
            {"id": "elec_5", "name": "Google Pixel 8", "brand": "Google", "category": "electronics", "score": 80, "breakdown": {"carbon": 11, "water": 5, "other": 4}, "image": "", "alternatives": []},
            {"id": "elec_6", "name": "Dell XPS 13", "brand": "Dell", "category": "electronics", "score": 65, "breakdown": {"carbon": 18, "water": 9, "other": 8}, "image": "", "alternatives": []},
            {"id": "elec_7", "name": "AirPods Pro", "brand": "Apple", "category": "electronics", "score": 70, "breakdown": {"carbon": 16, "water": 7, "other": 7}, "image": "", "alternatives": []},
            {"id": "elec_8", "name": "Sony WH-1000XM5", "brand": "Sony", "category": "electronics", "score": 73, "breakdown": {"carbon": 15, "water": 8, "other": 4}, "image": "", "alternatives": []}
        ],
        'food': [
            {"id": "food_1", "name": "Coca Cola Classic", "brand": "Coca Cola", "category": "food", "score": 25, "breakdown": {"carbon": 45, "water": 25, "other": 5}, "image": "", "alternatives": []},
            {"id": "food_2", "name": "Beyond Meat Burger", "brand": "Beyond Meat", "category": "food", "score": 82, "breakdown": {"carbon": 12, "water": 4, "other": 2}, "image": "", "alternatives": []},
            {"id": "food_3", "name": "Organic Quinoa", "brand": "Nature's Path", "category": "food", "score": 90, "breakdown": {"carbon": 5, "water": 3, "other": 2}, "image": "", "alternatives": []},
            {"id": "food_4", "name": "Fair Trade Coffee", "brand": "Equal Exchange", "category": "food", "score": 85, "breakdown": {"carbon": 8, "water": 4, "other": 3}, "image": "", "alternatives": []},
            {"id": "food_5", "name": "Local Honey", "brand": "Local Farm", "category": "food", "score": 95, "breakdown": {"carbon": 2, "water": 2, "other": 1}, "image": "", "alternatives": []},
            {"id": "food_6", "name": "Organic Avocado", "brand": "Earthbound Farm", "category": "food", "score": 78, "breakdown": {"carbon": 12, "water": 8, "other": 2}, "image": "", "alternatives": []},
            {"id": "food_7", "name": "Plant-Based Milk", "brand": "Oatly", "category": "food", "score": 88, "breakdown": {"carbon": 7, "water": 3, "other": 2}, "image": "", "alternatives": []},
            {"id": "food_8", "name": "Sustainable Tuna", "brand": "Wild Planet", "category": "food", "score": 72, "breakdown": {"carbon": 15, "water": 8, "other": 5}, "image": "", "alternatives": []}
        ],
        'clothing': [
            {"id": "cloth_1", "name": "Nike Air Max 270", "brand": "Nike", "category": "clothing", "score": 45, "breakdown": {"carbon": 35, "water": 15, "other": 5}, "image": "", "alternatives": []},
            {"id": "cloth_2", "name": "Patagonia Better Sweater", "brand": "Patagonia", "category": "clothing", "score": 88, "breakdown": {"carbon": 8, "water": 3, "other": 1}, "image": "", "alternatives": []},
            {"id": "cloth_3", "name": "Allbirds Tree Runners", "brand": "Allbirds", "category": "clothing", "score": 85, "breakdown": {"carbon": 10, "water": 4, "other": 1}, "image": "", "alternatives": []},
            {"id": "cloth_4", "name": "Veja V-10 Sneakers", "brand": "Veja", "category": "clothing", "score": 82, "breakdown": {"carbon": 12, "water": 5, "other": 1}, "image": "", "alternatives": []},
            {"id": "cloth_5", "name": "Organic Cotton T-Shirt", "brand": "Pact", "category": "clothing", "score": 90, "breakdown": {"carbon": 5, "water": 4, "other": 1}, "image": "", "alternatives": []},
            {"id": "cloth_6", "name": "Recycled Denim Jeans", "brand": "Outerknown", "category": "clothing", "score": 75, "breakdown": {"carbon": 15, "water": 8, "other": 2}, "image": "", "alternatives": []},
            {"id": "cloth_7", "name": "Hemp Hoodie", "brand": "Patagonia", "category": "clothing", "score": 92, "breakdown": {"carbon": 4, "water": 3, "other": 1}, "image": "", "alternatives": []},
            {"id": "cloth_8", "name": "Wool Base Layer", "brand": "Icebreaker", "category": "clothing", "score": 80, "breakdown": {"carbon": 12, "water": 6, "other": 2}, "image": "", "alternatives": []}
        ],
        'automotive': [
            {"id": "auto_1", "name": "Tesla Model 3", "brand": "Tesla", "category": "automotive", "score": 78, "breakdown": {"carbon": 18, "water": 4, "other": 0}, "image": "", "alternatives": []},
            {"id": "auto_2", "name": "Toyota Prius", "brand": "Toyota", "category": "automotive", "score": 85, "breakdown": {"carbon": 12, "water": 2, "other": 1}, "image": "", "alternatives": []},
            {"id": "auto_3", "name": "BMW i3", "brand": "BMW", "category": "automotive", "score": 72, "breakdown": {"carbon": 20, "water": 5, "other": 3}, "image": "", "alternatives": []},
            {"id": "auto_4", "name": "Nissan Leaf", "brand": "Nissan", "category": "automotive", "score": 80, "breakdown": {"carbon": 15, "water": 3, "other": 2}, "image": "", "alternatives": []},
            {"id": "auto_5", "name": "Hyundai Ioniq", "brand": "Hyundai", "category": "automotive", "score": 75, "breakdown": {"carbon": 18, "water": 4, "other": 3}, "image": "", "alternatives": []},
            {"id": "auto_6", "name": "Ford Mustang Mach-E", "brand": "Ford", "category": "automotive", "score": 70, "breakdown": {"carbon": 22, "water": 5, "other": 3}, "image": "", "alternatives": []}
        ],
        'beauty': [
            {"id": "beauty_1", "name": "Organic Face Cream", "brand": "Dr. Bronner's", "category": "beauty", "score": 85, "breakdown": {"carbon": 8, "water": 4, "other": 3}, "image": "", "alternatives": []},
            {"id": "beauty_2", "name": "Cruelty-Free Shampoo", "brand": "Aveda", "category": "beauty", "score": 80, "breakdown": {"carbon": 12, "water": 6, "other": 2}, "image": "", "alternatives": []},
            {"id": "beauty_3", "name": "Natural Deodorant", "brand": "Native", "category": "beauty", "score": 88, "breakdown": {"carbon": 6, "water": 3, "other": 3}, "image": "", "alternatives": []},
            {"id": "beauty_4", "name": "Reef-Safe Sunscreen", "brand": "All Good", "category": "beauty", "score": 92, "breakdown": {"carbon": 4, "water": 3, "other": 1}, "image": "", "alternatives": []}
        ],
        'home': [
            {"id": "home_1", "name": "LED Light Bulbs", "brand": "Philips", "category": "home", "score": 90, "breakdown": {"carbon": 5, "water": 2, "other": 3}, "image": "", "alternatives": []},
            {"id": "home_2", "name": "Smart Thermostat", "brand": "Nest", "category": "home", "score": 85, "breakdown": {"carbon": 8, "water": 3, "other": 4}, "image": "", "alternatives": []},
            {"id": "home_3", "name": "Bamboo Cutting Board", "brand": "Bambu", "category": "home", "score": 95, "breakdown": {"carbon": 2, "water": 2, "other": 1}, "image": "", "alternatives": []},
            {"id": "home_4", "name": "Reusable Water Bottle", "brand": "Hydro Flask", "category": "home", "score": 88, "breakdown": {"carbon": 6, "water": 4, "other": 2}, "image": "", "alternatives": []}
        ]
    }
    
    return category_products.get(category, [])

# Removed problematic scraping function - using dynamic product generation instead

def calculate_food_sustainability_score(product_data: Dict) -> int:
    """Calculate sustainability score for food products based on available data"""
    score = 50  # Base score
    
    # Check for organic certification
    if 'organic' in str(product_data.get('labels_tags', [])).lower():
        score += 20
    
    # Check for sustainable packaging
    packaging = str(product_data.get('packaging', '')).lower()
    if any(eco in packaging for eco in ['recyclable', 'biodegradable', 'compostable']):
        score += 15
    
    # Check for fair trade
    if 'fair trade' in str(product_data.get('labels_tags', [])).lower():
        score += 10
    
    # Check for local production
    origins = str(product_data.get('origins', '')).lower()
    if any(local in origins for local in ['local', 'regional', 'domestic']):
        score += 5
    
    return min(100, max(0, score))

@app.get("/api/search")
def search_products(q: str = "", category: str = "", brand: str = "", sustainability: str = ""):
    """Search for products by name, brand, category, or sustainability rating"""
    all_products = []
    
    # If category is specified but no query, show all products in that category
    if category and not q:
        all_products = get_products_by_category(category)
    # If query is provided, search for products
    elif q:
        # Try to find real products first
        real_products = search_real_products(q)
        all_products = real_products.copy()
    
    # Always add mock products for demonstration
    products_db = [
        {
            "id": 1,
            "name": "iPhone 15 Pro",
            "brand": "Apple",
            "category": "electronics",
            "score": 85,
            "breakdown": {"carbon": 12, "water": 6, "other": 3},
            "image": "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=400",
            "alternatives": [
                {"name": "iPhone 15 Pro (Refurbished)", "score": 92},
                {"name": "Fairphone 5", "score": 95}
            ]
        },
        {
            "id": 2,
            "name": "Tesla Model 3",
            "brand": "Tesla",
            "category": "automotive",
            "score": 78,
            "breakdown": {"carbon": 18, "water": 4, "other": 0},
            "image": "https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=400",
            "alternatives": [
                {"name": "Tesla Model 3 (Used)", "score": 88},
                {"name": "BYD Atto 3", "score": 82}
            ]
        },
        {
            "id": 3,
            "name": "Nike Air Max 270",
            "brand": "Nike",
            "category": "clothing",
            "score": 45,
            "breakdown": {"carbon": 35, "water": 15, "other": 5},
            "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
            "alternatives": [
                {"name": "Allbirds Tree Runners", "score": 85},
                {"name": "Veja V-10", "score": 82}
            ]
        },
        {
            "id": 4,
            "name": "Coca Cola Classic",
            "brand": "Coca Cola",
            "category": "food",
            "score": 25,
            "breakdown": {"carbon": 45, "water": 25, "other": 5},
            "image": "https://images.unsplash.com/photo-1581636625402-29b2a704ef13?w=400",
            "alternatives": [
                {"name": "La Croix Sparkling Water", "score": 75},
                {"name": "Topo Chico Mineral Water", "score": 68}
            ]
        },
        {
            "id": 5,
            "name": "Samsung Galaxy S24",
            "brand": "Samsung",
            "category": "electronics",
            "score": 72,
            "breakdown": {"carbon": 15, "water": 8, "other": 5},
            "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400",
            "alternatives": [
                {"name": "Samsung Galaxy S24 (Refurbished)", "score": 88},
                {"name": "Google Pixel 8", "score": 85}
            ]
        },
        {
            "id": 6,
            "name": "MacBook Pro M3",
            "brand": "Apple",
            "category": "electronics",
            "score": 68,
            "breakdown": {"carbon": 20, "water": 7, "other": 5},
            "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400",
            "alternatives": [
                {"name": "MacBook Pro M3 (Refurbished)", "score": 85},
                {"name": "Framework Laptop 16", "score": 92}
            ]
        },
        {
            "id": 7,
            "name": "Patagonia Better Sweater",
            "brand": "Patagonia",
            "category": "clothing",
            "score": 88,
            "breakdown": {"carbon": 8, "water": 3, "other": 1},
            "image": "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400",
            "alternatives": [
                {"name": "Patagonia Better Sweater (Used)", "score": 95},
                {"name": "Arcteryx Atom LT", "score": 82}
            ]
        },
        {
            "id": 8,
            "name": "Beyond Meat Burger",
            "brand": "Beyond Meat",
            "category": "food",
            "score": 82,
            "breakdown": {"carbon": 12, "water": 4, "other": 2},
            "image": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=400",
            "alternatives": [
                {"name": "Impossible Burger", "score": 78},
                {"name": "Black Bean Burger (Homemade)", "score": 95}
            ]
        }
    ]
    
    # Add mock products to the search pool
    all_products.extend(products_db)
    
    # Filter products based on search query and filters
    filtered_products = []
    
    for product in all_products:
        # Check if product matches search query (only if query is provided)
        matches_query = True
        if q:
            query_lower = q.lower()
            matches_query = (
                query_lower in product["name"].lower() or
                query_lower in product["brand"].lower() or
                query_lower in product["category"].lower()
            )
        
        # Check category filter
        matches_category = not category or product["category"] == category
        
        # Check brand filter
        matches_brand = not brand or product["brand"].lower() == brand.lower()
        
        # Check sustainability filter
        matches_sustainability = True
        if sustainability:
            if sustainability == "excellent" and product["score"] < 80:
                matches_sustainability = False
            elif sustainability == "good" and (product["score"] < 60 or product["score"] >= 80):
                matches_sustainability = False
            elif sustainability == "fair" and (product["score"] < 40 or product["score"] >= 60):
                matches_sustainability = False
            elif sustainability == "poor" and product["score"] >= 40:
                matches_sustainability = False
        
        if matches_query and matches_category and matches_brand and matches_sustainability:
            filtered_products.append(product)
    
    # Sort by relevance (exact matches first, then by score)
    if q:
        query_lower = q.lower()
        filtered_products.sort(key=lambda x: (
            -1 if query_lower in x["name"].lower() else 0,
            -x["score"]
        ))
    else:
        # Sort by score when no query is provided
        filtered_products.sort(key=lambda x: -x["score"])
    
    return filtered_products

@app.get("/api/suggestions")
def get_suggestions(q: str):
    """Get search suggestions based on query"""
    # Mock suggestions - in a real app, this would use a search index
    all_suggestions = [
        {"name": "iPhone 15 Pro", "brand": "Apple"},
        {"name": "iPhone 15", "brand": "Apple"},
        {"name": "Tesla Model 3", "brand": "Tesla"},
        {"name": "Tesla Model Y", "brand": "Tesla"},
        {"name": "Nike Air Max 270", "brand": "Nike"},
        {"name": "Nike Air Force 1", "brand": "Nike"},
        {"name": "Coca Cola Classic", "brand": "Coca Cola"},
        {"name": "Samsung Galaxy S24", "brand": "Samsung"},
        {"name": "Samsung Galaxy S23", "brand": "Samsung"},
        {"name": "MacBook Pro M3", "brand": "Apple"},
        {"name": "MacBook Air M2", "brand": "Apple"},
        {"name": "Patagonia Better Sweater", "brand": "Patagonia"},
        {"name": "Beyond Meat Burger", "brand": "Beyond Meat"}
    ]
    
    query_lower = q.lower()
    suggestions = []
    
    for suggestion in all_suggestions:
        if query_lower in suggestion["name"].lower() or query_lower in suggestion["brand"].lower():
            suggestions.append(suggestion)
    
    # Limit to 5 suggestions
    return suggestions[:5]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
