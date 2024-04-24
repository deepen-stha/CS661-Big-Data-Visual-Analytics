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


def show_piechart(
    df,
    scale,
    features,
    show_title=True,
    standalone=False,
):
    """
    Feature Contribution for `scale` out of the given `features`.
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

    # Calculate the sum-contribution of each property
    feature_sums = filtered_df[features].sum()
    contributions = {
        features[i]: feature_sums.iloc[i] for i in range(len(features))
    }

    # Create and display the plot
    fig = px.pie(
        pd.DataFrame.from_dict(
            contributions,
            orient='index',
            columns=['Contribution'],
        ),
        values='Contribution',
        names=feature_sums.index,
    )
    fig.update_layout(
        margin=dict(b=0),
    )
    if show_title:
        fig.update_layout(
            title=f'{scale} Features',
        )

    # Use the result
    if standalone:
        fig.show()
    else:
        return fig


# Demo
if __name__ == '__main__':
    show_piechart(
        df=initialize(),
        scale=scales[0],
        features=properties,
        show_title=True,
        standalone=True,
    )
