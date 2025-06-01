from django.urls import path
from . import views

urlpatterns = [
    # Record management URLs
    path('', views.record_list, name='record_list'),
    path('add/', views.add_record, name='add_record'),
    path('edit-record/<int:pk>/', views.edit_record, name='edit_record'),
    path('delete/<int:pk>/', views.delete_record, name='delete_record'),
    
    # Dynamic data loading URLs
    path('get_categories/', views.get_categories, name='get_categories'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
    
    # Quick-add functionality URLs
    path('status/quick-add/', views.quick_add_status, name='quick_add_status'),
    path('type/quick-add/', views.quick_add_type, name='quick_add_type'),
    path('category/quick-add/', views.quick_add_category, name='quick_add_category'),
    path('subcategory/quick-add/', views.quick_add_subcategory, name='quick_add_subcategory'),
]