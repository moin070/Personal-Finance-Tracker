from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  # Ensure this points to the correct login view
    path('logout/', views.logout_view, name='logout'),  # This should now work

    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='tracker/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='tracker/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='tracker/password_reset_complete.html'), name='password_reset_complete'),

    path('add_income/', views.add_income, name='add_income'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('edit_income/<int:income_id>/', views.edit_income, name='edit_income'),
    path('edit_expense/<int:expense_id>/', views.edit_expense, name='edit_expense'),


    path('financial_reports/', views.financial_reports, name='financial_reports'),
    path('set_budget/', views.set_budget, name='set_budget'),
    path('export_to_excel/', views.export_to_excel, name='export_to_excel'),
    path('export_to_pdf/', views.export_to_pdf, name='export_to_pdf'),


    path('delete_expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('delete_income/<int:income_id>/', views.delete_income, name='delete_income'),


]

