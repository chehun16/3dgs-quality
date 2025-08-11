import os
import json

camera_dir = "room8/keyframes/cameras"
output_path = "room8/keyframes/transforms.json"

frames = []

for fname in os.listdir(camera_dir):
    if not fname.endswith(".json"):
        continue

    full_path = os.path.join(camera_dir, fname)
    with open(full_path, "r") as f:
        meta = json.load(f)

    transform_matrix = [
        [meta["t_00"], meta["t_01"], meta["t_02"], meta["t_03"]],
        [meta["t_10"], meta["t_11"], meta["t_12"], meta["t_13"]],
        [meta["t_20"], meta["t_21"], meta["t_22"], meta["t_23"]],
        [0.0, 0.0, 0.0, 1.0]
    ]

    frames.append({
        "file_path": f"keyframes/images/{fname.replace('.json', '.jpg')}",
        "transform_matrix": transform_matrix,
        "fl_x": meta["fx"],
        "fl_y": meta["fy"],
        "cx": meta["cx"],
        "cy": meta["cy"],
        "w": meta["width"],
        "h": meta["height"]
    })

transforms = {
    "camera_model": "OPENCV",
    "frames": frames
}

with open(output_path, "w") as f:
    json.dump(transforms, f, indent=2)
