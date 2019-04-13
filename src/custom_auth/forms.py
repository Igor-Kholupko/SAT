from django.forms import ModelForm

from custom_auth.models import User, Student, Teacher


class TeacherPersonalInfoForm(ModelForm):
    class Meta:
        model = Teacher
        exclude = ('user', )


class StudentPersonalInfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentPersonalInfoForm, self).__init__(*args, **kwargs)
        self.fields['faculty'].widget.attrs['readonly'] = True
        self.fields['speciality'].widget.attrs['readonly'] = True
        self.fields['year_of_studying'].widget.attrs['readonly'] = True
        self.fields['group'].widget.attrs['readonly'] = True

    class Meta:
        model = Student
        exclude = ('user',)


class UserPersonalInfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserPersonalInfoForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['readonly'] = True
        self.fields['surname'].widget.attrs['readonly'] = True
        self.fields['patronymic'].widget.attrs['readonly'] = True

    class Meta:
        model = User
        fields = ('first_name', 'surname', 'patronymic', 'email', 'phone_number')
