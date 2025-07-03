from rest_framework.permissions import BasePermission


class IsTrainer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_trainer

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsMentor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_mentor

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsApprentice(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_apprentice

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsApprenticeOrTrainer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_trainer or request.user.is_apprentice

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsMentorOrTrainer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_trainer or request.user.is_mentor

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
