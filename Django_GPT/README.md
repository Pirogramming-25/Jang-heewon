---

## 📌 주요 기능 (Features)

1. **감정 분석 (Sentiment Analysis)**
   * RoBERTa 모델 기반으로 입력 문장의 긍정/부정 감정 상태 및 확신도(Score) 측정
2. **문서 요약 (Text Summarization)**
   * DistilBART 모델을 이용한 긴 문서 및 뉴스 기사 핵심 요약 기능
3. **유해 표현 분석 (Toxicity Analysis)**
   * Toxic-BERT 기반의 유해 언어, 욕설, 차별적 표현 탐지 및 카테고리별 위험도 평가
4. **복합 분석 (Combo Pipeline)**
   * **유해성 검사 + 요약 + 감정 분석**을 한 번의 요청으로 연속 처리하는 AI 파이프라인
   * 입력 텍스트 제약 조건 검증 (200자 ~ 5,000자) 및 데이터 규격화(Normalization) 처리
   * 분석 결과 종합 판정 문구 및 최근 실행 히스토리 실시간 업데이트
5. **사용자 관리 (User Auth)**
   * 회원가입, 로그인 및 서비스별 접근 권한 제어 (Decorator 기반)
   * 사용자별 AI 추론 이력(Inference History) 저장 및 조회

---

## 🛠 기술 스택 (Tech Stack)

* **Backend**: Python 3.x, Django 5.x
* **Frontend**: HTML5, CSS3, JavaScript (Fetch API, Async/Await)
* **AI/NLP Pipeline**: Hugging Face Transformers, PyTorch, Pre-trained Models (`RoBERTa`, `DistilBART`, `Toxic-BERT`)
* **Version Control**: Git, GitHub

---

## 📁 프로젝트 구조 (Directory Structure)

```text
Django_GPT/
├── config/                  # Django 설정 (settings, urls, wsgi)
├── my_gpt/                  # 메인 앱
│   ├── migrations/          # DB 마이그레이션 파일
│   ├── services/            # AI 모델 추론 및 파이프라인 로직
│   │   ├── combo.py         # 복합 분석 데이터 정형화 및 통합 파이프라인
│   │   ├── moderator.py     # 유해 표현 분석 서비스
│   │   ├── sentiment.py     # 감정 분석 서비스
│   │   └── summarizer.py    # 문서 요약 서비스
│   ├── templates/           # HTML 템플릿
│   ├── static/              # CSS 및 JS 정적 파일
│   ├── views.py             # 비즈니스 로직 및 API 엔드포인트
│   ├── models.py            # 데이터베이스 모델 (InferenceHistory)
│   └── urls.py              # 앱 라우팅 설정
├── manage.py
└── requirements.txt         # 프로젝트 의존성 라이브러리