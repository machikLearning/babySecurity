from django.core.exceptions import ValidationError
import re

class MinimumLengthValidator:
    def __init__(self, minLength=10):
        self.minLength = minLength

    def validate(self, password, user=None):
        if len(password) < self.minLength:
            raise ValidationError(
                code='password_too_short',
                params ={ 'minimumLength' : self.minLength}
            )

        letterPattern = re.compile("\D")
        integerPattern = re.compile("\d")

        if not letterPattern.match(password) and not integerPattern.match(password):
            raise ValidationError(
                code='조합이 잘못되었습니다',
            )

    def get_help_text(self):
        return ("10자리 이상 및 숫자와 영문조합의 비밀번호여야 합니다")