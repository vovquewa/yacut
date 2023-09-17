from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (CUSTOM_ID_MAX_LENGTH, FORMS_CREATE, FORMS_LONG_LINK,
                        FORMS_REQUIRED, FORMS_SHORT_LINK_VALIDATION,
                        FORMS_YOUR_SHORT_LINK, ORIGINAL_MAX_LENGTH, API_REGEX)


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
                max=CUSTOM_ID_MAX_LENGTH,
                message=FORMS_SHORT_LINK_VALIDATION
            ),
            Regexp(
                API_REGEX,
                message=FORMS_SHORT_LINK_VALIDATION
            )
        ]
    )
    submit = SubmitField(FORMS_CREATE)
