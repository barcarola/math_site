from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.core.validators import MinValueValidator, MaxValueValidator

choices1 = (('count10', "Сложение до 10"), ('subtr10', "Вычитание до 10"), ('equation10', "Уравнения до 10"), ('multiplication', "Умножение"))

exercises_options_errors = {
    "required": "Нужно выбрать, что тренируем"
}

total_option_errors = {
    "required": "Нужно указать сколько примеров",
    "max_value": "Должно быть меньше 50",
    'min_value': "Должно быть больше 5"
}


class SettingsForm(forms.Form):

    primery_eto_ya = forms.MultipleChoiceField(choices=choices1, widget=CheckboxSelectMultiple(), required=True, label="Что тренируем?", error_messages=exercises_options_errors)
    total = forms.IntegerField(label="Всего примеров", widget=forms.NumberInput(attrs={"id": "user_settings_input"}), validators=[MinValueValidator(5), MaxValueValidator(50)], error_messages=total_option_errors, required=True)

