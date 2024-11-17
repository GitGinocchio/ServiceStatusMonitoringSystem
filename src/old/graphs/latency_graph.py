from datetime import datetime,timezone
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np
import json

import mpld3

#plt.style.use('seaborn-v0_8-darkgrid') #'seaborn-v0_8-deep' 'seaborn-v0_8-pastel' 'seaborn-v0_8-darkgrid' 'Solarize_Light2' 'seaborn-v0_8-white' 'ggplot'
plt.rcParams['legend.fontsize'] = 17

from utils import generate_spline_curve

# Leggi il file JSON
with open('./data/services/google/google.json') as f:
    data = json.load(f)

# Estrai le metriche
metrics = data['metrics']
overall = [metric['overall'] for metric in metrics]

# Crea un DataFrame dalle metriche
metrics_df = pd.DataFrame(metrics[-10::])
overall_df = pd.DataFrame(overall[-10::])

# Convertilo in formato datetime
metrics_df['timestamp'] = pd.to_datetime(metrics_df['timestamp'],dayfirst=True,format='ISO8601', utc=True)

x_int = [int(date.timestamp()) for date in metrics_df['timestamp']]

x_latency, y_latency = generate_spline_curve(x_int, metrics_df['latency'], num_points=100000, clip_y=(0,np.inf))
#x_avg_latency, y_avg_latency = generate_spline_curve(x_int, overall_df['avg-latency'], line=x_latency, num_points=100000,clip_y=(0,np.inf))

x_plot_datetime = [datetime.fromtimestamp(x,timezone.utc) for x in x_latency]

plt.plot(x_plot_datetime, y_latency, label='Latency',color='tab:purple', linewidth=2)
#plt.plot(metrics_df['timestamp'], metrics_df['latency'], label='Latency',color='tab:purple', linewidth=2)
plt.plot(metrics_df['timestamp'], metrics_df['latency'], 'o', label='Latency',color='purple', markersize=3)

plt.fill_between(x_plot_datetime,y_latency, alpha=0.3)

#plt.plot(x_plot_datetime, y_avg_latency, label='Average Latency',color='tab:blue', linewidth=2)
#plt.plot(metrics_df['timestamp'], overall_df['avg-latency'], label='Average Latency',color='tab:blue', linewidth=2)
#plt.plot(metrics_df['timestamp'], overall_df['avg-latency'], 'o', label='Average Latency',color='blue', markersize=3)

# Add tick marks on the x-axis
#date_formatter = mdates.DateFormatter('%d-%m-%Y')
#plt.gca().xaxis.set_major_locator(mdates.DayLocator())
#plt.gca().xaxis.set_major_formatter(date_formatter)

#hour_formatter = mdates.DateFormatter('%H:%M')
#plt.gca().xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0,24,2)))
#plt.gca().xaxis.set_minor_formatter(hour_formatter)

# Set tick sizes
#plt.gca().xaxis.set_tick_params(which='major', size=12)
#plt.gca().xaxis.set_tick_params(which='minor', size=2)

#plt.title("Latency",loc='left', fontsize=20, fontweight="bold",color='black')
#legend = plt.legend(loc='best')
plt.axis("off")

# Impostare lo sfondo della legenda
#frame = legend.get_frame()
#frame.set_facecolor((0.15, 0.15, 0.15, 1.00)) # Sfondo grigio

#for text in legend.texts: text.set_color('white')  # Colore del testo: bianco

plt.savefig("latency.png",transparent=True, dpi=1000,bbox_inches='tight', pad_inches=0)
plt.show()

#figure = plt.gcf()
#mpld3.show(figure, port=5000)

# Salva come file HTML interattivo con mpld3
#html_str = mpld3.fig_to_html(figure)
#with open("latency.html", "w") as f:
    #f.write(html_str)