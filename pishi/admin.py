from django.contrib import admin
from models import *


class TeamAdmin(admin.ModelAdmin):
    pass


class MatchAdmin(admin.ModelAdmin):
    pass


class PredictAdmin(admin.ModelAdmin):
    pass


admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Predict, PredictAdmin)
