from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import item_router, category_router, auth_router,user_router
app = FastAPI(title="POS Backend")

# ------------------------------
# CORS setup
# ------------------------------
origins = [
    "http://localhost:3000",  # your frontend origin
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allow requests from these origins
    allow_credentials=True,
    allow_methods=["*"],    # allow GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],    # allow all headers
)

# ------------------------------
# Include Routers
# ------------------------------
app.include_router(item_router.router)
app.include_router(category_router.router)
app.include_router(auth_router.router)
app.include_router(user_router.router)

@app.get("/")
def root():
    return {"message": "POS Backend is running!"}