from fastapi import FastAPI, Depends, UploadFile, File
from app.database import SessionLocal
from app.models import User, Report
from app.schemas import UserCreate, UserLogin
from app.security import hash_password, verify_password
from app.jwt_handler import create_access_token
from app.dependencies import get_current_user
import shutil
import os
from app.pdf_reader import extract_text_from_pdf
from app.ai_analyzer import analyze_medical_report
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
import os
from dotenv import load_dotenv

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
print("MAIN.PY GEMINI:", os.getenv("GEMINI_API_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://medical-report-assistant.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Hello, Medical Report Assistant!"}


@app.post("/register")
def register(user: UserCreate):
    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        db.close()
        return {"message": "Email already registered"}

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return {"message": "User registered successfully"}


@app.post("/login")
def login(user: UserLogin):
    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    db.close()

    if not existing_user:
        return {"message": "Invalid email or password"}

    if verify_password(user.password, existing_user.password):
        access_token = create_access_token(
            data={"sub": existing_user.email}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    return {"message": "Invalid email or password"}


@app.get("/profile")
def profile(current_user: str = Depends(get_current_user)):
    return {
        "message": "Welcome!",
        "email": current_user
    }


@app.post("/upload-report")
def upload_report(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):
    print("STEP 1: Upload request received")

    upload_folder = "uploads"

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, file.filename)

    print("STEP 2: Saving PDF")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("STEP 3: PDF saved")

    try:
        print("STEP 4: Extracting PDF text")
        extracted_text = extract_text_from_pdf(file_path)
        print("STEP 5: PDF text extracted")
    except Exception as e:
        print("PDF ERROR:", e)
        raise

    try:
        print("STEP 6: Calling Gemini")
        analysis = analyze_medical_report(extracted_text)
        print("STEP 7: Gemini finished")
    except Exception as e:
        print("GEMINI ERROR:", e)
        raise

    db = SessionLocal()

    print("STEP 8: Finding user")

    logged_in_user = db.query(User).filter(
        User.email == current_user
    ).first()

    print("STEP 9: User found")

    try:
        new_report = Report(
            filename=file.filename,
            filepath=file_path,
            analysis=analysis,
            user_id=logged_in_user.id
        )

        db.add(new_report)
        db.commit()
        db.refresh(new_report)

        print("STEP 10: Database saved")

    except Exception as e:
        print("DATABASE ERROR:", e)
        raise

    finally:
        db.close()

    print("STEP 11: Returning response")

    return {
        "message": "Report uploaded successfully",
        "filename": file.filename,
        "analysis": analysis
    }

@app.get("/my-reports")
def my_reports(current_user: str = Depends(get_current_user)):
    db = SessionLocal()

    logged_in_user = db.query(User).filter(
        User.email == current_user
    ).first()

    reports = db.query(Report).filter(
        Report.user_id == logged_in_user.id
    ).all()

    result = []

    for report in reports:
        result.append({
            "id": report.id,
            "filename": report.filename,
            "analysis": report.analysis
        })

    db.close()

    return result
@app.delete("/report/{report_id}")
def delete_report(
    report_id: int,
    current_user: str = Depends(get_current_user)
):
    db = SessionLocal()

    # Find the logged-in user
    logged_in_user = db.query(User).filter(
        User.email == current_user
    ).first()

    # Find the report
    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == logged_in_user.id
    ).first()

    if not report:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    # Delete PDF file if it exists
    if os.path.exists(report.filepath):
        os.remove(report.filepath)

    # Delete database record
    db.delete(report)
    db.commit()
    db.close()

    return {
        "message": "Report deleted successfully"
    }
@app.get("/dashboard")
def dashboard(current_user: str = Depends(get_current_user)):
    db = SessionLocal()

    logged_in_user = db.query(User).filter(
        User.email == current_user
    ).first()

    reports = db.query(Report).filter(
        Report.user_id == logged_in_user.id
    ).all()

    total_reports = len(reports)

    latest_report = None

    if reports:
        latest_report = reports[-1].filename

    db.close()

    return {
        "total_reports": total_reports,
        "latest_report": latest_report
    }