import uuid

import plotly.express as px
import pandas as pd


def get_chart(data, price) -> str:
    df = pd.DataFrame({"date": data, "price": price})

    fig = px.area(df, x='date', y="price", color_discrete_sequence=[f"{'#a5787a' if price[0] > price[-1] else '#7ea578'}"], range_y=[min(price), max(price)])
    fig.add_hline(y=price[-1],
                  line_dash="dot",
                  line_color="#D0D0D9",
                  annotation_text=f"${'{:,}'.format(price[-1])}",
                  annotation_position="bottom right",
                  annotation_font_color="#D0D0D9")
    
    fig.update_xaxes(showgrid=False, visible=True, showticklabels=True, gridcolor="#D0D0D9")
    fig.update_yaxes(showgrid=True, visible=True, showticklabels=True, gridcolor="#D0D0D9")
    fig.update_layout(font_family="verdana",
                      yaxis_title=None,
                      xaxis_title=None,
                      plot_bgcolor='#181526',
                      paper_bgcolor="#181526",
                      margin=dict(l=40, r=40, t=25, b=25),
                      yaxis = dict(color = "#D0D0D9"),
                      xaxis = dict(color = "#D0D0D9"),
                      xaxis_tickformat = '%b %d',
                      yaxis_tickprefix = '$')
    
    file_name = str(uuid.uuid4())
    fig.write_image(f"images/{file_name}.webp", width=1280, height=720)
    
    return file_name
