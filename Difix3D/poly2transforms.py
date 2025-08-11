import os
import json
import math

# 설정
image_dir = "keyframes/input"
camera_dir = "keyframes/cameras"
output_path = "keyframes/transforms_train.json"  # output도 keyframes 안에 저장

def load_camera_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def build_transform_matrix(cam):
    return [
        [cam["t_00"], cam["t_01"], cam["t_02"], cam["t_03"]],
        [cam["t_10"], cam["t_11"], cam["t_12"], cam["t_13"]],
        [cam["t_20"], cam["t_21"], cam["t_22"], cam["t_23"]],
        [0.0,        0.0,        0.0,        1.0]
    ]

def compute_camera_angle_x(cam):
    fx = cam["fx"]
    width = cam["width"]
    return 2 * math.atan(0.5 * width / fx)

frames = []
camera_angle_x = None

for fname in sorted(os.listdir(camera_dir)):
    if not fname.endswith(".json"):
        continue

    stem = fname.replace(".json", "")
    cam_path = os.path.join(camera_dir, fname)
    img_path = os.path.join(image_dir, stem + ".jpg")

    if not os.path.exists(img_path):
        print(f"❗ 이미지 없음: {img_path}")
        continue

    cam_data = load_camera_json(cam_path)
    transform_matrix = build_transform_matrix(cam_data)

    if camera_angle_x is None:
        camera_angle_x = compute_camera_angle_x(cam_data)

    # ✅ 여기서 keyframes/ 제거된 상대 경로로 저장
    frames.append({
        "file_path": f"images/{stem}.jpg",
        "transform_matrix": transform_matrix
    })

output = {
    "camera_angle_x": camera_angle_x,
    "frames": frames
}

with open(output_path, "w") as f:
    json.dump(output, f, indent=4)

print(f"✅ transforms.json 생성 완료! 총 {len(frames)}개 프레임.")
