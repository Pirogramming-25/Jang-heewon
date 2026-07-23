from functools import lru_cache
from transformers import pipeline
from .common import get_pipeline_device


# 1. 모델 최초 1회 로딩 및 캐싱을 위한 함수
@lru_cache(maxsize=1)
def get_moderation_pipeline():
    """
    유해 표현 분석 모델을 로딩하고 캐싱하는 함수 (최초 1회만 로드됨)
    """
    print("유해 표현 분석 모델(unitary/toxic-bert) 로딩 중...")
    pipe = pipeline(
        task="text-classification",
        model="unitary/toxic-bert",
        top_k=None,  # 모든 레이블의 점수를 가져오기 위해 필수
        device=get_pipeline_device(),  # 공통 디바이스 적용
    )
    print("유해 표현 모델 로딩 완료!")
    return pipe


# 2. 유해 표현 분석 수행 함수
def analyze_toxicity(text: str, return_all_sorted: bool = True) -> str:
    """
    toxic-bert 모델을 활용한 유해 표현 분석 함수
    - return_all_sorted=True: 전체 레이블을 점수가 높은 순서대로 정렬하여 출력 (권장)
    - return_all_sorted=False: 최고 위험 레이블과 위험 점수만 출력
    """
    # @lru_cache 덕분에 몇 번을 호출해도 모델은 1번만 로드되고 기존 객체를 재사용함
    moderator = get_moderation_pipeline()
    predictions = moderator(text)[0]  # 예: [{'label': 'insult', 'score': 0.7843}, ...]

    # 1. 점수가 높은 순서대로 내림차순 정렬
    sorted_predictions = sorted(predictions, key=lambda x: x['score'], reverse=True)

    # 2. 방식 1: 전체 레이블 점수를 높은 순서대로 정렬해 출력
    if return_all_sorted:
        lines = []
        for item in sorted_predictions:
            label = item['label']
            score = round(item['score'] * 100, 2)
            lines.append(f"{label}: {score}%")
        return "\n".join(lines)

    # 3. 방식 2: 최고 위험 레이블 및 위험 점수만 출력
    else:
        top_item = sorted_predictions[0]
        top_label = top_item['label']
        top_score = round(top_item['score'] * 100, 2)
        return f"최고 위험 레이블: {top_label}\n위험 점수: {top_score}%"