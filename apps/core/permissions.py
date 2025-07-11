from rest_framework.permissions import BasePermission


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

class IsMentorOrApprentice(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_mentor or request.user.is_apprentice)

    def has_object_permission(self, request, view, obj):
        return (obj.mentor.user == request.user) or (obj.apprentice.user == request.user)


class IsTrainerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_trainer or request.user.is_staff)


class IsApprenticeOrTrainerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_trainer
            or request.user.is_apprentice
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsMentorOrTrainerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_trainer or request.user.is_mentor or request.user.is_staff
        )
