from .summarizer import summarize_text
from .sentiment import analyze_twitter_sentiment
from .moderator import analyze_toxicity

def process_combo(text: str) -> dict:
    mod_result = analyze_toxicity(text)
    summary_result = summarize_text(text)
    sentiment_result = analyze_twitter_sentiment(text)

    # 1. 유해성 검사 결과 타입 처리
    if isinstance(mod_result, dict):
        is_flagged = mod_result.get('flagged', False)
        highest_label = mod_result.get('highest_label', 'clean')
        toxicity_score = mod_result.get('score', 0.0)
        all_scores = mod_result.get('all_scores', {})
    else:
        is_flagged = False
        highest_label = str(mod_result)
        toxicity_score = 0.0
        all_scores = {}

    # 2. 요약 결과 타입 처리
    if isinstance(summary_result, dict):
        summary_text_out = summary_result.get('summary_text', str(summary_result))
    else:
        summary_text_out = str(summary_result)

    # 3. 감정 분석 결과 타입 처리
    if isinstance(sentiment_result, dict):
        sentiment_label = sentiment_result.get('label', 'N/A')
        sentiment_score = sentiment_result.get('score', 0.0)
    else:
        sentiment_label = str(sentiment_result)
        sentiment_score = 0.0

    # 4. 종합 판정 문구 생성
    if is_flagged:
        overall_verdict = f"주의: 유해 표현이 감지되었습니다. (위험 유형: {highest_label})"
    else:
        overall_verdict = f"안전: 유해 표현이 감지되지 않은 정상 텍스트입니다. (감정: {sentiment_label})"

    # 5. 프론트엔드 맞춤 결과 반환
    return {
        'original_text': text,
        'summary': summary_text_out,
        'sentiment': {
            'label': sentiment_label,
            'score': sentiment_score
        },
        'toxicity': {
            'highest_label': highest_label,
            'score': toxicity_score,
            'all_scores': all_scores
        },
        'overall_verdict': overall_verdict
    }