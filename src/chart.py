import uuid

import plotly.express as px
import pandas as pd


def get_chart(data, price) -> str:
    file_name = str(uuid.uuid4())

    fig = make_chart(pd.DataFrame({'date': data, 'price': price}))
    fig.write_image(f'images/{file_name}.webp', width=1280, height=720)

    return file_name


def make_chart(df: pd.DataFrame):
    first, last = df['price'][0], df['price'][df['price'].count()-1]
    min, max = df['price'].min(), df['price'].max()

    fig = px.area(df, x='date', y='price',
                  color_discrete_sequence=[f"{'#a67b77' if first > last else '#87a677'}"],
                  range_y=[min, max])
    fig.add_hline(y=last,
                  line_dash='dot',
                  line_color='#D2D3D9',
                  annotation_text=f"${'{:,}'.format(last)}",
                  annotation_position='top right',
                  annotation_font_color='#D2D3D9')

    fig.update_xaxes(showgrid=False, visible=True, showticklabels=True, gridcolor="#D2D3D9")
    fig.update_yaxes(showgrid=True, visible=True, showticklabels=True, gridcolor='#D2D3D9')
    fig.update_layout(font_family='Ruberoid Medium',
                      yaxis_title=None,
                      xaxis_title=None,
                      plot_bgcolor='#181526',
                      paper_bgcolor='#181526',
                      margin=dict(l=40, r=40, t=25, b=25),
                      yaxis=dict(color='#D2D3D9'),
                      xaxis=dict(color='#D2D3D9'),
                      xaxis_tickformat='%b %d',
                      yaxis_tickprefix='$')
    return fig