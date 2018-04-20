# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

import sys
import requests
from rest_framework import viewsets
from bs4 import BeautifulSoup, SoupStrainer

#  django import jsonify

from mechanize import Browser

import json
import cookielib
import mechanize
from django.http import HttpResponse
from django.http import JsonResponse


class UserViewSet(viewsets.GenericViewSet, viewsets.ViewSet):

    def retrieve(self, request, email=None):
        """get user and device detail"""
        pass
        # return Response(data)

# class UserViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # queryset = User.objects.all().order_by('-date_joined')
    # serializer_class = UserSerializer
    # Model = User

    # list(self, request):






def api_article(request, registrationnum=None):
# def api_article(request):

    # import pdb; pdb.set_trace()
    url = "http://mis.mptransport.org/MPLogin/eSewa/VehicleSearch.aspx"
    br = mechanize.Browser()
    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    # br.set_handle_equiv(True)
    # br.set_handle_gzip(True)
    # br.set_handle_redirect(True)
    # br.set_handle_referer(True)
    # br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    # br.set_handle_robots(False)
    br.open(url)
    br.select_form(name='aspnetForm')
    br["ctl00$ContentPlaceHolder1$txtRegNo"] =(registrationnum)
    res = br.submit()
    # import pdb; pdb.set_trace()

    content = res.read()
    soup=BeautifulSoup(content,  "html5lib")    

    table = soup.find("table", {"border":"1","id":"ctl00_ContentPlaceHolder1_grvSearchSummary"})

    # import pdb; pdb.set_trace()
    try:    
        for row in table.findAll('tr',{'class':'GridItem'}):
            col = row.findAll('td')
            number=col[2].find('a').string
            model_name=col[14].string
            owner_name=col[5].string
            city_rto=col[6].string
            reg_date=col[8].string
            data = {
            'registration_num': number,
                'model': model_name,
                'owner_name': owner_name,
                'rto_name': city_rto,
                'regis_date':reg_date,
                }

        # import pdb; pdb.set_trace()
        # return JsonResponse(data)
        # return HttpResponse(data)

        return render_to_response('mp_trans_scrap/base.html', data )

    except:
        return HttpResponse("No data found")




# Create your views here.

# def testwork(request):
#     # page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
#     page = requests.get("http://mis.mptransport.org/MPLogin/eSewa/VehicleSearch.aspx")

#     soup = BeautifulSoup(page.content, 'html.parser')
#     # import pdb;pdb.set_trace()

#     cookies = page.cookies

#     soup = BeautifulSoup(r.text, 'html.parser')
#     viewstate = soup.select('input[name="javax.faces.ViewState"]')[0]['value']

#     data = {
#         'javax.faces.partial.ajax':'true',
#         'javax.faces.source':'convVeh_Form:j_idt21',
#         'javax.faces.partial.execute':'@all',
#         'javax.faces.partial.render':'convVeh_Form:rcPanel',
#         'convVeh_Form:j_idt21':'convVeh_Form:j_idt21',
#         'convVeh_Form':'convVeh_Form',
#         'convVeh_Form:tf_reg_no1': first,
#         'convVeh_Form:tf_reg_no2': second,
#         'javax.faces.ViewState': viewstate,
#     }

#     r = requests.post(url=url, data=data, cookies=cookies)
    
#     soup = BeautifulSoup(r.text, 'html.parser')
#     table = SoupStrainer('tr')
#     soup = BeautifulSoup(soup.get_text(), 'html.parser', parse_only=table)
#     print(soup.get_text())

#     import pdb;pdb.set_trace()


#     return Response(soup)



