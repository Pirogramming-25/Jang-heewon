from functools import lru_cache
from transformers import pipeline
from .common import get_pipeline_device


# @lru_cache(maxsize=1)를 사용해 최초 1회 실행 결과를 메모리에 저장(캐싱)
@lru_cache(maxsize=1)
def get_summarize_pipeline():
    """
    문서 요약 모델을 로딩하고 캐싱하는 함수 (최초 1회만 로드됨)
    """
    print("문서 요약 모델(distilbart-cnn-6-6) 로딩 중...")
    pipe = pipeline(
        task="summarization",
        model="sshleifer/distilbart-cnn-6-6",
        device=get_pipeline_device(),  # 디바이스 추가 추천
    )
    print("요약 모델 로딩 완료!")
    return pipe


def summarize_text(text: str) -> str:
    """
    문서 요약 실행 후 지정된 요구사항 포맷으로 결과를 반환하는 함수
    """
    # @lru_cache 덕분에 몇 번을 호출해도 모델은 1번만 로드되고 기존 객체를 재사용함
    summarizer = get_summarize_pipeline()

    # 1. 요약 실행
    summary_result = summarizer(
        text, max_length=130, min_length=30, do_sample=False
    )
    summary_text = summary_result[0]["summary_text"].strip()

    # 2. 길이 및 비율 계산
    original_len = len(text)
    summary_len = len(summary_text)

    # 요약 비율 계산 공식: (summary_len / original_len) * 100
    ratio = (summary_len / original_len) * 100 if original_len > 0 else 0.0

    # 3. 요구사항에 맞춘 출력 문자열 생성
    output_text = (
        f"원문 길이: {original_len:,}자\n"
        f"요약문 길이: {summary_len:,}자\n"
        f"요약 비율: {ratio:.2f}%\n\n"
        f"요약 결과:\n{summary_text}"
    )

    return output_text