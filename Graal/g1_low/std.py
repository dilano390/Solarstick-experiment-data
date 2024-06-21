import sys
import json
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime
import numpy as np
import matplotlib.ticker as ticker
import scipy.stats as stats
import os


statistics_interval = 1
metrics_paths = ["20_20_28/metrics.json","20_20_36/metrics.json","20_20_44/metrics.json"]
metric_names_path = "metric_names.json"
timestamp =  datetime.datetime.now().strftime("%d_%H_%M")

with open(metric_names_path) as metric_names_file:
    metric_types = json.load(metric_names_file)
    metric_files = [open(metric_path) for metric_path in metrics_paths]
    all_data = [json.load(file) for file in metric_files]
    for i in range(len(all_data[0])):
        current_metric_type = metric_types[i]
        metric_data_list = [json.loads(data[i]) for data in all_data]
        fig, ax = plt.subplots(figsize=(10, 6))
        metric_results = [metric['data']['result'] for metric in metric_data_list]
        
        all_data_points = []
        for metric_data in metric_results:
            for x in metric_data:
                data_points = x['values']
                data_points = [float(x[1]) for x in data_points]
                for y in data_points:
                    all_data_points.append(y)  
            
        ax.set_xlabel("{0}".format(current_metric_type['y_label']))
        ax.boxplot(all_data_points,vert=False,patch_artist=True,meanline=True,showmeans=False,showfliers=True)
        plt.tight_layout()
        fig.savefig("collective/{0}_boxplot.png".format(current_metric_type['graph_title'].replace(" ", "")), bbox_inches='tight')
        fig.savefig("collective/{0}_boxplot.pdf".format(current_metric_type['graph_title'].replace(" ", "")), bbox_inches='tight')
        plt.clf


        data_points_np = np.array(all_data_points)
                
        mean = np.mean(data_points_np)
        std_dev = np.std(data_points_np)
        variance = np.var(data_points_np)
        median = np.median(data_points_np)
        mode = stats.mode(data_points_np)
        data_range = np.ptp(data_points_np)
        percentiles = np.percentile(data_points_np, [25, 50, 75, 90, 95])
        iqr = stats.iqr(data_points_np)
        skewness = stats.skew(data_points_np)
        kurtosis = stats.kurtosis(data_points_np)
        minimum = np.min(data_points_np)
        maximum = np.max(data_points_np)
        confidence_interval = stats.norm.interval(0.95, loc=mean, scale=std_dev/np.sqrt(len(data_points_np)))
        
        results = (
        f"Mean: {mean:.2f} \n"
        f"Standard Deviation: {std_dev:.2f} \n"
        f"Variance: {variance:.2f} ^2\n"
        f"Median: {median:.2f} \n"
        f"Mode: {mode}\n"
        f"Range: {data_range:.2f} \n"
        f"25th, 50th, 75th, 90th, 95th Percentiles: {percentiles}\n"
        f"Interquartile Range (IQR): {iqr:.2f} \n"
        f"Skewness: {skewness:.2f}\n"
        f"Kurtosis: {kurtosis:.2f}\n"
        f"Minimum: {minimum:.2f} \n"
        f"Maximum: {maximum:.2f} \n"
        f"95% Confidence Interval: {confidence_interval}\n"
        )

        with open("collective/{0}_statistics.txt".format(current_metric_type['graph_title'].replace(" ", "")), 'w') as output_file:
            output_file.write(results)


        