from django.shortcuts import render

# Create your views here.
from rest_framework import response,generics,status,permissions
from rest_framework.response import Response
from ecomerce.models import Account
from django.db.models import F,Q,Sum
from django.core.serializers.json import DjangoJSONEncoder
import bcrypt
from cryptography.fernet import Fernet
import jwt
from django.conf import settings
from datetime import datetime,timedelta
import json
from rest_framework.permissions import IsAuthenticated
import logging

from ecomerce.resolver import encrypt_token_data
logger=logging.getLogger(__name__)


class logine(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes=[]

    """
    URLS - assig/login/
    """
    def post(self,request):
        
        try:
            data=request.data

            user_name=data.get('user_name')
            psd=data.get('password')
            if not user_name and psd:
                return Response({'status':'fail','message':'Please enter the user name/password'},status=status.HTTP_400_BAD_REQUEST)
            logine_vald=Account.objects.get(user_name__iexact=user_name)
            if not bcrypt.checkpw(bytes(psd,'utf-8'),bytes(logine_vald.password,'utf-8')):
                return Response({'status':'fail','message':'Invalid password'},status=status.HTTP_400_BAD_REQUEST)
            token_con = {'user_id':logine_vald.id,'user_name':logine_vald.user_name}
            encrypt_data=encrypt_token_data(token_con) 
            z
            signing_key = open("public_key.txt").read()
            expiry= datetime.now() + timedelta(hours=23)
            serialized_datetime = json.dumps(expiry, cls=DjangoJSONEncoder)
            token = jwt.encode({'data':encrypt_data,'exp_time':serialized_datetime,'user_name':logine_vald.user_name}, signing_key,'HS256')
            return Response({'status':'success','message':'succesfully login','user_id':token_con['user_id'],'token':token})
        except Account.DoesNotExist as ar:
            logging.debug('Exception {}'.format(ar))
            return Response({'status':'fail','message':'Acoount DoesnotExist'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as er:
            logging.debug('Exception {}'.format(er))
            return Response({'status':'fail','message':'something went wrong please try agine later'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Registration(generics.GenericAPIView):
    def post(self,request):
        """
        URLS - assig/register/ '

        {
        "role_name_id":1,
        "user_name":"user_name",
        "password":"password",
        "account_hoder":"account_hoder",
        "mail_id":"mail_id",
        "mobile_number":23456789,
        "dob":"",
        "address":"address"
                        }
        """
        try:
            print(request.user_id)
            data=request.data
            print(request.user_id)
            pasword=data.get('password')
            logine_vald=Account.objects.filter(user_name__iexact=data.get('user_name')).values('id')
            if logine_vald:
                return Response({'status':'fail','message':'User name already exist'},status=status.HTTP_400_BAD_REQUEST)
            mail_vald=Account.objects.filter(mail_id__iexact= data.get('mail_id')).values('id')
            if mail_vald:
                return Response({'status':'fail','message':'mail linked with other account'},status=status.HTTP_400_BAD_REQUEST)
                
            if not data.get('role_name_id'):
                return Response({'status':'fail','message':'please Enter the login role'},status=status.HTTP_400_BAD_REQUEST)
            if not data.get('user_name'):
                return Response({'status':'fail','message':'please Enter the user_name'},status=status.HTTP_400_BAD_REQUEST)
            hash_pasword=bcrypt.hashpw(bytes(pasword.encode('utf-8')),bcrypt.gensalt(10)).decode('utf-8')
            datas={
                "role_name_id":data.get('role_name_id'),
                "user_name":data.get('user_name'),
                "password":hash_pasword,
                "account_holder":data.get('account_hoder'),
                "mail_id":data.get('mail_id'),
                "mobile_number":data.get('mobile_number'),
                "dob":data.get('dob'),
                "del_address":data.get('del_address'),
            }
            logine_vald=Account.objects.create(**datas)
            return Response({'status':'success','message':'succesfully created'})

        except Exception as er:
            logging.debug('Exception {}'.format(er))
            return Response({'status':'fail','message':'something went wrong please try agine later',},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
