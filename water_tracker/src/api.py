from fastapi import FastAPI
from pydantic import BaseModel
from src.agent import WaterIntakeAgent
from src.database import log_intake, get_intake_history
from src.logger import log_message

app = FastAPI()
agents = WaterIntakeAgent()

class WaterIntakeRequest(BaseModel):
    user_id : str
    intake_ml: int


# @app.post('/log-intake')
# async def log_water_intake(request: WaterIntakeRequest):
#     log_intake(request.user_id, request.intake_ml)
    
#     analysis = agents.analyze_intake(request.intake_ml)
#     log_message(f'user {request.user_id} logged {request.intake_ml}ml')
#     return {'message': 'Water intake logged successfully', 'analysis': analysis}
@app.post('/log-intake')
async def log_water_intake(request: WaterIntakeRequest):
    log_intake(request.user_id, request.intake_ml)
    
    analysis = agents.analyze_intake(request.intake_ml)
    log_message(f'user {request.user_id} logged {request.intake_ml}ml')
    
    return {
        'message': 'Water intake logged successfully',
        'user_id': request.user_id,
        'intake_ml': request.intake_ml,
        'analysis': analysis
    }


# @app.get('/history/{user_id}')
# async def get_water_history(user_id:str):
#     history = get_intake_history(user_id)
#     return {'user_ID':user_id, 'history': history}


@app.get('/history/{user_id}')
async def get_water_history(user_id: str):
    history = get_intake_history(user_id)
    
    formatted_history = [
        {'date': date, 'intake_ml': intake_ml}
        for intake_ml, date in history
    ]
    
    return {
        'user_id': user_id,
        'history': formatted_history,
        #'total_days': len(formatted_history),
        'total_intake_ml': sum(item['intake_ml'] for item in formatted_history)
    }
