import os
import json
import folium
import requests


def update_data():
    url = 'https://deolhonafila.prefeitura.sp.gov.br/processadores/dados.php'
    form = {'dados': 'dados'}
    return requests.post(url, data=form).json()


def add_categorical_legend(folium_map, title, colors, labels):

    if len(colors) != len(labels):
        raise ValueError("colors and labels must have the same length.")

    color_by_label = dict(zip(labels, colors))

    legend_categories = ""
    for label, color in color_by_label.items():
        legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"
        
    legend_html = f"""
    <div id='maplegend' class='maplegend'>
      <div class='legend-title'>{title}</div>
      <div class='legend-scale'>
        <ul class='legend-labels'>
        {legend_categories}
        </ul>
      </div>
    </div>
    """
    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """

    css = """
    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))
    return folium_map


def plot_map(data):

    brand_list = ['coronavac', 'astrazeneca', 'pfizer']
    colors = {'SEM FILA': 'darkgreen',
              'FILA PEQUENA': 'beige',
              'FILA MÉDIA': 'orange',
              'FILA GRANDE': 'red',
              'NÃO FUNCIONANDO': 'purple',
              'AGUARDANDO ABASTECIMENTO': 'gray'}

    cwd = os.path.dirname(__file__)
    geodata_filename = '../data/geodata.json'
    geodata_path = os.path.join(cwd, geodata_filename)
    with open(geodata_path) as f:
        geodata = json.load(f)

    geo_sp = (-23.62, -46.53)
    m = folium.Map(geo_sp, zoom_start=10, height='100%')
    fig = folium.Figure(height=500)

    for item in data:

        name = item.get('equipamento')
        status = item.get('status_fila')
        color = colors.get(status) or 'gray'
        place = geodata.get(name)

        if place:
            availablity = []
            location = place['location'].values()
            lat, lon = location
            tooltip_text = name + ' | ' + item.get('tipo_posto')
            maps_url = f'https://www.google.com/maps/dir//{lat},{lon}'

            for brand in brand_list:
                if item[brand] == '1':
                    availablity += [f'<br>{brand.title()}: <span style="color:Green";>Sim</span>']
                if item[brand] == '0':
                    availablity += [f'<br>{brand.title()}: <span style="color:Red";>Não</span>']

            brands = f'<br><br><b>Imunizantes 2ª dose</b>:{"".join(availablity)}<br>'
            maps_link = f'<br><a href="{maps_url}" target="_blank"><b>Ver no Google Maps</b></a>'
            popup_text = '<b>Última atualização:</b><br>' + item['data_hora'] + brands + maps_link
            popup = folium.Popup(html=popup_text, parse_html=False, max_width=200)
            folium.Marker(tuple(location), tooltip=tooltip_text, popup=popup, icon=folium.Icon(color=color)).add_to(m)

    fig = fig.add_child(m)
    map_clean = fig._repr_html_()

    fig_leg = add_categorical_legend(fig, 'Legenda', 
                                 colors = colors.values(),
                                 labels = colors.keys())
    map_leg = fig_leg._repr_html_()

    return map_clean, map_leg
