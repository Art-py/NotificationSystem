import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.adapters.notifications.api import router as notifications_router

app = FastAPI(
    title='Notification System',
)


@app.get(path='/healthcheck', tags=['System'])
def healthcheck():
    return JSONResponse({'status': 'ok'})


app.include_router(notifications_router)

if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )
