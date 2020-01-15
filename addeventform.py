from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, optional


class EventForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Event', validators=[DataRequired()])
    picture = FileField("Picture")
    submit = SubmitField('Add Entry')

    def __init__(self, edit=None):
        super().__init__()
        try:
            self.title.label = edit[1]
            self.title.validators = [optional()]
            self.content.label = edit[2]
            self.content.validators = [optional()]
        except:
            pass
