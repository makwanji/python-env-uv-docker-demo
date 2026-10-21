from fastapi import FastAPI
import platform

app = FastAPI(title="Hello API", version="1.0.0")


@app.get("/")
def hello():
    return {
        "message": "Hello World from API!",
        "python_version": platform.python_version(),
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
