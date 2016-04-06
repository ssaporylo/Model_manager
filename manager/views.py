from django.contrib.auth.models import User, Group
from django.apps import apps
from django.db import models
from django.db import connection
from rest_framework import viewsets
from serializers import UserSerializer, GroupSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils import create_model, SendData

_broker = SendData()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@api_view(['GET', 'POST'])
def create_models(request):
    if request.method == 'POST':
        name = request.data['name']
        try:
            name = str(request.data['name'])
            fields = request.data['fields'].split(',')
            fields_dict = {str(i): models.CharField(max_length=255) for i in fields}
        except:
            return Response({"message": "Incorrect data", "data": request.data})
        model = create_model(name, app_label='rest_framework', fields=fields_dict)
        table = 'rest_framework_{0}'.format(name.lower())
        attr = '{0} varchar(30) NOT NULL'.format(
            ' varchar(30) NOT NULL,'.join(fields_dict.keys()))
        cursor = connection.cursor()
        sql = 'CREATE TABLE {0} (id serial NOT NULL PRIMARY KEY, {1})'.format(
            table, attr)
        cursor.execute(sql)
        cursor.close()
        _broker.send(
            'Create model {0} with fields {1}'.format(
                name, str(fields_dict.keys())))

        return Response({"message": "Create model", "data": request.data})

    return Response({"message": str(apps.all_models.keys())})


@api_view(['POST', ])
def update_models(request):

    try:
        name = str(request.data['name'])
        fields = request.data['fields'].split(',')
        fields_dict = {str(i.split(':')[0]): str(i.split(':')[1]) for i in fields}
    except:
        message = "Incorrect data"
    try:
        model = apps.get_model(app_label='rest_framework', model_name=name)
        inst = model(**fields_dict)
        inst.save()
        message = "Create record in model {0}".format(name)
        _broker.send(
            'Update model: {0} fields: {1}'.format(name, fields_dict.items()))
    except Exception:
        message = Exception.message
    return Response({"message": message, "data": request.data})


@api_view(['POST', ])
def remove_models(request):
    try:
        name = str(request.data['name'])
        table = 'rest_framework_{0}'.format(name.lower())
        cursor = connection.cursor()
        sql = 'DROP TABLE {0}'.format(table)
        cursor.execute(sql)
        cursor.close()
        message = 'Delete model {0}'.format(name)
        _broker.send(message)
    except Exception:
        message = Exception.message

    try:
        model = apps.get_model(app_label='rest_framework', model_name=name)
        del model
    except Exception:
        pass

    return Response({"message": message, "data": request.data})
