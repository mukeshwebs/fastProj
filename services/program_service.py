from sqlalchemy.orm import Session
from models.program import Program
from schemas.program import ProgramCreate

# Create a new program
def create_program(db: Session,user_id:int, program_data: ProgramCreate):
    new_program = Program(
        name=program_data.name,
        description=program_data.description,
        created_by=user_id
    )
    db.add(new_program)
    db.commit()
    db.refresh(new_program)
    return new_program

# Get all programs
def get_programs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Program).offset(skip).limit(limit).all()

# Get a single program by ID
def get_program_by_id(db: Session, program_id: int):
    return db.query(Program).filter(Program.id == program_id).first()

# Update an existing program
def update_program(db: Session, program_id: int, updated_data: ProgramCreate):
    program = db.query(Program).filter(Program.id == program_id).first()
    if program:
        program.name = updated_data.name
        program.description = updated_data.description
        db.commit()
        db.refresh(program)
    return program

# Delete a program
def delete_program(db: Session, program_id: int):
    program = db.query(Program).filter(Program.id == program_id).first()
    if program:
        db.delete(program)
        db.commit()
        return True
    return False