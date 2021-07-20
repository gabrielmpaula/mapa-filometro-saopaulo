import json
import folium
import requests


def update_data():
    url = 'https://deolhonafila.prefeitura.sp.gov.br/processadores/dados.php'
    form = {'dados': 'dados'}
    data = requests.post(url, data=form).json()
    return data


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

    colors = {'SEM FILA': 'darkgreen',
              'FILA PEQUENA': 'beige',
              'FILA MÉDIA': 'orange',
              'FILA GRANDE': 'red',
              'NÃO FUNCIONANDO': 'purple',
              'AGUARDANDO ABASTECIMENTO': 'gray'}

    geodata_path = '../data/geodata.json'
    with open(geodata_path) as f:
        geodata = json.load(f)

    geo_sp = (-23.80128, -46.658112)
    map = folium.Map(geo_sp, zoom_start=10)

    for item in data:

        name = item['equipamento']
        color = colors[item['status_fila']]
        text = 'Atualização:\n' + item['data_hora']
        location = geodata[name]['location'].values()
        folium.Marker(tuple(location), tooltip=name, popup=text, icon=folium.Icon(color=color)).add_to(map)

    map = add_categorical_legend(map, 'Legenda',
                                colors = colors.values(),
                               labels = colors.keys())

    return map