#!/usr/bin/python3
"""
Author:     Konstantinos Liosis
File:       temp_graph.py
Desc:       Plot temperature data
"""

import plotly.graph_objects as go
from queries import yearly_avg, monthly_avg

# Add data
months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July',
          8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

colors = ["#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231", "#911eb4", "#46f0f0", "#f032e6",
          "#bcf60c", "#fabebe", "#008080", "#e6beff", "#9a6324", "#fffac8", "#800000", "#aaffc3",
          "#808000", "#ffd8b1", "#000075", "#808080", "#ffffff", "#000000"]


#
# fig.add_trace(go.Scatter(x=month, y=low_2014, name='Low 2014',
#                          line=dict(color='royalblue', width=4)))
# fig.add_trace(go.Scatter(x=month, y=high_2007, name='High 2007',
#                          line=dict(color='firebrick', width=4,
#                                    dash='dash')  # dash options include 'dash', 'dot', and 'dashdot'
#                          ))
# fig.add_trace(go.Scatter(x=month, y=low_2007, name='Low 2007',
#                          line=dict(color='royalblue', width=4, dash='dash')))
# fig.add_trace(go.Scatter(x=month, y=high_2000, name='High 2000',
#                          line=dict(color='firebrick', width=4, dash='dot')))
# fig.add_trace(go.Scatter(x=month, y=low_2000, name='Low 2000',
#                          line=dict(color='royalblue', width=4, dash='dot')))
#



def draw(db_conn, choice, month):
    # docstring

    # Yearly avg
    if choice == 2:
        TITLE = "Average month temperatures"
        X_AXIS = "Month"
        x_data = list(months.values())
        data = yearly_avg(db_conn)

    # Monthly avg
    elif choice == 1:
        TITLE = "Average daily temperature for " + months[month]
        X_AXIS = "Days"
        x_data = list(range(1, 31))
        data = monthly_avg(db_conn, month)

    fig = go.Figure()


    for idx, year in enumerate(data.keys()):
        fig.add_trace(go.Scatter(x=x_data, y=data[year], name= year,
                                 line=dict(color=colors[idx], width=4)))



    # Edit the layout
    fig.update_layout(title=TITLE,
                      xaxis_title=X_AXIS,
                      yaxis_title='Temperature (degrees C)')

    fig.show()