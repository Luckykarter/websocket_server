from django.shortcuts import render

from django.db import connections
from authentication.permissions import HasToken
from authentication import models
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
import datetime

DATE_FORMAT = '%d/%m/%Y'

def _get_error_from_token(token):
    current_date = datetime.date.today()
    if not token:
        return "Вы не авторизованы"
    error = ""
    try:
        token = models.ApiToken.objects.get(token=token)
        if current_date < token.start_date:
            open_date = token.start_date + datetime.timedelta(days=1)
            error = f'Ваш доступ откроется {open_date.strftime(DATE_FORMAT)}\nНужно просто подождать :-)'
        elif current_date > token.end_date:
            error = f'Ваш доступ закончился {token.end_date.strftime(DATE_FORMAT)}\n\nСпасибо за участие!'

    except models.ApiToken.DoesNotExist:
        error = 'У вас нет доступа к данному ресурсу.\nПопробуйте залогиниться в приложении заново'
    return error


@api_view(['POST'])
@permission_classes([HasToken])
def obtain_token(request):
    token, _ = models.ApiToken.objects.get_or_create(
        purpose=request.data.get('purpose'),
        owner=request.data.get('owner')
    )

    token.start_date = datetime.datetime.strptime(request.data.get('start_date'), DATE_FORMAT)
    token.end_date = datetime.datetime.strptime(request.data.get('end_date'), DATE_FORMAT)

    for database in request.data.get('databases'):
        database, _ = models.SupportedDatabase.objects.get_or_create(database_name=database)
        token.allowed_databases.add(database)
    token.save()

    return Response(data={'token': token.token, 'error': _get_error_from_token(token.token)},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def validate_token(request):
    error = _get_error_from_token(request.headers.get('token'))
    print(error)

    return Response(data={'error': error}, status=status.HTTP_200_OK)

