from django import forms
from .models import Income, Expense, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'date', 'description', 'category']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'date', 'description', 'category']


# tracker/forms.py

from .models import Budget

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month', 'year']
