from fastapi import FastAPI
from legalaseAPI.routes import router

app = FastAPI(
    title="LegalEase - AI Legal Document Generator",
    version="1.0.0",
    description="Generate editable legal-document drafts with AI."
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "message": "Welcome to LegalEase AI Legal Document Generator API",
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
