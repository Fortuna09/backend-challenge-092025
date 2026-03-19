from fastapi import FastAPI
from fastapi.responses import JSONResponse

from sentiment_analyzer import ValidationErrorInfo, analyze_feed


# cria a aplicacao principal
app = FastAPI(title="MBRAS Backend Challenge", version="1.0.0")


@app.post("/analyze-feed")
def analyze_feed_endpoint(payload: dict):
    # processa o payload e converte erros em respostas padronizadas
    try:
        return analyze_feed(payload)
    except ValidationErrorInfo as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.error,
                "code": exc.code,
            },
        )
