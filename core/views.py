from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from io import BytesIO
import json

# Create your views here.


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def home(request):
    return render(request, 'home.html')


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    template_name = 'logout.html'


def emi_calculator(request):
    if request.method == 'POST':
        principal = float(request.POST.get('principal', 0))
        rate = float(request.POST.get('rate', 0)) / 100 / 12  # Monthly rate
        tenure = int(request.POST.get('tenure', 0)) * 12  # In months

        # EMI calculation
        if rate > 0:
            emi = principal * rate * (1 + rate) ** tenure / ((1 + rate) ** tenure - 1)
        else:
            emi = principal / tenure

        total_amount = emi * tenure
        total_interest = total_amount - principal

        # Generate amortization schedule
        schedule = []
        remaining_balance = principal
        for month in range(1, tenure + 1):
            interest_payment = remaining_balance * rate
            principal_payment = emi - interest_payment
            remaining_balance -= principal_payment
            schedule.append({
                'month': month,
                'emi': round(emi, 2),
                'principal': round(principal_payment, 2),
                'interest': round(interest_payment, 2),
                'balance': round(remaining_balance, 2)
            })

        context = {
            'principal': principal,
            'rate': request.POST.get('rate'),
            'tenure': request.POST.get('tenure'),
            'emi': round(emi, 2),
            'total_amount': round(total_amount, 2),
            'total_interest': round(total_interest, 2),
            'schedule': schedule,
            'schedule_json': json.dumps(schedule),
        }
        return render(request, 'emi_calculator.html', context)

    return render(request, 'emi_calculator.html')


import json
from datetime import datetime
from io import BytesIO
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def emi_pdf(request):
    if request.method == 'POST':
        schedule = json.loads(request.POST.get('data', '[]'))

        # Extra loan details (hidden fields will be added in template)
        principal = request.POST.get('principal')
        rate = request.POST.get('rate')
        tenure = request.POST.get('tenure')
        emi = request.POST.get('emi')
        total_interest = request.POST.get('total_interest')
        total_amount = request.POST.get('total_amount')

        # Current Date & Time
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()

        # Title
        title = Paragraph("<b>JAYA RANJAN CHIT FUNDS - EMI SCHEDULE</b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Date & Time
        elements.append(Paragraph(f"<b>Generated On:</b> {now}", styles['Normal']))
        elements.append(Spacer(1, 12))

        

        # Amortization Table Heading
        elements.append(Paragraph("<b>Amortization Schedule</b>", styles['Heading3']))
        elements.append(Spacer(1, 10))

        # Table Data
        table_data = [['Month', 'EMI', 'Principal', 'Interest', 'Balance']]
        for row in schedule:
            table_data.append([
                str(row['month']),
                f"₹{row['emi']}",
                f"₹{row['principal']}",
                f"₹{row['interest']}",
                f"₹{row['balance']}"
            ])

        # Table Styling
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)

        # Build PDF
        doc.build(elements)
        buffer.seek(0)

        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=\"emi_schedule.pdf\"'
        return response

    return HttpResponse("Invalid request")
