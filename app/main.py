from fastapi import FastAPI

app = FastAPI(title="Airport Delay API")

@app.get("/")
def home():
    return {"message": "Airport Delay API is running"}
