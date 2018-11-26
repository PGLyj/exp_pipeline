from django.shortcuts import render
from .models import Exp_models
from django import forms
import pandas as pd
import numpy as np
import csv

# Create your views here.
class NameForm(forms.Form):
    gene_name = forms.CharField(max_length=20)
 
def index(request):
    DBex       = Exp_models.objects.order_by('?')[0]
    if request.method=='POST':
        form = NameForm(request.POST)
        if form.is_valid():
            query 		= form.cleaned_data['gene_name']
            #DBex 		= Exp_models.objects.get(Gene_id=query)
            print(query)
            form 		= NameForm()
            gene_filter = Exp_models.objects.filter(Gene_id=query)
            print(gene_filter)
            DBdatas     = []
            DBdatas += [[x.Tpm, x.Treatment] for x in gene_filter]
            #DBdatas += DBdata 
            print(DBdatas)
            #for x in DBdata:
             #   DBdatas += x


            data=[(np.array(DBdatas))]
            
            np.savetxt('./blog/static/%s.csv'%query, np.column_stack((data)), delimiter = ',', fmt = '%s', header = 'tpm,treatment',comments="")

            csv_file	= './blob/static/%s.csv'%query
            return render(request, 'blog/index.html', {'DBex' : DBex, 'form': form, 'csv_file' : csv_file.split('/')[-1], 'query' : query})
                #return redirect('',query=genename)
    else:
        form = NameForm()
        return render(request, 'blog/index.html', {'csv_file' : 'AT1G04000.1.csv' ,'DBex' : DBex, 'form': form, 'query' : 'AT1G4000.1'})