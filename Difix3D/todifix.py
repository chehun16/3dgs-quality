import json, os
from pathlib import Path

# ====== 사용자 설정 ======
TRANSFORMS_JSON = "transforms_novel.json"   # 읽을 transforms 파일
ROOT_DIR = "."                             # file_path가 상대경로일 때 기준 경로
TARGET_DIR = None
# 예) TARGET_DIR = "3dgs/output/0718/test/ours_30000/renders"
# None이면 image와 target_image를 동일하게 둠
PROMPT = "remove degradation"
OUT_JSON = "difix3d_train.json"            # 저장 파일명
# ========================

def to_abs(path_str):
    p = Path(ROOT_DIR) / path_str
    return str(p.resolve())

def remap_to_target(img_path):
    """TARGET_DIR가 지정되면 file_name만 유지하고 TARGET_DIR로 경로 교체"""
    if TARGET_DIR is None:
        return img_path
    fname = os.path.basename(img_path)
    return str(Path(TARGET_DIR).resolve() / fname)

def main():
    with open(TRANSFORMS_JSON, "r") as f:
        data = json.load(f)

    frames = data.get("frames", [])
    if not frames:
        raise ValueError(f"{TRANSFORMS_JSON} 안에 frames가 비어있습니다.")

    train = {}
    for i, fr in enumerate(frames):
        img = to_abs(fr["file_path"])
        tgt = remap_to_target(img)

        # ✅ ref_image 필드가 있으면 그 경로 사용, 없으면 자기 자신
        ref_path = fr.get("ref_image", None)
        if ref_path:
            ref = to_abs(ref_path)
        else:
            ref = img

        item_id = f"train_{i:05d}"
        train[item_id] = {
            "image": img,
            "target_image": tgt,
            "ref_image": ref,
            "prompt": PROMPT,
        }

    out = {
        "train": train,
        "test": {}  # 학습만 할 거면 빈 객체로 둡니다.
    }

    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {OUT_JSON} with {len(train)} train items")
    if TARGET_DIR:
        print(f"  • target_image는 '{TARGET_DIR}'의 파일명으로 매핑했습니다.")
    else:
        print("  • target_image는 image와 동일 경로입니다.")

if __name__ == "__main__":
    main()
