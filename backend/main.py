from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import upload, doc_query

Port = 8000

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(doc_query.router)

@app.get("/health")
async def read_health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=Port)
