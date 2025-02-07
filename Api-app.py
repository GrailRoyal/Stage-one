from fastapi import FastAPI, Query, HTTPException, Request
from typing import Union
import requests
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os  # Import os for environment variables

# Custom Exception
class UnicornException(Exception):
    def __init__(self):
        pass

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development purposes)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Custom Exception Handler
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=400,
        content={"error": True, "number": "alphabet"},
    )

# Helper Functions
def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is perfect."""
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(abs(n))]  # Handle negative numbers
    return sum(d**len(digits) for d in digits) == abs(n)

def get_fun_fact(n: int) -> str:
    """Fetch a fun fact about the number from the Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json")
        if response.status_code == 200:
            return response.json().get("text", "No fun fact available.")
    except:
        pass
    return "No fun fact available."

# API Endpoint
@app.get("/api/classify-number/")
def classify_number(number: Union[int, None] = Query(default=None)):
    """Classify a number and return its properties."""
    if not number:
        raise UnicornException()

    try:
        converted_number = int(number)
    except ValueError:
        raise UnicornException()

    properties = []
    if is_armstrong(converted_number):
        properties.append("armstrong")
    properties.append("odd" if converted_number % 2 else "even")

    return {
        "number": number,
        "is_prime": is_prime(converted_number),
        "is_perfect": is_perfect(converted_number),
        "properties": properties,
        "digit_sum": sum(int(digit) for digit in str(abs(converted_number)) if digit.isdigit()),
        "fun_fact": get_fun_fact(converted_number),
    }

# Run Server
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT or default to 5000
    uvicorn.run(app, host="0.0.0.0", port=port)
