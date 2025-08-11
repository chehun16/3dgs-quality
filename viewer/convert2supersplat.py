import numpy as np
from plyfile import PlyData, PlyElement

input_path = "point_cloud.ply"
output_path = "dist/scene.compressed.ply"

plydata = PlyData.read(input_path)
vertex_data = plydata['vertex'].data
num_points = len(vertex_data)

# 필드 이름 목록 추출
existing_fields = vertex_data.dtype.names

# 추가할 필드 정의
color_fields = ['red', 'green', 'blue', 'opacity']
color_types = [
    ('red', 'u1'),
    ('green', 'u1'),
    ('blue', 'u1'),
    ('opacity', 'u1')  
]

# 중복 방지를 위해 새로운 dtype 만들기
new_dtype = vertex_data.dtype.descr.copy()
for name, typ in color_types:
    if name not in existing_fields:
        new_dtype.append((name, typ))

# 새로운 vertex 데이터 생성
new_vertex_data = np.empty(num_points, dtype=new_dtype)

# 기존 데이터 복사
for name in vertex_data.dtype.names:
    new_vertex_data[name] = vertex_data[name]

# 색상 및 투명도 기본값 설정 (없는 경우에만)
if 'red' not in existing_fields:
    new_vertex_data['red'] = 128
if 'green' not in existing_fields:
    new_vertex_data['green'] = 128
if 'blue' not in existing_fields:
    new_vertex_data['blue'] = 128
if 'opacity' not in existing_fields:
    new_vertex_data['opacity'] = np.full(num_points, 255, dtype=np.uint8)

# 저장
vertex_element = PlyElement.describe(new_vertex_data, 'vertex')
PlyData([vertex_element], text=False).write(output_path)

print(f"✅ 변환 완료! 저장 위치: {output_path}")
