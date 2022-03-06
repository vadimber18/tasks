import uvicorn

from app import app

if __name__ == "__main__":
    uvicorn.run(app, host=app.config.app_host, port=app.config.app_port)
