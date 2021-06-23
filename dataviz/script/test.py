import numpy as np
import pandas as pd
import plotly.express as px
import os






def load_main():
	df2020 = pd.read_csv (r'dataviz/script/valeursfoncieres-2020.txt',sep='|')
	df2020 = df2020.replace('', np.nan).fillna(0)
	df2020=df2020.drop(['Code service CH','Reference document','1 Articles CGI','2 Articles CGI','3 Articles CGI','4 Articles CGI','5 Articles CGI','No disposition','No voie','B/T/Q','Type de voie','Code voie','Voie','Code postal','Code commune','Prefixe de section','Section','No plan','No Volume','1er lot','Surface Carrez du 1er lot','2eme lot','Surface Carrez du 2eme lot','3eme lot','Surface Carrez du 3eme lot','4eme lot','Surface Carrez du 4eme lot','5eme lot','Surface Carrez du 5eme lot','Nombre de lots','Code type local','Identifiant local','Nature culture speciale'], axis=1)
	df2020["Nombre pieces principales"] = pd.to_numeric(df2020["Nombre pieces principales"],downcast='integer')
	return df2020

def test(df2020=pd.DataFrame()):
	if df2020.empty:
		print("###ERROR")
		df2020=load_main()
	df=df2020[['Nature mutation','Surface terrain']]
	df=df.groupby('Nature mutation').mean().sort_values("Surface terrain",ascending=False)
	df.plot.barh(rot=0)
	#plt.show()
	fig = px.bar(df, x="Surface terrain",  orientation='h')
	return html_checkout(fig)


def html_checkout(fig,h=500, w=700):
	return fig.to_html(full_html=False, default_height=h, default_width=w)

