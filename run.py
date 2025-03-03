import uvicorn
from app.settings import settings


def run():
    if settings.environment in ["development", "qa", "production"]:
        # In production/qa/dev environment, without reloading
        uvicorn.run("app.main:app", host="0.0.0.0", port=8001)
    else:
        # In local environment, enable reloading
        uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)

if __name__ == "__main__":
    run()
