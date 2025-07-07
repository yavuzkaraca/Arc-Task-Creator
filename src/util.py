import os


def get_output_path(template_name: str, filename: str = "output.png") -> str:
    """
    Returns a clean output path like: out/occlusion/overlap_input.png
    Creates the folders if they don't exist.
    """
    base_dir = "../out"
    sub_dir = os.path.join(base_dir, template_name)
    os.makedirs(sub_dir, exist_ok=True)
    return os.path.join(sub_dir, filename)
