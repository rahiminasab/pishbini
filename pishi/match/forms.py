from django import forms

from ..models import Match, Predict


class SoccerMatchPredictionForm(forms.ModelForm):

    class Meta:
        model = Predict
        fields = ('home_result', 'away_result', 'home_penalty', 'away_penalty')

    def clean(self):
        cleaned_data = super(SoccerMatchPredictionForm, self).clean()
        home_result = cleaned_data.get('home_result')
        away_result = cleaned_data.get('away_result')
        home_penalty = cleaned_data.get('home_penalty')
        away_penalty = cleaned_data.get('away_penalty')
        if (home_penalty or away_penalty) and home_result != away_result:
            raise forms.ValidationError(u'Penalty scores may happen when both teams have equal scores.')
        return cleaned_data

