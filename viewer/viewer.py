import open3d as o3d
import numpy as np
import json

# point cloud, camera pose loading
pcd = o3d.io.read_point_cloud("point_cloud.ply")

with open("transforms_train.json", "r") as f:
    meta = json.load(f)

# frustum으로 카메라 시각화
def create_camera_frustum(pose, color=[1, 0, 0], scale=0.2):
    frustum = o3d.geometry.LineSet()
    points = np.array([
        [0, 0, 0],       # camera center
        [1, 1, 1.5],
        [1, -1, 1.5],
        [-1, -1, 1.5],
        [-1, 1, 1.5],
    ]) * scale
    points = (pose[:3, :3] @ points.T).T + pose[:3, 3]
    lines = [[0,1],[0,2],[0,3],[0,4],[1,2],[2,3],[3,4],[4,1]]
    frustum.points = o3d.utility.Vector3dVector(points)
    frustum.lines = o3d.utility.Vector2iVector(lines)
    frustum.colors = o3d.utility.Vector3dVector([color] * len(lines))
    return frustum

# 카메라 프레임마다 frustum 생성 
geometries = [pcd]
for frame in meta["frames"]:
    pose = np.array(frame["transform_matrix"])
    filepath = frame["file_path"]
    if "novel_" in filepath:
        color = [1, 0, 0]  
    else:
        color = [0.4, 0.8, 1.0]  
    frustum = create_camera_frustum(pose, color=color)
    geometries.append(frustum)

o3d.visualization.draw_geometries(geometries)
