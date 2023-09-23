import colorsys


def get_distinct_colors(n: int) -> list:
    """
    Get a list of n distinguishable colors in hexadecimal format.

    Parameters:
    - n: Number of colors required.

    Returns:
    - A list of n colors in hexadecimal.
    """
    HSV_tuples = [(x * 1.0 / n, 0.5, 0.5) for x in range(n)]
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    hex_out = []
    for rgb in RGB_tuples:
        hex_out.append(
            "#{:02x}{:02x}{:02x}".format(
                int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
            )
        )
    return hex_out
