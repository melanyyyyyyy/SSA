from django.contrib.auth.decorators import user_passes_test

def professor_required(view_func=None, redirect_field_name=None, login_url='login'):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_professor(),  
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    return actual_decorator(view_func) if view_func else actual_decorator

def student_required(view_func=None, redirect_field_name=None, login_url='login'):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_student(),  
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    return actual_decorator(view_func) if view_func else actual_decorator