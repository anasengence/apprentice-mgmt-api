from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


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


class IsTrainerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_trainer or request.user.is_staff)


class IsApprenticeOrTrainer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_trainer or request.user.is_apprentice

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsMentorOrTrainer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_trainer or request.user.is_mentor
