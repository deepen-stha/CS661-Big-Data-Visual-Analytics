"""
Copyright 2024 Indraneel Rajeevan
SPDX-License-Identifier: BSD-3-Clause

Project:
IIT Kanpur CS661 End-semester Activity,
Music Data Visualization,
Music Scale Analysis (Valence-Mode)
"""

import runpy

runpy.run_module(
    'utilities.music_scale_analysis.music_scale_analysis',
    run_name='__main__',
    alter_sys=True,
)
