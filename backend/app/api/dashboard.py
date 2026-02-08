from fastapi import APIRouter 

router = APIRouter()


@router.post('/poll/create')
def poll_create():
    return {"message": "poll creation endpoint"}

@router.get('/poll/view')
def poll_view():
    return {"message": "poll view endpoint"}

@router.get('/poll/result')
def poll_result():
    return {"message": "poll result endpoint"}
