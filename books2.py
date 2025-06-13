from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book(): #Books as class-obj 
    id : int
    title : str
    author : str
    description : str
    rating : int
    published_date : int

    def __init__(self,id,title,author,description,rating, published_date): #init to initialise const
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id : Optional[int] = Field(description='ID is not needed on create', default = None)
    title : str = Field(min_length=3)
    author : str = Field(min_length=1)
    description : str = Field(min_length=1, max_length=100)
    rating : int = Field(gt=0,lt=6)
    published_date : int = Field(gt = 1999, lt = 2025)

    #To add specific example value in Swagger UI
    model_config = {
        "json_schema_extra": {
            "example" : {
                "title" : "A new book",
                "author" : "codingwithsreshta",
                "description" : "A new description",
                "rating" : 5,
                "published_date" : 2024 # type: ignore
            }
        }
    }




BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithsreshta', 'A very nice book', 5, 2020 ),
    Book(2, 'Fast with FastAPI', 'codingwithsreshta', 'A great book', 5, 2020 ),
    Book(3, 'Master Endpoints', 'codingwithsreshta', 'A awesome book', 5, 2019 ),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2017 ),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2017 ),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2016 )

]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


#Find a book based on book.id
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id : int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')
        
        
#Fetch all books filtered by ratings passing a query parameter 'rating'
#Does not interfere with the previous get - since his is a query parameter 
#Would've interfered if this also had an extra path parameter added next to books - books/{book_rating}
@app.get("/books/",status_code=status.HTTP_200_OK)
async def filter_books_by_rating(book_rating : int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

#Assignment 2 copied here due to order
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(published_date : int = Query(gt = 1999, lt = 2025)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request : BookRequest):
    new_book = Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


#Put Request Method - Update a book
@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book : BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True #Exception Handling Instance
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')

    


#Delete request Method - Delete a book
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id : int = Path(gt = 0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')



#ASSIGNMENT 2
#ADD A NEW FIELD - published_date: int to Book, BookRequest
#Enhance each book to have published_date
#Create a get request method -  to filter by published_date

''' Added published_date in the class Book Obj, BookRequest, Model config'''

