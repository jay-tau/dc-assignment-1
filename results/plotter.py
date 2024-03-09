"""
This script plots the average response time and total response time for each cluster size.

and saves the plots as .png files. It also creates a table with the average response time
and total response time for each cluster size and saves it as a .csv file.

Usage:
    python plotter.py
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df_1 = pd.read_csv("data/response_data_1.csv")
df_2 = pd.read_csv("data/response_data_2.csv")
df_4 = pd.read_csv("data/response_data_4.csv")
df_8 = pd.read_csv("data/response_data_8.csv")
df_16 = pd.read_csv("data/response_data_16.csv")
df_32 = pd.read_csv("data/response_data_32.csv")


avg_response_time_1 = df_1["response_time"].mean()
total_response_time_1 = df_1["response_time"].sum()
avg_response_time_2 = df_2["response_time"].mean()
total_response_time_2 = df_2["response_time"].sum()
avg_response_time_4 = df_4["response_time"].mean()
total_response_time_4 = df_4["response_time"].sum()
avg_response_time_8 = df_8["response_time"].mean()
total_response_time_8 = df_8["response_time"].sum()
avg_response_time_16 = df_16["response_time"].mean()
total_response_time_16 = df_16["response_time"].sum()
avg_response_time_32 = df_32["response_time"].mean()
total_response_time_32 = df_32["response_time"].sum()

average_response_times = np.array(
    [
        avg_response_time_1,
        avg_response_time_2,
        avg_response_time_4,
        avg_response_time_8,
        avg_response_time_16,
        avg_response_time_32,
    ]
)
average_response_times = average_response_times * 1000

total_response_times = [
    total_response_time_1,
    total_response_time_2,
    total_response_time_4,
    total_response_time_8,
    total_response_time_16,
    total_response_time_32,
]
x_data = [1, 2, 4, 8, 16, 32]

plt.plot(x_data, average_response_times, label="Average Response Time")
plt.title("Average Response Time vs Cluster Size")
plt.xlabel("Cluster Size")
plt.ylabel("Average Response Time (ms)")
plt.savefig("average_response_time.png")

plt.clf()

plt.plot(x_data, total_response_times, label="Total Response Time")
plt.title("Total Response Time vs Cluster Size")
plt.xlabel("Cluster Size")
plt.ylabel("Total Response Time (s)")
plt.savefig("total_response_time.png")

# Make a table with total response times and average response time as colums and rows as cluster size
# Save the table as a csv file
table = pd.DataFrame(
    {
        "Cluster Size": x_data,
        "Average Response Time (ms)": average_response_times,
        "Total Response Time (s)": total_response_times,
    }
)
table.to_csv("response_time_table.csv", index=False)
