import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os


def html_checkout(fig,h=500, w=700):
	return fig.to_html(full_html=False, default_height=h, default_width=w)




def load_main():
	df2020 = pd.read_csv (r'dataviz/script/valeursfoncieres-2020.txt',sep='|')
	df2019 = pd.read_csv (r'dataviz/script/valeursfoncieres-2019.txt',sep='|')

	df2020 = df2020.replace('', np.nan).fillna(0)
	df2019 = df2019.replace('', np.nan).fillna(0)

	df2020=df2020.drop(['Code service CH','Reference document','1 Articles CGI','2 Articles CGI','3 Articles CGI','4 Articles CGI','5 Articles CGI','No disposition','No voie','B/T/Q','Type de voie','Code voie','Voie','Code postal','Code commune','Prefixe de section','Section','No plan','No Volume','1er lot','Surface Carrez du 1er lot','2eme lot','Surface Carrez du 2eme lot','3eme lot','Surface Carrez du 3eme lot','4eme lot','Surface Carrez du 4eme lot','5eme lot','Surface Carrez du 5eme lot','Nombre de lots','Code type local','Identifiant local','Nature culture speciale'], axis=1)
	df2019=df2019.drop(['Code service CH','Reference document','1 Articles CGI','2 Articles CGI','3 Articles CGI','4 Articles CGI','5 Articles CGI','No disposition','No voie','B/T/Q','Type de voie','Code voie','Voie','Code postal','Code commune','Prefixe de section','Section','No plan','No Volume','1er lot','Surface Carrez du 1er lot','2eme lot','Surface Carrez du 2eme lot','3eme lot','Surface Carrez du 3eme lot','4eme lot','Surface Carrez du 4eme lot','5eme lot','Surface Carrez du 5eme lot','Nombre de lots','Code type local','Identifiant local','Nature culture speciale'], axis=1)

	df2020["Nombre pieces principales"] = pd.to_numeric(df2020["Nombre pieces principales"],downcast='integer')
	df2020["Valeur fonciere"] = df2020["Valeur fonciere"].replace({',': '.'}, regex=True)
	df2020["Valeur fonciere"] = pd.to_numeric(df2020["Valeur fonciere"],downcast='float')
	df2020['Code departement'] = df2020['Code departement'].astype(str)
	df2020['Date mutation'] = pd.to_datetime(df2020['Date mutation'], format='%d/%m/%Y')

	df2019["Nombre pieces principales"] = pd.to_numeric(df2019["Nombre pieces principales"],downcast='integer')
	df2019["Valeur fonciere"] = df2019["Valeur fonciere"].replace({',': '.'}, regex=True)
	df2019["Valeur fonciere"] = pd.to_numeric(df2019["Valeur fonciere"],downcast='float')
	df2019['Code departement'] = df2019['Code departement'].astype(str)
	df2019['Date mutation'] = pd.to_datetime(df2019['Date mutation'], format='%d/%m/%Y')
	return df2019,df2020



# Static graphs 

#Analyse Financiere

def distribution_valeur_fonciere(df2020=pd.DataFrame()):
	if df2020.empty:
		print("###ERROR")
		df2019,df2020=load_main()
	df=df2020[["Valeur fonciere"]]
	df=df[df["Valeur fonciere"] < 1000000]
	fig = px.histogram(df, x="Valeur fonciere", title="Distribution des valeurs foncières des transactions")
	return html_checkout(fig)

def distribution_prix_m2(df2020=pd.DataFrame()):
	if df2020.empty:
		print("###ERROR")
		df2019,df2020=load_main()
	df=df2020
	df['Surface reelle bati']=df2020[df2020['Surface reelle bati']>0]['Surface reelle bati']
	df['prix m2']=df2020["Valeur fonciere"]/df['Surface reelle bati']
	#df.head()
	df=df[df['prix m2'] < 15000]
	df=df['prix m2'][0:10000]


	fig = px.histogram(df, x="prix m2", title="Distribution des prix au m2 des transactions")
	return html_checkout(fig)

def m2_per_mutation(df2020=pd.DataFrame()):
	if df2020.empty:
		print("###ERROR")
		df2019,df2020=load_main()
	df=df2020[["Surface terrain","Valeur fonciere",'Nature mutation']]
	df=df[df["Surface terrain"] != 0]
	df["prixm"]=df["Valeur fonciere"]/df["Surface terrain"]
	df=df[['Nature mutation',"prixm"]]
	df=df.groupby('Nature mutation').mean().sort_values("prixm",ascending=False).reset_index()
	#print(df.head())
	fig = px.bar(df, x='Nature mutation', y="prixm", title="m² en fonction de la nature de la mutation")
	return html_checkout(fig)

def proportion_types_biens(df2020=pd.DataFrame()):
	if df2020.empty:
		print("###ERROR")
		df2019,df2020=load_main()
	dftemp=df2020[df2020['Type local']!=0].groupby('Type local').size().reset_index(name='counts')             
	fig=px.pie(dftemp, values='counts',names='Type local',title="Proportion des différents types de biens parmi les transactions")
	return html_checkout(fig)

def distribution_prix_m2_par_type(df2020=pd.DataFrame()):
	if df2020.empty:
		print("###ERROR")
		df2019,df2020=load_main()
	df=df2020[['Surface reelle bati','Valeur fonciere','Type local']]
	df=df[df['Surface reelle bati']>0]
	df['Prix m2']=df["Valeur fonciere"]/df["Surface reelle bati"]
	df=df[df['Prix m2']<15000]
	df.pop('Surface reelle bati')
	df.pop('Valeur fonciere')
	fig = px.histogram(df, x="Prix m2", color="Type local", barmode="overlay",title="Distribution des prix au m2 en fonction des types de biens")
	return html_checkout(fig)

# Tailles de terrain





def prop_terrain_taille(df2020=pd.DataFrame()):
	if df2020.empty:
		print("###ERROR")
		df2019,df2020=load_main()
	d = {'Terrain': [False if el<=10 else True for el in df2020['Surface terrain']]}
	df = pd.DataFrame(data=d)
	df=df.groupby('Terrain').size().reset_index(name='counts')
	fig=px.pie(df, values='counts',names='Terrain',title="Proportion des mutations avec terrain")
	return html_checkout(fig)
	

def histo_surface(df2020=pd.DataFrame()):
	if df2020.empty:
		print("###ERROR")
		df2019,df2020=load_main()
	df=df2020[["Surface terrain"]]
	df=df[df["Surface terrain"] > 10][0:100000]
	df=df[df["Surface terrain"] < 10000]
	fig = px.histogram(df, x="Surface terrain",title="Surface de terrain")
	return html_checkout(fig)

def prop_nature_mutation(df2020=pd.DataFrame()):
	if df2020.empty:
		print("###ERROR")
		df2019,df2020=load_main()
	dftemp=df2020.groupby('Nature mutation').size().reset_index(name='counts')
	fig=px.pie(dftemp, values='counts',names='Nature mutation', title="Proportion des différentes nature de mutation")
	return html_checkout(fig)

def surface_moy_per_mutation(df2020=pd.DataFrame()):
	if df2020.empty:
		print("###ERROR")
		df2019,df2020=load_main()
	df=df2020[['Nature mutation','Surface terrain']]
	df=df.groupby('Nature mutation').mean().sort_values("Surface terrain",ascending=False).reset_index()
	fig = px.bar(df, x="Surface terrain", y="Nature mutation", orientation='h', title="Surface de terrain moyenne en fonction de la nature de la mutation")
	return html_checkout(fig)


# href vers prop_nature_from_mutation


# Etude Geographique



def vente_per_departement(df2020=pd.DataFrame()):
	if df2020.empty:
		print("###ERROR")
		df2019,df2020=load_main()
	df=df2020[['Nature mutation','Code departement']]
	#df=df[df['Surface terrain']>0].groupby('Code departement').mean().reset_index()
	df=df[df['Nature mutation']=='Vente'].groupby('Code departement').count().rename(columns={'Nature mutation': 'Nb de ventes'}).reset_index()
	#print(df.head())
	import pygal
	fr_chart = pygal.maps.fr.Departments(human_readable=True)
	fr_chart.title = 'Nombre de ventes par departements francais'
	dictvalues=dict(zip(df["Code departement"],df["Nb de ventes"]))
	fr_chart.add('In 2020', dictvalues)
	return fr_chart.render()

def terrains_per_departement(df2020=pd.DataFrame()):
	if df2020.empty:
		print("###ERROR")
		df2019,df2020=load_main()
	df= df2020[['Surface terrain','Code departement']]
	df=df[df['Surface terrain']>0].groupby('Code departement').mean().reset_index()
	
	import pygal
	fr_chart = pygal.maps.fr.Departments(human_readable=True)
	fr_chart.title = 'Nombre de ventes par departements francais'
	dictvalues=dict(zip(df["Code departement"],df["Surface terrain"]))
	fr_chart.add('In 2020', dictvalues)
	return fr_chart.render()

def m2_moyen_IDF(df2020=pd.DataFrame()):
	if df2020.empty:
		print("###ERROR")
		df2019,df2020=load_main()
	df= df2020[['Surface reelle bati','Code departement','Valeur fonciere']]
	df=df[df['Surface reelle bati']>0]

	df=df[df['Code departement'].isin(['75','77','78','91','92','93','94','95'])]
	df['prix m2']=df["Valeur fonciere"]/df['Surface reelle bati']
	df=df.groupby('Code departement')['prix m2'].mean().reset_index(name='Moyenne')
	#df.head()
	fig = px.bar(df,x='Code departement',y='Moyenne', title="Prix au m² moyen des départements d'île de France")
	fig.update_layout(xaxis_type = 'category')
	return html_checkout(fig)





# Comparaison 2019 2020


def weekly_transac(df2019=pd.DataFrame(),df2020=pd.DataFrame()):
	if df2020.empty or df2019.empty: 
		print("###ERROR")
		df2019,df2019,df2020=load_main()
	
	data2020 = df2020[["Date mutation"]]
	data2019= df2019[["Date mutation"]]

	data2020['Month-Day'] = data2020['Date mutation'].dt.strftime('%m-%d')
	data2019['Month-Day'] = data2019['Date mutation'].dt.strftime('%m-%d')

	data2020=data2020.groupby('Date mutation')['Month-Day'].count().reset_index(name='counts')
	data2019=data2019.groupby('Date mutation')['Month-Day'].count().reset_index(name='counts')
	data2020=data2020[data2020['Date mutation'].dt.dayofweek<5]
	data2019=data2019[data2019['Date mutation'].dt.dayofweek<5]

	data2020=data2020.groupby(data2020['Date mutation'].dt.weekofyear)['counts'].sum().reset_index(name='counts')
	data2019=data2019.groupby(data2019['Date mutation'].dt.weekofyear)['counts'].sum().reset_index(name='counts')


	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data2020['Date mutation'], y=data2020['counts'], name="2020",))
	fig.add_trace(go.Scatter(x=data2019['Date mutation'], y=data2019['counts'], name="2019"))

	fig.update_layout(title='Nombre de mutations par semaine en 2019 et 2020',
					xaxis_title='Semaine',
					yaxis_title='Nombre de transactions')
	return html_checkout(fig)



def proportion_types_biens_2019(df2019=pd.DataFrame(),df2020=pd.DataFrame()):
	if df2020.empty or df2019.empty: 
		print("###ERROR")
		df2019,df2019,df2020=load_main()
	
	data2019=df2019[df2019['Type local']!=0].groupby('Type local').size().reset_index(name='counts')
	data2020=df2020[df2020['Type local']!=0].groupby('Type local').size().reset_index(name='counts')

	#data2020.head()


	from plotly.subplots import make_subplots
	labels=['Appartement','Dépendance','Local industriel. commercial ou assimilé','Maison']

	fig = make_subplots(1, 2, specs=[[{'type':'domain'}, {'type':'domain'}]],
						subplot_titles=['2019', '2020'])
	fig.add_trace(go.Pie(labels=labels, values=data2019['counts'], scalegroup='one'), 1, 1)
	fig.add_trace(go.Pie(labels=labels, values=data2020['counts'], scalegroup='one'), 1, 2)

	fig.update_layout(title_text='Proportion des types de biens pour les transactions de 2019 et 2020')
	return html_checkout(fig)



def croissance_transac(df2019=pd.DataFrame(),df2020=pd.DataFrame()):
	if df2020.empty or df2019.empty: 
		print("###ERROR")
		df2019,df2019,df2020=load_main()
	
	data2020 = df2020[["Code departement"]]
	data2019= df2019[["Code departement"]]


	data2020=data2020.groupby('Code departement')['Code departement'].count().reset_index(name='counts 2020')
	data2019=data2019.groupby('Code departement')['Code departement'].count().reset_index(name='counts 2019')
	data=data2020
	data['counts 2019']=data2019['counts 2019']
	#data.head()

	data=data.sort_values(by='counts 2020',ascending=False).reset_index(drop=True)

	data["Croissance en %"]=(data['counts 2020']-data['counts 2019'])*100/data['counts 2019']
	data=data.sort_values(by='Croissance en %',ascending=False).reset_index(drop=True)
	data=data[data['Code departement']<'95']

	#data.head()
	fig=px.bar(data, x="Code departement",y="Croissance en %")
	fig.update_layout(xaxis_type = 'category')

	return html_checkout(fig)



# Dynamic graphs
def prop_nature_from_mutation(type_mutation,df2020=pd.DataFrame()):
	if df2020.empty:
		print("###ERROR")
		df2019,df2020=load_main()
	
	df=df2020[df2020['Nature mutation']==type_mutation][['Nature culture','Surface terrain']].rename(columns={'Surface terrain': 'Count'}) #Surface terrain is used only as a gateway column for the count
	df=df.groupby("Nature culture").count().drop(0).sort_values("Count",ascending=True).reset_index()
	#print(df.head())
	fig = px.pie(df, values="Count", names='Nature culture' , title="Proportion des natures des cultures sur les "+type_mutation.lower() ,width=900, height=900)

	return html_checkout(fig)


def evol_prix_from_depart(dept_choisi,df2019=pd.DataFrame(),df2020=pd.DataFrame()):
	if df2020.empty or df2019.empty: 
		print("###ERROR")
		df2019,df2019,df2020=load_main()

	data2020=df2020[['Date mutation','Code departement','Surface reelle bati','Valeur fonciere']]
	data2020['Surface reelle bati']=data2020[data2020['Surface reelle bati']>0]['Surface reelle bati']
	data2020['Prix m2']=data2020["Valeur fonciere"]/data2020['Surface reelle bati']

	data2019=df2019[['Date mutation','Code departement','Surface reelle bati','Valeur fonciere']]
	data2019['Surface reelle bati']=data2019[data2019['Surface reelle bati']>0]['Surface reelle bati']
	data2019['Prix m2']=data2019["Valeur fonciere"]/data2019['Surface reelle bati']


	data2020=data2020[data2020['Code departement']== dept_choisi]
	data2019=data2019[data2019['Code departement']== dept_choisi]


	data2020=data2020.drop(['Valeur fonciere','Surface reelle bati'], axis=1)
	data2019=data2019.drop(['Valeur fonciere','Surface reelle bati'], axis=1)
	#print(dept_choisi)
	#data2020.head()

	data2020=data2020.groupby(data2020['Date mutation'].dt.weekofyear).agg(['count','mean']).reset_index().rename(columns={'count':'Nombre de transactions','mean':'Moyenne des prix au m2'})
	data2019=data2019.groupby(data2019['Date mutation'].dt.weekofyear).agg(['count','mean']).reset_index().rename(columns={'count':'Nombre de transactions','mean':'Moyenne des prix au m2'})

	#data2019.info()
	data2019.columns = ['Date mutation', 'Nombre de transactions','Moyenne des prix au m2']
	data2020.columns = ['Date mutation', 'Nombre de transactions','Moyenne des prix au m2']

	#data2019.head()


	fig1 = go.Figure()
	fig1.add_trace(go.Scatter(x=data2019['Date mutation'], y=data2019['Moyenne des prix au m2'],name='2019'))
	fig1.add_trace(go.Scatter(x=data2020['Date mutation'], y=data2020['Moyenne des prix au m2'],name='2020'))

	fig1.update_layout(xaxis_title='Semaine',
					yaxis_title='Prix au m2',title="Evolution du prix au m2 au cours de l'année pour le département "+dept_choisi)
	return html_checkout(fig1)