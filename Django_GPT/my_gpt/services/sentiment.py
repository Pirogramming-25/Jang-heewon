from functools import lru_cache
from transformers import pipeline
from .common import get_pipeline_device


# 1. 감정 분석 모델 최초 1회 로딩 및 캐싱
@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    """
    Twitter RoBERTa 감정 분석 모델을 로딩하고 캐싱하는 함수 (최초 1회만 로드됨)
    """
    print("감정 분석 모델 로딩 중...")
    pipe = pipeline(
        task="text-classification",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        top_k=None,  # 모든 레이블(Positive, Neutral, Negative)의 점수를 가져오기 위해 필수
        device=get_pipeline_device(),  # 공통 디바이스 적용
    )
    print("모델 로딩 완료!")
    return pipe


# 2. 감정 분석 실행 함수
def analyze_twitter_sentiment(text: str, return_all_scores: bool = False):
    """
    Twitter RoBERTa 감정 분석 서비스 함수
    - return_all_scores=False: 대표 감정 + 신뢰도 출력
    - return_all_scores=True: 모든 레이블의 신뢰도 출력
    """
    # @lru_cache 덕분에 몇 번을 호출해도 모델은 1번만 로드되고 기존 객체를 재사용함
    classifier = get_sentiment_pipeline()
    predictions = classifier(text)[0]  # 예: [{'label': 'positive', 'score': 0.9248}, ...]

    # 레이블 명칭 첫 글자 대문자화 및 데이터 가공
    formatted_results = []
    for item in predictions:
        label_name = item['label'].capitalize()  # 'positive' -> 'Positive'
        score_percentage = round(item['score'] * 100, 2)  # 소수점 2자리 퍼센트
        formatted_results.append({
            'label': label_name,
            'score': score_percentage
        })

    # 방식 1: 대표 감정 1개 + 신뢰도만 출력하는 경우
    if not return_all_scores:
        top_result = formatted_results[0]
        return f"감정: {top_result['label']}\n신뢰도: {top_result['score']}%"

    # 방식 2: 모든 레이블의 점수를 출력하는 경우
    else:
        output_lines = [f"{res['label']}: {res['score']}%" for res in formatted_results]
        return "\n".join(output_lines)