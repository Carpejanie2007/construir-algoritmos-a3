import os
import requests
from dotenv import load_dotenv
from folium import Map, Marker, Popup, Icon

load_dotenv(".env")

s = requests.Session()
res = s.post(
    f"https://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={os.getenv('SPTRANS_TOKEN')}"
)
print(res.text)

paradas = s.get("https://api.olhovivo.sptrans.com.br/v2.1/Parada/Buscar?termosBusca=8000")
paradas = paradas.json()
print(paradas)


m = Map(location=[-23.55052, -46.633308], zoom_start=12)

for parada in paradas:
    nome_parada = parada.get("np")
    parada_py = parada.get("py")
    parada_px = parada.get("px")

    if parada_px is not None and parada_py is not None:
         Marker(
            location=[parada_py, parada_px], 
            popup=Popup(nome_parada, max_width="200")
        ).add_to(m)

         
posicao = s.get("https://api.olhovivo.sptrans.com.br/v2.1//Posicao/Linha?codigoLinha=8000")
posicao_json = posicao.json()
veiculos = posicao_json.get("vs", [])

for onibus in veiculos:
    onibus_py = onibus.get("py")  
    onibus_px = onibus.get("px")  
    prefixo = onibus.get("p")   
    
    if onibus_py is not None and onibus_px is not None:
        
        Marker(
            location=[onibus_py, onibus_px],
            popup=Popup(f"Busão {prefixo} Aqui!", max_width="200"),
            icon=Icon(color="red", icon="info-sign")
        ).add_to(m)

m.save("unasp.html")