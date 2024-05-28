def admin_check(user):
    return user.is_superuser or user.is_staff  # Assuming admins are either superusers or staff