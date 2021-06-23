from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse  #instead of render, you can send simple return HttpResponse("<H1>text</H1>")

from django.core.paginator import Paginator

import pandas as pd
import plotly as pt
import plotly.express as px
from .script.graphs import *

df2019,df2020=load_main()

def home(request):
	return render(request,"index.html")

#Analyse fi
dvf=distribution_valeur_fonciere(df2020)
dpm=distribution_prix_m2(df2020)
mpm=m2_per_mutation(df2020)
ptb=proportion_types_biens(df2020)
dpmpt=distribution_prix_m2_par_type(df2020)


#Analyse terrain
ptt=prop_terrain_taille(df2020)
hs=histo_surface(df2020)
pnm=prop_nature_mutation(df2020)
smpm=surface_moy_per_mutation(df2020)

#Analyse geo
vpd=vente_per_departement(df2020)
tpd=terrains_per_departement(df2020)
mmi=m2_moyen_IDF(df2020)

def graph_fi(request):
	graph_list=[]
	graph_list.append(dvf)
	graph_list.append(dpm)
	graph_list.append(mpm)
	graph_list.append(ptb)
	graph_list.append(dpmpt)

	paginator = Paginator(graph_list, 1)
	page_number = request.GET.get('page')
	graphs = paginator.get_page(page_number)
	context={'graphs': graphs}
	return render(request,"graph.html",context)


def graph_terrain(request):
	graph_list=[]
	graph_list.append(ptt)
	graph_list.append(hs)
	graph_list.append(pnm)
	graph_list.append(smpm)

	paginator = Paginator(graph_list, 1)
	page_number = request.GET.get('page')
	graphs = paginator.get_page(page_number)
	context={'graphs': graphs}
	return render(request,"graph.html",context)

def graph_geo(request):
	graph_list=[]
	graph_list.append(vpd)
	graph_list.append(tpd)
	graph_list.append(mmi)

	paginator = Paginator(graph_list, 1)
	page_number = request.GET.get('page')
	graphs = paginator.get_page(page_number)
	context={'graphs': graphs}
	return render(request,"graph.html",context)


wt=weekly_transac(df2019,df2020)
ptb=proportion_types_biens_2019(df2019,df2020)
ct=croissance_transac(df2019,df2020)
def graph_comp(request):
	graph_list=[]
	graph_list.append(wt)
	graph_list.append(ptb)
	graph_list.append(ct)

	paginator = Paginator(graph_list, 1)
	page_number = request.GET.get('page')
	graphs = paginator.get_page(page_number)
	context={'graphs': graphs}
	return render(request,"graph.html",context)





def graph_dyn_nature(request):
	if request.method=="POST":
		type_mutation=request.POST.get("option", "")
		
		graph_list=[]
		graph_list.append(prop_nature_from_mutation(type_mutation,df2020))
		paginator = Paginator(graph_list, 1)
		page_number = request.GET.get('page')
		graphs = paginator.get_page(page_number)
		context={'graphs': graphs,'widget': ["Echange","Vente","Vente terrain à bâtir","Expropriation","Adjudication","Vente en l'état futur d'achèvement"],
		'input_text':"Choisissez le type de mutation:",
		"func_name":"graph_dyn_nature"}
		return render(request,"graph.html",context)
	else:
		context={'widget': ["Echange","Vente","Vente terrain à bâtir","Expropriation","Adjudication","Vente en l'état futur d'achèvement"],
		'input_text':"Choisissez le type de mutation:",
		"func_name":"graph_dyn_nature"}
		return render(request,"graph.html",context)

def graph_dyn_evol_prix(request):
	if request.method=="POST":
		type_mutation=request.POST.get("option", "")
		
		graph_list=[]
		graph_list.append(evol_prix_from_depart(type_mutation,df2019,df2020))
		paginator = Paginator(graph_list, 1)
		page_number = request.GET.get('page')
		graphs = paginator.get_page(page_number)
		context={'graphs': graphs,'widget': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
       '13', '14', '15', '16', '17', '18', '19', '21', '22', '23', '24',
       '25', '26', '27', '28', '29', '2A', '2B', '30', '31', '32', '33',
       '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44',
       '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55',
       '56', '58', '59', '60', '61', '62', '63', '64', '65', '66', '69',
       '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81',
       '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92',
       '93', '94', '95', '971', '972', '973', '974'],
	   'input_text':"Choisissez le département:","func_name":"graph_dyn_evol_prix"}
		return render(request,"graph.html",context)
	else:
		context={'widget': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
       '13', '14', '15', '16', '17', '18', '19', '21', '22', '23', '24',
       '25', '26', '27', '28', '29', '2A', '2B', '30', '31', '32', '33',
       '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44',
       '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55',
       '56', '58', '59', '60', '61', '62', '63', '64', '65', '66', '69',
       '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81',
       '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92',
       '93', '94', '95', '971', '972', '973', '974'],
	   'input_text':"Choisissez le département:","func_name":"graph_dyn_evol_prix"}
		return render(request,"graph.html",context)