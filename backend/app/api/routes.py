from fastapi import APIRouter
from pydantic import BaseModel
from app.services.predictor import predict_news
from app.utils.scraper import extract_article_text

router = APIRouter()

class TextReq(BaseModel):
    text: str

class URLReq(BaseModel):
    url: str


@router.post("/predict/text")
def predict_text(req: TextReq):
    return predict_news(req.text)


@router.post("/predict/url")
def predict_url(req: URLReq):
    text = extract_article_text(req.url)

    if not text or len(text) < 200:
        return {"error": "Could not extract article"}

    return predict_news(text, source_url=req.url)
