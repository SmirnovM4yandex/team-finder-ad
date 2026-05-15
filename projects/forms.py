from django import forms

from core.constants import PROJECT_DESCRIPTION_ROWS
from projects.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project

        fields = [
            "name",
            "description",
            "github_url",
            "status",
        ]

        labels = {
            "name": "Название",
            "description": "Описание",
            "github_url": "GitHub",
            "status": "Статус",
        }

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": PROJECT_DESCRIPTION_ROWS,
                }
            ),
        }
