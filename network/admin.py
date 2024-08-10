from django.contrib import admin

from network import models as network_models 


class FriendRequestAdmin(admin.options.ModelAdmin):
    list_select_related = ('sender', 'recipient')

class UserFriendAdmin(admin.options.ModelAdmin):
    list_select_related = ('user', 'friend')


admin.site.register(network_models.FriendRequest, FriendRequestAdmin)
admin.site.register(network_models.UserFriend, UserFriendAdmin)
