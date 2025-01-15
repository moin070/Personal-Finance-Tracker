from django.shortcuts import render


from .forms import IncomeForm, ExpenseForm
from .models import Income, Expense
# Create your views here.
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login


from django.contrib.auth import logout




from django.db.models import Sum
from django.utils import timezone
from .models import Income, Expense, Budget
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})

from django.shortcuts import render
from .models import Income, Expense


def homepage(request):
    incomes = Income.objects.all()
    expenses = Expense.objects.all()
    return render(request, 'tracker/homepage.html', {'incomes': incomes, 'expenses': expenses})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')  # Redirect to homepage or any other page
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'tracker/login.html')





# Custom password reset view
def password_reset_request(request):
    if request.method == "POST":
        # Check if the form is valid
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            messages.success(request, "Password reset email has been sent.")
            return render(request, "tracker/password_reset_done.html")
        else:
            messages.error(request, "Please enter a valid email address.")
    else:
        form = PasswordResetForm()

    return render(request, "tracker/password_reset.html", {"form": form})




# Logout view
def logout_view(request):
    logout(request)  # Logs the user out
    return redirect('login')  # Redirects to the login page after logout




# views.py

from django.contrib.auth.decorators import login_required

@login_required  # Ensures only logged-in users can access this view
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            # Set the user before saving the form
            income = form.save(commit=False)
            income.user = request.user  # Associate the logged-in user
            income.save()
            return redirect('homepage')  # Redirect to the homepage after saving
    else:
        form = IncomeForm()

    return render(request, 'tracker/add_income.html', {'form': form})



@login_required 
def delete_income(request, income_id):
    try:
        # Fetch the specific income object for the logged-in user
        income = get_object_or_404(Income, id=income_id, user=request.user)
        income.delete()  # Delete the income object
        return redirect('homepage')  # Redirect to the homepage or the desired page
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")  # Debugging response



from django.contrib.auth.decorators import login_required
import datetime


@login_required
def add_expense(request):
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    # Get user's budget for the current month and year
    user_budget = Budget.objects.filter(user=request.user, month=current_month, year=current_year).first()

    # Get total expenses for the current month and year
    total_expenses = Expense.objects.filter(user=request.user, date__month=current_month, date__year=current_year).aggregate(Sum('amount'))['amount__sum'] or 0

    # Check if total expenses exceed the user's budget
    if user_budget and total_expenses > user_budget.amount:
        # Notify the user or show a warning
        messages.warning(request, 'You have exceeded your budget for this month!')

    # Process the form submission (e.g., adding a new expense)
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Assign the current user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('homepage')  # Redirect to the same page or another view
    else:
        form = ExpenseForm()

    return render(request, 'tracker/add_expense.html', {
        'total_expenses': total_expenses,
        'user_budget': user_budget,
        'form': form,
    })



from django.shortcuts import get_object_or_404, redirect

@login_required 
def delete_expense(request, expense_id):
    try:
        print(f"Expense ID: {expense_id}, Logged-in User: {request.user}")
        
        expense = get_object_or_404(Expense, id=expense_id, user=request.user)
        print(f"Expense found: {expense}")
        
        expense.delete()
        return redirect('homepage')  # Or your desired page
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")  # Debugging response



@login_required 
def edit_income(request, income_id):
    income = Income.objects.get(id=income_id)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('homepage')  # Redirect to homepage after updating the income
    else:
        form = IncomeForm(instance=income)
    return render(request, 'tracker/edit_income.html', {'form': form, 'income': income})


@login_required 
def edit_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('homepage')  # Redirect to homepage after updating the expense
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'tracker/edit_expense.html', {'form': form, 'expense': expense})




@login_required 
def financial_reports(request):
    current_month = timezone.now().month
    current_year = timezone.now().year
    
    monthly_income = Income.objects.filter(date__month=current_month).aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_expenses = Expense.objects.filter(date__month=current_month).aggregate(Sum('amount'))['amount__sum'] or 0

    yearly_income = Income.objects.filter(date__year=current_year).aggregate(Sum('amount'))['amount__sum'] or 0
    yearly_expenses = Expense.objects.filter(date__year=current_year).aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'tracker/financial_reports.html', {
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'yearly_income': yearly_income,
        'yearly_expenses': yearly_expenses,
    })


from django.http import HttpResponseForbidden
@login_required 
def export_to_excel(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You need to be logged in to access this page.")

    wb = Workbook()
    ws = wb.active
    ws.append(['Date', 'Amount', 'Category'])

    # Filtering income and expense by authenticated user
    incomes = Income.objects.filter(user=request.user)
    for income in incomes:
        ws.append([income.date, income.amount, income.category])

    expenses = Expense.objects.filter(user=request.user)
    for expense in expenses:
        ws.append([expense.date, expense.amount, expense.category])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=financial_data.xlsx'
    wb.save(response)
    return response



from io import BytesIO
@login_required 
def export_to_pdf(request):
    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Example content: fetch data from models (Income and Expense)
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    y_position = 750  # starting Y position for the content

    # Write the headers
    p.drawString(100, y_position, "Date")
    p.drawString(200, y_position, "Amount")
    p.drawString(300, y_position, "Category")
    
    y_position -= 20

    # Write incomes to PDF
    for income in incomes:
        p.drawString(100, y_position, str(income.date))
        p.drawString(200, y_position, str(income.amount))
        # Ensure the category is not None
        p.drawString(300, y_position, income.category.name if income.category else "No Category")
        y_position -= 20

    # Write expenses to PDF
    for expense in expenses:
        p.drawString(100, y_position, str(expense.date))
        p.drawString(200, y_position, str(expense.amount))
        # Ensure the category is not None
        p.drawString(300, y_position, expense.category.name if expense.category else "No Category")
        y_position -= 20

    # Finalize PDF and get the content into the response
    p.showPage()
    p.save()

    # Set the response type to PDF and send the content
    buffer.seek(0)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="financial_data.pdf"'
    response.write(buffer.read())
    
    return response

from .forms import BudgetForm

@login_required 
def set_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user  # associate budget with logged-in user
            budget.save()
            return redirect('budget_dashboard')  # redirect to a budget dashboard
    else:
        form = BudgetForm()
    return render(request, 'tracker/set_budget.html', {'form': form})



# for admin dashbord
# Username (leave blank to use 'smahe'): moin
# Email address: mkpmoinkhan@gmail.com
# Password: 1234