from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешает создавать, удалять, изменять
    объект только пользователю с ролью admin, остальным доступно
    только чтение.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin)
                )


class IsAdminAuthorModeratorOrReadOnly(permissions.BasePermission):
    """Разрешает:
    - moderator, admin - право удалять и редактировать любые отзывы и
    комментарии.
    - author - создателю объекта разрешено удаление и редактирование
    созданного объекта.
    - остальным только чтение
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or obj.author == request.user
                or request.user.is_moderator
                )

class IsAdminOrForbidden(permissions.BasePermission):
    """Разрешает создавать, удалять, изменять
    объект только пользователю с ролью admin.
    """
    def has_permission(self, request, view):
        return request.user.is_admin
