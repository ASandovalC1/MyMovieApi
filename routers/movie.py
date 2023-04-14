from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse

from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middelwares.jwt_bearer import JWTBearer
from services.movie  import MovieService
from schemas.movie import Movie


movie_router = APIRouter()




@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies() ->List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message":"No se encontro la pelicula"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['movies'] , response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) ->List[Movie]:
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={"message":"No se encontro la categoria"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
    
    
@movie_router.post('/movies', tags=['movies'], response_model=dict ,status_code=201)
def create_movie(movie:Movie) -> dict:
    db = Session() #Se crea una instancia de la base de datos
    MovieService(db).create_movie(movie) #Se llama al servicio para crear la pelicula
    # new_movie = MovieModel(**movie.dict()) #Se crea una instancia de la clase MovieModel
    # db.add(new_movie) #Se agrega la instancia a la base de datos
    # db.commit() #Se confirma la transacción
    return JSONResponse(status_code=201, content={"message":"Se registro la pelicula"})

@movie_router.put('/movies', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id:int , movie:Movie)-> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message":"No se encontro la pelicula"})
    
    MovieService(db).update_movie(id, movie)
    
    return JSONResponse(status_code=200,content={"message":"Se modifico la pelicula"})

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int)-> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message":"No se encontro la pelicula"})
    
    MovieService(db).delete_movie(id)
    
    
    return JSONResponse(status_code=200, content={"message":"Se elimino la pelicula"})