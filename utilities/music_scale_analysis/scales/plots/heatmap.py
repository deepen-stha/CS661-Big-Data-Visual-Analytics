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


def show_heatmap(
    df,
    property,
    use_sharp_notation=True,
    show_title=True,
    standalone=False,
):
    """
    Heatmap of `property` by Scale and Key.
    """

    # Create a new column for the pitch class notation
    df['pitch_class'] = df['key'].map(
        pitch_class_map_sharp if use_sharp_notation else pitch_class_map_flat
    )

    # Sort the rows (keys) based on pitch class order
    if use_sharp_notation:
        sorted_keys = [pitch_class_map_sharp[i] for i in range(12)][::-1]
    else:
        sorted_keys = [pitch_class_map_flat[i] for i in range(12)][::-1]

    # Create a new DataFrame for the heatmap
    heatmap_df = pd.pivot_table(
        df,
        values=property,
        index='pitch_class',
        columns='major',
    )
    heatmap_df = heatmap_df.reindex(sorted_keys)

    # Create and display the plot
    fig = px.imshow(
        heatmap_df,
        x=['Minor', 'Major'],
        y=sorted_keys,
        color_continuous_scale='deep',
    )
    fig.update_xaxes(title='Scale')
    fig.update_yaxes(title='Key')
    fig.update_coloraxes(colorbar_title=property.capitalize())
    if show_title:
        fig.update_layout(
            title=f'{property.capitalize()} heatmap of Scales',
        )

    # Use the result
    if standalone:
        fig.show()
    else:
        return fig


# Demo
if __name__ == '__main__':
    show_heatmap(
        df=initialize(),
        property=properties[0],
        use_sharp_notation=True,
        show_title=True,
        standalone=True,
    )
