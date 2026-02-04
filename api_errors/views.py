from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import ErrorReport
from .serializers import StatusSerializer, ErrorSerializer
from django.shortcuts import render


@api_view(['GET'])
def get_server_status(request):
    data = {'status': 'running', 'date': datetime.now()}
    serializer = StatusSerializer(data)
    return Response(serializer.data)

@api_view(['GET'])
def get_errors(request):
    errors = ErrorReport.objects.all()
    serializer = ErrorSerializer(errors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_error_from_code(request, code):
    try:
        error = ErrorReport.objects.get(code=code)
        serializer = ErrorSerializer(error)
        return Response(serializer.data)
    except ErrorReport.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_error(request):
    serializer = ErrorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def error_update_delete(request, id):
    try:
        error = ErrorReport.objects.get(id=id)
    except ErrorReport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ErrorSerializer(error, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        error.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
def api_demo(request):
    return render(request, 'api_demo.html')