from django import forms

from ..models import Match, Predict


class SoccerMatchPredictionForm(forms.ModelForm):

    class Meta:
        model = Predict
        fields = ('home_result', 'away_result', 'home_penalty', 'away_penalty')

    def __init__(self, *args, **kwargs):
        self.match = kwargs.pop('match', '')
        super(SoccerMatchPredictionForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SoccerMatchPredictionForm, self).clean()
        if self.match.due:
            raise forms.ValidationError(u'You cannot predict a match which has been started/finished')
        home_result = cleaned_data.get('home_result')
        away_result = cleaned_data.get('away_result')
        home_penalty = cleaned_data.get('home_penalty')
        away_penalty = cleaned_data.get('away_penalty')
        if (home_penalty or away_penalty) and home_result != away_result:
            raise forms.ValidationError(u'Penalty scores may happen when both teams have equal scores.')
        return cleaned_data

