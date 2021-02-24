import math
import typing
from string import ascii_uppercase

from qgis.core import *
from qgis.gui import *

GROUP_NAME = 'Plugin - Custom grid label'


@qgsfunction(args='auto', group=GROUP_NAME)
def get_grid_interval(map_scale, feature, parent):
    if map_scale >= 150000:
        result = 0.066666666668
    elif 99999 <= map_scale < 150000:
        result = 0.033333333334
    elif 49999 <= map_scale < 99999:
        result = 0.016666666667
    elif 24999 <= map_scale < 49999:
        result = 0.0083333333335
    else:
        result = 0.00416666666675
    return result


@qgsfunction(args='auto', group=GROUP_NAME)
def get_grid_label(
        map_width,
        extent_min,
        interval_width,
        current_grid_value,
        use_letters,
        reversed,
        feature,
        parent,
        context
):
    """Calculates the current grid label"""
    num_intervals = math.ceil(map_width / interval_width)
    current_position = current_grid_value - extent_min
    for i in range(num_intervals):
        interval_start = extent_min + i * interval_width
        interval_end = extent_min + (i + 1) * interval_width
        if interval_start <= current_grid_value < interval_end:
            result = _get_choices_label(
                i,
                num_intervals,
                reverse_order=reversed,
                choices=ascii_uppercase if use_letters else None,
            )
            break
    else:
        result = 'error'
    return result


def _get_choices_label(
        current_item: int,
        total_items: int,
        reverse_order: typing.Optional[bool] = False,
        choices: typing.Optional[typing.Iterable] = None,
        offset: typing.Optional[int] = 1,
) -> str:
    if choices is None:
        possible_outputs = range(total_items)
    else:
        possible_outputs = choices
    output_values = list(possible_outputs)[:total_items]
    if reverse_order:
        output_values.reverse()
    return output_values[current_item + offset]