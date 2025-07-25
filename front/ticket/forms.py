from django import forms


class CreateTicketForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(), label="Текст заявки", required=True)
    status = forms.ChoiceField(choices=[("Created", "Создана")], label="Статус заявки")
    department = forms.ChoiceField(
        choices=(),
        label="Служба",
    )
    subdivisions = forms.MultipleChoiceField(
        choices=(), widget=forms.CheckboxSelectMultiple()
    )

    def __init__(
        self, *args, department_choices=None, subdivissions_choises=None, **kwargs
    ):
        super().__init__(*args, **kwargs)
        if department_choices:
            # Например: [(1, "Дитис"), (2, "Департмент"), …]
            self.fields["department"].choices = department_choices
        else:
            # Если не передали – оставляем пустой выбор или можем добавить пустой пункт:
            self.fields["department"].choices = [("", "— выберите подразделение —")]
        if subdivissions_choises:
            # Например: [(1, "Дитис"), (2, "Департмент"), …]
            self.fields["subdivisions"].choices = subdivissions_choises
        else:
            # Если не передали – оставляем пустой выбор или можем добавить пустой пункт:
            self.fields["subdivisions"].choices = [("", "— выберите подразделение —")]
