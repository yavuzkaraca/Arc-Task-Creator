from rules.occlusion import generate_occlusion_reversal


def generate_occlusion_mirror_x(grid_size=(12, 12), size_range=(2, 5), colors=("red", "blue")):
    grid_input, _, _ = generate_occlusion_reversal(
        grid_size=grid_size, size_range=size_range, colors=colors
    )

    # TODO: abstract out the grid_input creation to reduce code redundancy

    grid_output = grid_input.copy()
    grid_output.mirror_x()

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": 2
    }

    return grid_input, grid_output, params


def generate_occlusion_mirror_y(grid_size=(12, 12), size_range=(2, 5), colors=("red", "blue")):
    grid_input, _, _ = generate_occlusion_reversal(
        grid_size=grid_size, size_range=size_range, colors=colors
    )
    grid_output = grid_input.copy()
    grid_output.mirror_y()

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": 2
    }

    return grid_input, grid_output, params


def generate_occlusion_rotate_90(grid_size=(12, 12), size_range=(2, 5), colors=("red", "blue")):
    grid_input, _, _ = generate_occlusion_reversal(
        grid_size=grid_size, size_range=size_range, colors=colors
    )
    grid_output = grid_input.copy()
    grid_output.rotate_left_90()

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": 2
    }

    return grid_input, grid_output, params


def generate_occlusion_rotate_180(grid_size=(12, 12), size_range=(2, 5), colors=("red", "blue")):
    grid_input, _, _ = generate_occlusion_reversal(
        grid_size=grid_size, size_range=size_range, colors=colors
    )
    grid_output = grid_input.copy()
    grid_output.rotate_left_90()
    grid_output.rotate_left_90()

    params = {
        "grid_size": grid_size,
        "colors": colors,
        "n_objects": 2
    }

    return grid_input, grid_output, params
