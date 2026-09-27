import os
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.schemas import WorkoutRequest
from app.database import SessionLocal, User, WorkoutPlan, save_user, save_plan, update_plan, get_original_plan
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(os.path.dirname(BASE_DIR), "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})

@router.post("/generate-workout/gemini")
async def generate_gemini_workout(request: WorkoutRequest):
    try:
        result = generate_workout_gemini({
            "goal": request.goal,
            "intensity": request.intensity
        })
        return {"model": "local-rules", "workout_plan": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/nutrition-tip")
def get_flash_tip(goal: str):
    tip = generate_nutrition_tip_with_flash(goal)
    return {"goal": goal, "nutrition_tip": tip}

@router.post("/generate-plan", response_class=HTMLResponse)
def generate_plan_form(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    try:
        save_user(
            user_id=user_id,
            name=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )
        plan = generate_workout_gemini({
            "goal": goal,
            "intensity": intensity
        })
        save_plan(user_id, plan)
        nutrition_tip = generate_nutrition_tip_with_flash(goal)

        return templates.TemplateResponse(request, "result.html", {
            "request": request,
            "username": username,
            "user_id": user_id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": plan,
            "nutrition_tip": nutrition_tip
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...)
):
    original = get_original_plan(user_id)
    if not original:
        return templates.TemplateResponse(request, "result.html", {
            "request": request,
            "error": "Original plan not found for this user ID.",
            "workout_plan": "",
            "nutrition_tip": ""
        })
    
    updated = update_workout_plan(original, feedback)
    update_plan(user_id, updated)

    db = SessionLocal()
    user = db.query(User).filter_by(id=user_id).first()
    db.close()

    return templates.TemplateResponse(request, "result.html", {
        "request": request,
        "username": user.name if user else "User",
        "user_id": user_id,
        "age": user.age if user else 0,
        "weight": user.weight if user else 0.0,
        "goal": user.goal if user else "",
        "intensity": user.intensity if user else "",
        "workout_plan": updated,
        "nutrition_tip": "Check your updated plan based on feedback!",
        "success_message": "Your plan has been updated based on your feedback!"
    })

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    db = SessionLocal()
    users = db.query(User).all()
    user_data = []
    for user in users:
        plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user.id).first()
        user_data.append({
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "original_plan": plan.original_plan if plan else "N/A",
            "updated_plan": plan.updated_plan if plan and plan.updated_plan else "Not updated"
        })
    db.close()
    return templates.TemplateResponse(request, "all_users.html", {
        "request": request,
        "users": user_data
    })