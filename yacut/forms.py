from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import (
    DataRequired, Length, Optional, Regexp,
    ValidationError
)

from .constants import API_REGEX, ORIGINAL_MAX_LENGTH, SHORT_MAX_LENGTH
from .models import URLMap

FORMS_LONG_LINK = 'Длинная ссылка'
FORMS_REQUIRED = 'Обязательное поле'
FORMS_YOUR_SHORT_LINK = 'Ваш вариант короткой ссылки'
FORMS_SHORT_LINK_VALIDATION = 'Короткая ссылка может быть не более 16 символов'
FORMS_CREATE = 'Создать'
FLASH_NAME_EXISTS = 'Имя {} уже занято!'


class CutForm(FlaskForm):
    original_link = StringField(
        FORMS_LONG_LINK,
        validators=[DataRequired(message=FORMS_REQUIRED),
                    Length(max=ORIGINAL_MAX_LENGTH)]
    )
    custom_id = StringField(
        FORMS_YOUR_SHORT_LINK,
        validators=[
            Optional(),
            Length(
                max=SHORT_MAX_LENGTH,
                message=FORMS_SHORT_LINK_VALIDATION
            ),
            Regexp(
                API_REGEX,
                message=FORMS_SHORT_LINK_VALIDATION
            ),
        ]
    )
    submit = SubmitField(FORMS_CREATE)

    def validate_custom_id(self, field):
        if field.data:
            if URLMap.get(short=field.data):
                raise ValidationError(
                    FLASH_NAME_EXISTS.format(field.data)
                )
