import uuid

import plotly.express as px
import pandas as pd

from crypto import get_prices


def get_chart(coin_id: str) -> str:
    data, price = get_prices(coin_id)
    df = pd.DataFrame({"date": data, "price": price})
    
    fig = px.line(df, x='date', y="price")
    
    file_name = str(uuid.uuid4())
    fig.write_image(f"images/{file_name}.webp")
    
    return file_name
