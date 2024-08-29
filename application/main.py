"""
Run flask and fasst api here.
"""
from application.api import fast_app
from fastapi.middleware.wsgi import WSGIMiddleware
from application.app import flask_app

fast_app.mount('/app', WSGIMiddleware(flask_app))  # Mount the Flask app object


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:fast_app', reload=True)