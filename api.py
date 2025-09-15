import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi import APIRouter

app = FastAPI(
    title = "SUI API",
    description = "An API to lookup Scratch user IDs via their usernames, and vice versa if necessary.",
    version = "1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(
    tags=["API"]
)

@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs", status_code=301)

DATABASE_FILE = "sui_usernames.db"


def query_db(query, args=(), one=False):
    con = sqlite3.connect(DATABASE_FILE)
    cur = con.cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
            for i, value in enumerate(row)) for row in cur.fetchall()]
    con.close()
    return (r[0] if r else None) if one else r


@router.get(
        "/user/{username}",
        summary="Search user ID.",
        responses = {
            404: {
                "description": "Username not found (in database).",
                "content": {
                    "application/json": {
                        "example": {"detail": "User not found"}
                    }
                },
            },
            200: {
                "description": "User ID found.",
                "content": {
                    "application/json": {
                        "example": {"username": "buddy", "user_id": 1234}
                    }
                },
            },
        }
    )
async def get_user_id(username: str):
    """
    Look up a user's ID by their username.
    """
    user = query_db("SELECT * FROM users WHERE username = ?", [username], one=True)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found") [20]
    return user

@router.get(
        "/id/{user_id}",
        summary="Search username.",
        responses = {
            404: {
                "description": "User ID not found (in database).",
                "content": {
                    "application/json": {
                        "example": {"detail": "User ID not found"}
                    }
                },
            },
            200: {
                "description": "Username found.",
                "content": {
                    "application/json": {
                        "example": {"username": "buddy", "user_id": 1234}
                    }
                },
            },
        }
    )
async def get_username(user_id: int):
    """
    Look up a username by their user ID.
    """
    user = query_db("SELECT * FROM users WHERE user_id = ?", [user_id], one=True)
    if user is None:
        raise HTTPException(status_code=404, detail="User ID not found") [20]
    return user

app.include_router(router, prefix="/v1")