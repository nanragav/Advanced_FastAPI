from fastapi import FastAPI, HTTPException
import logging
import uvicorn
from routers import user_router

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(user_router.router)

@app.get('/')
async def root():

    try:

        return {'message': 'FastAPI is running'}

    except Exception as e:

        logger.error(f'Error in Root Endpoint {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')


if __name__ == '__main__':

    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)