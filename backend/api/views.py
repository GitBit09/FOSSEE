from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import pandas as pd
import io
import traceback
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from .models import Dataset, Equipment
from .serializers import DatasetSerializer, DatasetListSerializer


class DatasetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling dataset operations:
    - List all datasets (last 5)
    - Upload CSV
    - Get summary statistics
    - Generate PDF report
    """
    serializer_class = DatasetListSerializer
    permission_classes = [AllowAny]  # Change to IsAuthenticated for production
    
    def get_queryset(self):
        """
        Override to return all datasets for detail views, but only last 5 for list
        """
        if self.action == 'list':
            return Dataset.objects.all()[:5]
        return Dataset.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DatasetSerializer
        return DatasetListSerializer
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        """
        Upload CSV file and analyze data
        """
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        csv_file = request.FILES['file']
        
        # Validate file type
        if not csv_file.name.endswith('.csv'):
            return Response(
                {'error': 'File must be a CSV'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Read CSV using pandas
            df = pd.read_csv(csv_file)
            
            # Validate required columns
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return Response(
                    {'error': f'Missing columns: {", ".join(missing_columns)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calculate summary statistics
            summary = {
                'total_count': len(df),
                'avg_flowrate': float(df['Flowrate'].mean()),
                'avg_pressure': float(df['Pressure'].mean()),
                'avg_temperature': float(df['Temperature'].mean()),
                'equipment_types': df['Type'].value_counts().to_dict(),
                'min_flowrate': float(df['Flowrate'].min()),
                'max_flowrate': float(df['Flowrate'].max()),
                'min_pressure': float(df['Pressure'].min()),
                'max_pressure': float(df['Pressure'].max()),
                'min_temperature': float(df['Temperature'].min()),
                'max_temperature': float(df['Temperature'].max()),
            }
            
            # Create Dataset record
            dataset = Dataset.objects.create(
                filename=csv_file.name,
                total_rows=len(df),
                uploaded_by=request.user if request.user.is_authenticated else None
            )
            dataset.set_summary(summary)
            dataset.save()
            
            # Create Equipment records
            equipment_records = []
            for _, row in df.iterrows():
                equipment_records.append(
                    Equipment(
                        dataset=dataset,
                        equipment_name=row['Equipment Name'],
                        equipment_type=row['Type'],
                        flowrate=row['Flowrate'],
                        pressure=row['Pressure'],
                        temperature=row['Temperature']
                    )
                )
            Equipment.objects.bulk_create(equipment_records)
            
            # Keep only last 5 datasets
            all_datasets = Dataset.objects.all()
            if all_datasets.count() > 5:
                old_datasets = all_datasets[5:]
                for old in old_datasets:
                    old.delete()
            
            # Return response with summary
            serializer = DatasetSerializer(dataset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': f'Error processing file: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def generate_pdf(self, request, pk=None):
        """
        Generate PDF report for a dataset
        """
        try:
            dataset = self.get_object()
            equipment_list = dataset.equipment.all()
            summary = dataset.get_summary()
            
            # Create PDF in memory
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            title = Paragraph(f"<b>Chemical Equipment Analysis Report</b>", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 0.3*inch))
            
            # Dataset info
            info_text = f"""
            <b>Filename:</b> {dataset.filename}<br/>
            <b>Upload Date:</b> {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M')}<br/>
            <b>Total Equipment:</b> {dataset.total_rows}<br/>
            """
            elements.append(Paragraph(info_text, styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
            
            # Summary statistics
            summary_title = Paragraph("<b>Summary Statistics</b>", styles['Heading2'])
            elements.append(summary_title)
            elements.append(Spacer(1, 0.1*inch))
            
            summary_data = [
                ['Metric', 'Value'],
                ['Average Flowrate', f"{summary.get('avg_flowrate', 0):.2f}"],
                ['Average Pressure', f"{summary.get('avg_pressure', 0):.2f}"],
                ['Average Temperature', f"{summary.get('avg_temperature', 0):.2f}"],
            ]
            
            summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(summary_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Equipment type distribution
            type_title = Paragraph("<b>Equipment Type Distribution</b>", styles['Heading2'])
            elements.append(type_title)
            elements.append(Spacer(1, 0.1*inch))
            
            type_data = [['Type', 'Count']]
            for eq_type, count in summary.get('equipment_types', {}).items():
                type_data.append([eq_type, str(count)])
            
            type_table = Table(type_data, colWidths=[3*inch, 2*inch])
            type_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(type_table)
            
            # Build PDF
            doc.build(elements)
            
            # Return PDF
            buffer.seek(0)
            response = HttpResponse(buffer.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{dataset.filename}_report.pdf"'
            return response
            
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': f'Error generating PDF: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """Simple login endpoint"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        login(request, user)
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
    else:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    """Simple registration endpoint"""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(username=username, email=email, password=password)
    login(request, user)
    
    return Response({
        'message': 'Registration successful',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """Logout endpoint"""
    logout(request)
    return Response({'message': 'Logout successful'})


@api_view(['GET'])
def user_status(request):
    """Check if user is authenticated"""
    if request.user.is_authenticated:
        return Response({
            'authenticated': True,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email
            }
        })
    else:
        return Response({'authenticated': False})