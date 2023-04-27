def extract_lambda_name_from_top_dir(root_dir: str):
    directory = root_dir.replace("/src", "")
    splits = directory.split('/')
    return f"{splits[-3]}_{splits[-2]}_{splits[-1]}"
