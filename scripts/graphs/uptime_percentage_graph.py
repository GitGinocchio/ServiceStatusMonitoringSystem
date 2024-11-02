from datetime import datetime,timezone
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import json

import mpld3
from mpld3 import plugins

sns.set_palette("viridis")

plt.style.use('seaborn-v0_8-darkgrid') #'seaborn-v0_8-deep' 'seaborn-v0_8-pastel' 'seaborn-v0_8-darkgrid' 'Solarize_Light2' 'seaborn-v0_8-white' 'ggplot'

from utils import generate_spline_curve

# Leggi il file JSON
with open('./data/services/google/google.json') as f:
    data = json.load(f)

# Estrai le metriche
metrics = data['metrics']
overall = [metric['overall'] for metric in metrics]

# Crea un DataFrame dalle metriche
metrics_df = pd.DataFrame(metrics)#[-100::])
overall_df = pd.DataFrame(overall)#[-100::])

# Convertilo in formato datetime
metrics_df['timestamp'] = pd.to_datetime(metrics_df['timestamp'],dayfirst=True,format='ISO8601', utc=True)

int_timestamp = [int(date.timestamp()) for date in metrics_df['timestamp']]

line, uptime_y = generate_spline_curve(int_timestamp,metrics_df['uptime-percentage'],num_points=10000,clip_y=(0, 100))

line_timestamps = [datetime.fromtimestamp(x,timezone.utc) for x in line]

#plt.plot(line_timestamps, uptime_y, label='Uptime %', color='tab:green', linewidth=1.5)
plt.plot(metrics_df['timestamp'], metrics_df['uptime-percentage'], label='Uptime %', color='tab:green', linewidth=5)
plt.plot(metrics_df['timestamp'], metrics_df['uptime-percentage'],'o', label='Uptime %',color='green', markersize=7)

plt.plot(metrics_df['timestamp'], overall_df['avg-uptime-percentage'], label='Average Uptime %', color='tab:blue', linewidth=5)
plt.plot(metrics_df['timestamp'], overall_df['avg-uptime-percentage'],'o', label='Average Uptime %',color='blue', markersize=7)

plt.ylim(-10,110)

# Add tick marks on the x-axis
date_formatter = mdates.DateFormatter('%d-%m-%Y')
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
plt.gca().xaxis.set_major_formatter(date_formatter)

hour_formatter = mdates.DateFormatter('%H:%M')
plt.gca().xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0,24,2)))
plt.gca().xaxis.set_minor_formatter(hour_formatter)

# Set tick sizes
plt.gca().xaxis.set_tick_params(which='major', size=12)
plt.gca().xaxis.set_tick_params(which='minor', size=2)

plt.title("Uptime %",loc='left', fontsize=15, fontweight="bold",color='white')
legend = plt.legend(loc='best')

# Impostare lo sfondo della legenda
frame = legend.get_frame()
frame.set_facecolor((0.15, 0.15, 0.15, 1.00)) # Sfondo grigio

for text in legend.texts: text.set_color('white')  # Colore del testo: bianco

#plt.savefig("uptime_percentage.png",transparent=True, dpi=1000)
#plt.show()

# Aggiungere tooltip ai punti dati
#tooltip = plugins.PointLabelTooltip(ax.collections, labels=[str(val) for val in metrics_df['timestamp']])
#plugins.connect(figure, tooltip)

figure = plt.gcf()
#mpld3.show(figure)

# Salva come file HTML interattivo con mpld3
html_str = mpld3.fig_to_html(figure)
with open("uptime_percentage.html", "w") as f:
    f.write(html_str)