from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict
from datetime import datetime, UTC
from sqlalchemy import create_engine, Column, Integer, Boolean, String, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

DATABASE = "sqlite:///./tasks.db"

app = FastAPI()

engine = create_engine(
    DATABASE,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)


class Base(DeclarativeBase):
    pass

class Taskdb(Base):
    __tablename__ = "tasks"
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    is_done = Column(Boolean, default=False)
    time_of_creation = Column(DateTime, nullable=False)

class Task(BaseModel):
    id: int
    title: str
    is_done: bool
    time_of_creation: datetime

    model_config = ConfigDict(from_attributes=True)

Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

@app.get("/tasks", response_model=list[Task])
async def get_tasks(db:Session = Depends(get_db)):
    return db.query(Taskdb).all()

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int, db:Session = Depends(get_db)):
    task = db.query(Taskdb).filter(Taskdb.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found!")
    return task

@app.post("/tasks", response_model=Task)
async def create_task(title: str, db:Session = Depends(get_db)):
    data = {
        "title": title,
        "is_done": False,
        "time_of_creation": datetime.now(UTC)
    }

    task = Taskdb(**data)
    db.add(task)
    db.commit()
    return task

@app.patch("/tasks/{task_id}", response_model=Task)
async def complete_task(task_id: int, db:Session = Depends(get_db)):
    task = db.query(Taskdb).filter(Taskdb.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found!")
    setattr(task, "is_done",True)
    db.commit()
    return task


@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int, db:Session = Depends(get_db)):
    task = db.query(Taskdb).filter(Taskdb.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found!")
    
    db.delete(task)
    db.commit()
    return task

@app.delete("/completed", response_model=int)
async def delete_completed_tasks(db:Session = Depends(get_db)):
    task = db.query(Taskdb).filter(Taskdb.is_done == True).delete()

    db.commit()
    return task