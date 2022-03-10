import math
import typing
from string import ascii_uppercase

from qgis.core import *
from qgis.gui import *

from qgis.PyQt.QtCore import *

@qgsfunction(args='auto', group='sagta')
def get_grid_interval(map_scale, feature, parent):
    current_scale = float(map_scale)
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
        
    
@qgsfunction(args='auto', group='sagta')
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
    """
    Calculates the current X label.
    <h2>Example usage:</h2>
    <ul>
      <li>my_sum(5, 8) -> 13</li>
      <li>my_sum("field1", "field2") -> 42</li>
    </ul>
    """
    num_intervals = math.ceil(map_width / interval_width)  # Number of grid blocks
    current_position = current_grid_value - extent_min  # Label position
    
    for i in range(num_intervals):  # Loops through each of the grids
        interval_start = extent_min + i * interval_width  # Grid start coordinates
        interval_end = extent_min + (i + 1) * interval_width  # Grid end coordinates
        
        # Find the grid block which needs to be labelled
        if interval_start <= current_grid_value < interval_end:
            result = get_choices_label(
                i,
                num_intervals,
                reverse_order=reversed,
                choices=ascii_uppercase if use_letters else None,
            )
            break
    else:  # When the loop ends
        result = 'error'
    
    return result
    
    
def get_choices_label(
        current_item: int,
        total_items: int,
        reverse_order: typing.Optional[bool] = False,
        choices: typing.Optional[typing.Iterable] = None,
        offset: typing.Optional[int] = 1,
) -> str:
    output_values = None
    if choices is None:  # x-axis, therefore integer values
        # Increments with one to be sure to include the last grid block case
        possible_outputs = range(total_items + 1)
        output_values = list(possible_outputs)[:total_items + 1]
    else:  # y-axis, therefore alphabetical characters
        possible_outputs = choices
        output_values = list(possible_outputs)[:total_items]
    
    if reverse_order:  # This is only done for the y-axis - alphabetical characters
        output_values.reverse()
    
    return output_values[current_item + offset]
