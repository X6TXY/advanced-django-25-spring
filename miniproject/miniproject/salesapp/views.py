from datetime import datetime, timedelta
from io import BytesIO

from django.core.files.base import ContentFile
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Invoice, Promotion, SalesOrder
from .serializers import (InvoiceSerializer, PromotionSerializer,
                          SalesOrderSerializer)


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'active',
                openapi.IN_QUERY,
                description="Filter active promotions",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'product_id',
                openapi.IN_QUERY,
                description="Filter by product ID",
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        active = request.query_params.get('active')
        if active is not None:
            active = active.lower() == 'true'
            queryset = queryset.filter(
                is_active=active,
                start_date__lte=datetime.now(),
                end_date__gte=datetime.now()
            )

        product_id = request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(products__id=product_id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SalesOrderViewSet(viewsets.ModelViewSet):
    serializer_class = SalesOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'sales':
            return SalesOrder.objects.filter(sales_rep=user)
        elif user.role == 'customer':
            return SalesOrder.objects.filter(customer=user)
        return SalesOrder.objects.all()

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['approved', 'cancelled']
                ),
            },
            required=['status']
        )
    )
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in ['approved', 'cancelled']:
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        if new_status == 'approved':
            invoice_number = f"INV-{order.id}-{datetime.now().strftime('%Y%m%d')}"
            due_date = datetime.now().date() + timedelta(days=30)
            Invoice.objects.create(
                sales_order=order,
                invoice_number=invoice_number,
                due_date=due_date
            )

        return Response({'status': 'Order status updated'})

    @action(detail=True, methods=['get'])
    def generate_invoice(self, request, pk=None):
        order = self.get_object()

        if not hasattr(order, 'invoice'):
            return Response(
                {'error': 'No invoice found for this order'},
                status=status.HTTP_404_NOT_FOUND
            )

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        elements = []
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1
        )

        elements.append(Paragraph("INVOICE", title_style))
        elements.append(Spacer(1, 20))

        elements.append(Paragraph(f"Invoice #: {order.invoice.invoice_number}", styles['Normal']))
        elements.append(Paragraph(f"Date: {order.invoice.generated_at.strftime('%B %d, %Y')}", styles['Normal']))
        elements.append(Paragraph(f"Due Date: {order.invoice.due_date.strftime('%B %d, %Y')}", styles['Normal']))
        elements.append(Spacer(1, 20))

        elements.append(Paragraph("Customer Details:", styles['Heading3']))
        elements.append(Paragraph(f"Name: {order.customer.get_full_name()}", styles['Normal']))
        elements.append(Paragraph(f"Email: {order.customer.email}", styles['Normal']))
        elements.append(Spacer(1, 20))

        table_data = [
            ['Product', 'Quantity', 'Unit Price', 'Discount', 'Total'],
        ]

        for item in order.items.all():
            table_data.append([
                item.product.name,
                str(item.quantity),
                f"${item.unit_price}",
                f"${item.discount_amount}",
                f"${item.final_price}"
            ])

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))

        elements.append(Paragraph(f"Subtotal: ${order.total_amount}", styles['Normal']))
        elements.append(Paragraph(f"Discount: ${order.discount_amount}", styles['Normal']))
        elements.append(Paragraph(f"Total: ${order.final_amount}", styles['Heading2']))

        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()

        order.invoice.pdf_file.save(
            f'invoice_{order.invoice.invoice_number}.pdf',
            ContentFile(pdf)
        )

        return Response({
            'message': 'Invoice generated successfully',
            'pdf_url': order.invoice.pdf_file.url
        })


class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'sales':
            return Invoice.objects.filter(sales_order__sales_rep=user)
        elif user.role == 'customer':
            return Invoice.objects.filter(sales_order__customer=user)
        return Invoice.objects.all()

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        invoice = self.get_object()
        if not invoice.pdf_file:
            return Response(
                {'error': 'PDF not generated yet'},
                status=status.HTTP_404_NOT_FOUND
            )
        response = HttpResponse(
            invoice.pdf_file,
            content_type='application/pdf'
        )
        response['Content-Disposition'] = f'attachment; filename="{invoice.invoice_number}.pdf"'
        return response
