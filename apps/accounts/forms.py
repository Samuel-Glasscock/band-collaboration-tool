from allauth.account.forms import LoginForm, SignupForm

class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = "form-control"
            if field.widget.input_type == "checkbox":
                css = "form-check-input"
            field.widget.attrs.update({"class": css})

class MySignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = "form-control"
            if field.widget.input_type == "checkbox":
                css = "form-check-input"
            field.widget.attrs.update({"class": css})