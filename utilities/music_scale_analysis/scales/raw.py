"""
Copyright 2024 Indraneel Rajeevan
SPDX-License-Identifier: BSD-3-Clause

Project:
IIT Kanpur CS661 End-semester Activity,
Music Data Visualization,
Music Scale Analysis (Valence-Mode)
"""

from pathlib import Path

import numpy as np
import pandas as pd

from scales.attributes import *

# Map of integer keys to pitch class notation (sharp)
pitch_class_map_sharp = {
    0: 'C',
    1: 'C#',
    2: 'D',
    3: 'D#',
    4: 'E',
    5: 'F',
    6: 'F#',
    7: 'G',
    8: 'G#',
    9: 'A',
    10: 'A#',
    11: 'B',
}

# Map of integer keys to pitch class notation (flat)
pitch_class_map_flat = {
    0: 'C',
    1: 'Db',
    2: 'D',
    3: 'Eb',
    4: 'E',
    5: 'F',
    6: 'Gb',
    7: 'G',
    8: 'Ab',
    9: 'A',
    10: 'Bb',
    11: 'B',
}

# List of all the 34 scales (sorted lexicographically)
scales = list(
    sorted(
        set(
            [
                f'{k}-{m}'
                for k in list(pitch_class_map_sharp.values())
                + list(pitch_class_map_flat.values())
                for m in ('Major', 'Minor')
            ]
        )
    )
)


def get_scaled_key(scale_key, use_sharp_notation=True):
    """
    Converts `scale_key` (int) to its corresponding string representation,
    based on `use_sharp_notation` (sharp/flat) notation.
    """
    if use_sharp_notation:
        return pitch_class_map_sharp.get(scale_key)
    else:
        return pitch_class_map_flat.get(scale_key)


def initialize():
    """
    Heavyweight initialization.
    """

    # Load the Dataset
    data = np.load(f'{Path(__file__).parent.absolute()}/datasets/scales.npz')

    # Create the DataFrame
    return pd.DataFrame(
        {
            key: data[key],
            major: data[major],
            valence: data[valence],
            energy: data[energy],
            speechiness: data[speechiness],
            acousticness: data[acousticness],
            instrumentalness: data[instrumentalness],
            danceability: data[danceability],
            liveness: data[liveness],
        }
    )
