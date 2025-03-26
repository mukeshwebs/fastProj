from fastapi import FastAPI
from db.database import init_db,get_db
from routes import auth, program,session,community,post,comment,booking,goal,progress,rag

app = FastAPI()
app.include_router(auth.router)
app.include_router(program.router)
app.include_router(session.router)
app.include_router(community.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(booking.router)
app.include_router(goal.router)
app.include_router(progress.router)
app.include_router(rag.router)

@app.on_event("startup")
def startup():
    init_db()  # Create tables on startup
    get_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to ConnectFit API"}