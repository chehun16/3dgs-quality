import json
import numpy as np
import os
from PIL import Image
from scipy.spatial.transform import Rotation as R  
from scipy.spatial.transform import Slerp

input_json_path = "transforms_train0.json"
output_json_path = "transforms_train.json"
num_novel_poses = 40    # 노벨 포즈 몇개할지
image_path_template = "images/novel_{:05d}.png"
image_output_dir = "images"

with open(input_json_path, 'r') as f:
    train_data = json.load(f)

train_frames = train_data["frames"]
camera_angle_x = train_data["camera_angle_x"]
train_poses = np.array([np.array(f["transform_matrix"]) for f in train_frames])  # (N, 4, 4)

# novel frame 생성
novel_frames = []
for i in range(num_novel_poses):
    alpha = i / (num_novel_poses - 1)
    idx_a = int(alpha * (len(train_poses) - 1))
    idx_b = min(idx_a + 1, len(train_poses) - 1)
    t = (alpha * (len(train_poses) - 1)) - idx_a

    pose_a = train_poses[idx_a]
    pose_b = train_poses[idx_b]

    # translation - linear interpolation
    trans_interp = (1 - t) * pose_a[:3, 3] + t * pose_b[:3, 3]

    # rotation - spherical linear interpolation
    rot_a = R.from_matrix(pose_a[:3, :3])
    rot_b = R.from_matrix(pose_b[:3, :3])
    key_times = [0, 1]
    rotations = R.concatenate([rot_a, rot_b])
    slerp = Slerp(key_times, rotations)
    rot_interp = slerp(t).as_matrix()

    # novel pose 만들기 
    novel_pose = np.eye(4)
    novel_pose[:3, :3] = rot_interp
    novel_pose[:3, 3] = trans_interp

    # 가장 가까운 training pose 찾기
    dists = [np.linalg.norm(p[:3, 3] - trans_interp) for p in train_poses]
    closest_idx = int(np.argmin(dists))
    ref_image_path = train_frames[closest_idx]["file_path"]

    file_path = image_path_template.format(i)
    novel_frames.append({
        "file_path": file_path,
        "transform_matrix": novel_pose.tolist(),
        "ref_image": ref_image_path
    })

#############################################################################
# 파일 저장하는 부분들
    
    os.makedirs(image_output_dir, exist_ok=True)
    img_full_path = os.path.join(image_output_dir, f"novel_{i:05d}.png")
    if not os.path.exists(img_full_path):
        Image.new("RGB", (1024, 768), (0, 0, 0)).save(img_full_path)

novel_frames_blender = [
    {
        "file_path": frame["file_path"],
        "transform_matrix": frame["transform_matrix"]
    }
    for frame in novel_frames
]

merged_frames = train_frames + novel_frames_blender
merged_data = {
    "camera_angle_x": camera_angle_x,
    "frames": merged_frames
}

with open(output_json_path, 'w') as f:
    json.dump(merged_data, f, indent=4)

novel_data = {
    "camera_angle_x": camera_angle_x,
    "frames": novel_frames_blender
}
with open("transforms_test.json", "w") as f:
    json.dump(novel_data, f, indent=4)

with open("transforms_novel.json", "w") as f:
    json.dump({
        "camera_angle_x": camera_angle_x,
        "frames": novel_frames
    }, f, indent=4)

print(f"Saved transforms_train.json with {len(merged_frames)} total poses (train + {num_novel_poses} novel)")
print(f"Dummy images saved in: {image_output_dir}")
print("Saved transforms_novel.json (with ref_idx)")
print("Saved transforms_test.json (Blender-style, no ref_idx)")
