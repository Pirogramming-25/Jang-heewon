from django import forms

class AnalysisForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, min_length=1, max_length=1000, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_length = min_length
        self.max_length = max_length

    def clean_content(self):
        content = self.cleaned_data.get('content')

        # 1. 예기치 않은 데이터 타입 체크
        if not isinstance(content, str):
            raise forms.ValidationError("올바른 문자열 형식이 아닙니다.")

        # 2. 공백 제거 후 빈 문자열 및 공백만 입력했는지 체크
        stripped_content = content.strip()
        if not stripped_content:
            raise forms.ValidationError("공백을 제외한 내용을 입력해 주세요.")

        # 3. 최소 길이 검증
        if len(stripped_content) < self.min_length:
            raise forms.ValidationError(f"최소 {self.min_length}자 이상 입력해야 합니다. (현재 {len(stripped_content)}자)")

        # 4. 최대 길이 검증
        if len(stripped_content) > self.max_length:
            raise forms.ValidationError(f"최대 {self.max_length}자까지 입력 가능합니다. (현재 {len(stripped_content)}자)")

        return stripped_content