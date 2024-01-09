from fastapi import FastAPI

app = FastAPI(docs_url='/docs')


@app.get('/')
def index():
    return {'message': 'Success'}

@app.get('/api/{message}')
def get_any_message(message: str):
    return {'message': message }



