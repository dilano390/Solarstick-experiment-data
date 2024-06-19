import sys
import json
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime
import numpy as np
import matplotlib.ticker as ticker

statistics_interval = 1
metrics_path = sys.argv[1]
metric_names_path = "metric_names.json"
timestamp =  datetime.datetime.now().strftime("%d_%H_%M")

with open(metric_names_path) as metric_names_file:
    metric_types = json.load(metric_names_file)
    with open(metrics_path) as file:
        data = json.load(file) 
        for i in range(len(data)):  
            current_metric_type = metric_types[i]
            metric_data = data[i]
            metric_data = json.loads(metric_data)
            all_values = []
            fig, ax = plt.subplots(figsize=(10, 6))
            
            for metric in metric_data['data']['result']:
                metric_values = metric['values']
                metric_values = [float(x[1]) for x in metric_values]
                all_values.append(metric_values)
                std_dev = np.std(metric_values, axis=0)
                mean = np.mean(metric_values,axis=0)
                print("Mean: ", mean," Std_dev: ",std_dev,current_metric_type['graph_title'])
                ax.plot(metric_values)    
            

            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=60))
            ax.xaxis.set_minor_locator(ticker.MultipleLocator(base=30))
            ax.set_xlabel("Time[s]")
            ax.set_ylabel("{0}".format(current_metric_type['y_label']))
            plt.tight_layout()
            plt.margins(0)
            ax.grid(True,which="both",linestyle='--', alpha=0.5)
            fig.savefig("temp/plot{0}.png".format(current_metric_type['graph_title'].replace(" ", "")), bbox_inches='tight')
            plt.clf()