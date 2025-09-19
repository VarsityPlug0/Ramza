from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Menu Items
    path('menu-items/', views.menu_items, name='menu_items'),
    path('menu-items/add/', views.edit_menu_item, name='add_menu_item'),
    path('menu-items/edit/<int:item_id>/', views.edit_menu_item, name='edit_menu_item'),
    path('menu-items/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    
    # Categories
    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.edit_category, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    
    # Orders
    path('orders/', views.orders, name='orders'),
    path('orders/update-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    
    # Site Settings
    path('settings/', views.site_settings, name='site_settings'),
]