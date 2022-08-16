from django import forms
from .models import Statistics


class StatisticsForm(forms.Form):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    sleep_hours = forms.IntegerField(label="sleep_hours")
    javascript_hours = forms.IntegerField()
    python_hours = forms.IntegerField()
    mathematics_learning_time = forms.IntegerField()
    javascript_testing_hours = forms.IntegerField()
    python_testing_hours = forms.IntegerField()

    class Meta:
        """_summary_
        """
        model = Statistics
        labels = [
            "sleep_hours",
            "javascript_hours",
            "python_hours",
            "mathematics_learning_time",
            "javascript_testing_hours",
            "python_testing_hours",
        ]