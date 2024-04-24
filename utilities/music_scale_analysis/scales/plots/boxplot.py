"""
Copyright 2024 Indraneel Rajeevan
SPDX-License-Identifier: BSD-3-Clause

Project:
IIT Kanpur CS661 End-semester Activity,
Music Data Visualization,
Music Scale Analysis (Valence-Mode)
"""

import plotly.express as px

from scales.raw import *
from scales.attributes import *


def show_boxplot(
    df,
    property,
    scale,
    show_title=True,
    standalone=False,
):
    """
    Box Plot of `property` by the given `scale`.
    """

    # Extract key and major from the scale
    scale_key, scale_type = scale.split('-')

    # Create a new column for the pitch class notation
    df['pitch_class'] = df['key'].map(
        pitch_class_map_sharp
        if (len(scale_key) > 1 and scale_key[1] == '#')
        else pitch_class_map_flat
    )

    # Filter the DataFrame based on the specified scale
    filtered_df = df[
        (df['pitch_class'] == scale_key)
        & (df['major'] == (scale_type == 'Major'))
    ]

    # Create and display the plot
    fig = px.box(
        filtered_df,
        y=property,
    )
    fig.update_xaxes(title=scale)
    fig.update_yaxes(title=property.capitalize())
    if show_title:
        fig.update_layout(
            title=f'{property.capitalize()} of {scale}',
        )

    # Use the result
    if standalone:
        fig.show()
    else:
        return fig


# Demo
if __name__ == '__main__':
    show_boxplot(
        df=initialize(),
        property=properties[0],
        scale=scales[0],
        show_title=True,
        standalone=True,
    )
