from fastapi import APIRouter
from pydantic import BaseModel
from app.services.predictor import predict_news
from app.utils.scraper import extract_article_text
from app.feedback.feedback_store import save_feedback

router = APIRouter()

# -------- Request Models --------
class TextReq(BaseModel):
    text: str

class URLReq(BaseModel):
    url: str

class FeedbackReq(BaseModel):
    text: str
    model_prediction: str
    user_feedback: int


# -------- Prediction Endpoints --------
@router.post("/predict/text")
def predict_text(req: TextReq):
    return predict_news(req.text)


@router.post("/predict/url")
def predict_url(req: URLReq):
    article_text = extract_article_text(req.url)

    if not article_text or len(article_text) < 200:
        return {"error": "Could not extract article"}

    return predict_news(article_text, source_url=req.url)



# -------- Feedback Endpoint --------
@router.post("/feedback")
def feedback(req: FeedbackReq):
    save_feedback(
        req.text,
        req.model_prediction,
        req.user_feedback
    )
    return {"status": "feedback recorded"}
