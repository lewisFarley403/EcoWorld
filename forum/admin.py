from django.contrib import admin
from .models import Post, PostInteraction
from django.db.models import Count, Case, When, IntegerField

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_type', 'visibility', 'created_at', 'get_likes', 'get_dislikes', 'get_ratio')
    list_filter = ('post_type', 'visibility', 'created_at')
    search_fields = ('user__username', 'post_type')
    date_hierarchy = 'created_at'

    def get_likes(self, obj):
        return obj.interactions.filter(interaction_type='like').count()
    get_likes.short_description = 'Likes'

    def get_dislikes(self, obj):
        return obj.interactions.filter(interaction_type='dislike').count()
    get_dislikes.short_description = 'Dislikes'

    def get_ratio(self, obj):
        likes = self.get_likes(obj)
        dislikes = self.get_dislikes(obj)
        if likes + dislikes == 0:
            return "N/A"
        return f"{dislikes/(likes + dislikes):.2%}"
    get_ratio.short_description = 'Dislike Ratio'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            like_count=Count(Case(
                When(interactions__interaction_type='like', then=1),
                output_field=IntegerField(),
            )),
            dislike_count=Count(Case(
                When(interactions__interaction_type='dislike', then=1),
                output_field=IntegerField(),
            ))
        )
        return queryset.order_by('-dislike_count', '-created_at')

@admin.register(PostInteraction)
class PostInteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'interaction_type', 'created_at')
    list_filter = ('interaction_type', 'created_at')
    search_fields = ('user__username', 'post__user__username')
    date_hierarchy = 'created_at'
