from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
class InicioView(ListView):
   
   


    def get(self,request):
        coches=Coche.objects.all()
        respuesta=Coche.objects.all() 
        paginator=Paginator(respuesta,4)
        page_number=request.GET.get('page')
        resultado =paginator.get_page(page_number)



        return render(request,"inicio.html",{"coches":coches,"resultado":resultado})


    
