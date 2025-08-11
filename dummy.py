import shutil
import os

render_dir = "output/cg/test_novel/ours_30000/renders"
dummy_dir = "data/cg_1/keyframes/images"
num_novel_poses = 40

for i in range(num_novel_poses):
    src = os.path.join(render_dir, f"{i:05d}.png")
    dst = os.path.join(dummy_dir, f"novel_{i:05d}.png")
    
    if os.path.exists(src):
        shutil.copyfile(src, dst)
    else:
        print(f"⚠️ Missing render: {src}")

print("✅ Dummy 이미지들이 렌더링된 결과로 성공적으로 덮어씌워졌습니다.")
