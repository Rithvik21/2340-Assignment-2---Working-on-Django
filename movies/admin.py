from django.contrib import admin
from .models import Movie, Review, MoviePetition, PetitionVote

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class PetitionVoteInline(admin.TabularInline):
    model = PetitionVote
    extra = 0
    readonly_fields = ['user', 'created_at']

class MoviePetitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'vote_count', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['title', 'description', 'created_by__username']
    ordering = ['-created_at']
    inlines = [PetitionVoteInline]
    readonly_fields = ['created_at']
    
    def vote_count(self, obj):
        return obj.vote_count
    vote_count.short_description = 'Votes'

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(MoviePetition, MoviePetitionAdmin)
admin.site.register(PetitionVote)