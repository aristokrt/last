from rest_framework.permissions import BasePermission


class IsNotAuthenticated(BasePermission):
	def has_object_permission(self, request, view, obj):
		return not request.user.is_authenticated
