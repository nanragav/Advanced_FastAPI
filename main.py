from fastapi import FastAPI, HTTPException
import logging
import uvicorn
from routers import user_router
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

ssl_keyfile = os.path.join(current_dir, "certs", "key.pem")
ssl_certfile = os.path.join(current_dir, "certs", "cert.pem")


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

    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True, ssl_keyfile=ssl_keyfile, ssl_certfile=ssl_certfile)