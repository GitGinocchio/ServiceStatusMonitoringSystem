import json
import matplotlib.pyplot as plt
import pandas as pd

# Leggi il file JSON
with open('./data/services/google.json') as f:
    data = json.load(f)

# Estrai le metriche
metrics = data['metrics']

# Crea un DataFrame dalle metriche
df = pd.DataFrame(metrics)

# Convertilo in formato datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Imposta il timestamp come indice
df.set_index('timestamp', inplace=True)

# Crea il grafico
plt.figure(figsize=(14, 10))

# Grafico per la latenza
plt.subplot(3, 2, 1)
plt.plot(df.index, df['latency'], label='Latenza', color='blue')
plt.title('Latenza')
plt.xlabel('Timestamp')
plt.ylabel('Latenza (s)')
plt.ylim(0, 1.0)
plt.grid()

# Grafico per l'uptime
plt.subplot(3, 2, 2)
plt.plot(df.index, df['uptime'], label='Uptime', color='green')
plt.title('Uptime')
plt.xlabel('Timestamp')
plt.ylabel('Uptime (s)')
plt.grid()

# Grafico per il downtime
plt.subplot(3, 2, 3)
plt.plot(df.index, df['downtime'], label='Downtime', color='red')
plt.title('Downtime')
plt.xlabel('Timestamp')
plt.ylabel('Downtime (s)')
plt.grid()

# Grafico per l'uptime percentage
plt.subplot(3, 2, 4)
plt.plot(df.index, df['uptime-percentage'], label='Uptime Percentage', color='orange')
plt.title('Uptime Percentage')
plt.xlabel('Timestamp')
plt.ylabel('Uptime Percentage (%)')
plt.ylim(0, 110)
plt.grid()

# Grafico per il downtime percentage
plt.subplot(3, 2, 5)
plt.plot(df.index, df['downtime-percentage'], label='Downtime Percentage', color='purple')
plt.title('Downtime Percentage')
plt.xlabel('Timestamp')
plt.ylabel('Downtime Percentage (%)')
plt.ylim(0, 110)
plt.grid()

# Grafico per il codice di stato con linee spezzate
plt.subplot(3, 2, 6)
plt.plot(df.index, df['code'], label='HTTP Code', color='black', marker='o', linestyle='--')  # Linea spezzata
plt.title('HTTP Code')
plt.xlabel('Timestamp')
plt.ylabel('HTTP Code')
plt.ylim(100, 599)
plt.grid()

plt.tight_layout()
plt.savefig('./data/graphsgrafici.png')
plt.show()