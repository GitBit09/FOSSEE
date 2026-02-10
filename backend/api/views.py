from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.http import HttpResponse

from .models import Dataset, Equipment

import pandas as pd
import io


# =========================
# AUTH VIEWS
# =========================

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')

    if not username or not password:
        return Response({'error': 'Username and password required'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'User exists'}, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )

    return Response(
        {'message': 'User created', 'username': user.username},
        status=201
    )


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        return Response({'message': 'Login success', 'username': user.username})

    return Response({'error': 'Invalid credentials'}, status=401)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'})


@api_view(['GET'])
def auth_status(request):
    if request.user.is_authenticated:
        return Response({
            'authenticated': True,
            'user': {
                'username': request.user.username,
                'email': request.user.email
            }
        })

    return Response({'authenticated': False})


# =========================
# DATASET VIEWS
# =========================

@api_view(['GET'])
def get_datasets(request):
    datasets = Dataset.objects.all()
    data = []

    for dataset in datasets:
        data.append({
            'id': dataset.id,
            'filename': dataset.filename,
            'uploaded_at': dataset.uploaded_at,
            'total_rows': dataset.total_rows,
            'summary': dataset.get_summary(),
            'uploaded_by': dataset.uploaded_by.username if dataset.uploaded_by else 'Anonymous'
        })

    return Response(data)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_dataset(request):
    """Upload and process CSV dataset"""
    try:
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=400)

        # Read CSV
        df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))

        # Required columns
        required_columns = [
            'Equipment Name',
            'Type',
            'Flowrate',
            'Pressure',
            'Temperature'
        ]

        if not all(col in df.columns for col in required_columns):
            return Response({
                'error': 'Missing required columns',
                'required': required_columns,
                'found': list(df.columns)
            }, status=400)

        # Summary stats
        summary = {
            'avg_flowrate': float(df['Flowrate'].mean()),
            'avg_pressure': float(df['Pressure'].mean()),
            'avg_temperature': float(df['Temperature'].mean()),
            'equipment_types': df['Type'].value_counts().to_dict()
        }

        # Create Dataset
        dataset = Dataset.objects.create(
            filename=file.name,
            total_rows=len(df),
            uploaded_by=request.user if request.user.is_authenticated else None
        )
        dataset.set_summary(summary)
        dataset.save()

        # Create Equipment records
        equipment_objects = []
        for _, row in df.iterrows():
            equipment_objects.append(
                Equipment(
                    dataset=dataset,
                    equipment_name=row['Equipment Name'],
                    equipment_type=row['Type'],
                    flowrate=row['Flowrate'],
                    pressure=row['Pressure'],
                    temperature=row['Temperature']
                )
            )

        Equipment.objects.bulk_create(equipment_objects)

        return Response({
            'message': 'Dataset uploaded successfully',
            'dataset_id': dataset.id,
            'filename': dataset.filename,
            'total_rows': dataset.total_rows,
            'summary': summary
        }, status=201)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def get_dataset_detail(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id)
        equipment = dataset.equipment.all()

        equipment_data = [
            {
                'id': eq.id,
                'equipment_name': eq.equipment_name,
                'equipment_type': eq.equipment_type,
                'flowrate': eq.flowrate,
                'pressure': eq.pressure,
                'temperature': eq.temperature
            }
            for eq in equipment
        ]

        return Response({
            'id': dataset.id,
            'filename': dataset.filename,
            'uploaded_at': dataset.uploaded_at,
            'total_rows': dataset.total_rows,
            'summary': dataset.get_summary(),
            'equipment': equipment_data
        })

    except Dataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=404)


# =========================
# PDF REPORT
# =========================

@api_view(['GET'])
def generate_pdf(request, dataset_id):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        dataset = Dataset.objects.get(id=dataset_id)

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)

        # Title
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, f"Equipment Report: {dataset.filename}")

        # Meta
        p.setFont("Helvetica", 12)
        y = 700
        p.drawString(100, y, f"Total Rows: {dataset.total_rows}")
        y -= 20
        p.drawString(
            100, y,
            f"Uploaded: {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
        )

        # Summary
        summary = dataset.get_summary()
        y -= 40
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y, "Summary Statistics")

        p.setFont("Helvetica", 10)
        y -= 20
        p.drawString(100, y, f"Average Flowrate: {summary.get('avg_flowrate', 0):.2f}")
        y -= 15
        p.drawString(100, y, f"Average Pressure: {summary.get('avg_pressure', 0):.2f}")
        y -= 15
        p.drawString(100, y, f"Average Temperature: {summary.get('avg_temperature', 0):.2f}")

        p.showPage()
        p.save()

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = (
            f'attachment; filename="report_{dataset_id}.pdf"'
        )
        return response

    except Dataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=404)

    except Exception as e:
        return Response({'error': str(e)}, status=500)
