from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "UP"}, status_code=200)


@app.get("/version")
def version_check():
    return JSONResponse(content={"version": "0.2.4"}, status_code=200)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)
