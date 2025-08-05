import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="192.168.0.110", port=9000, reload=True)
