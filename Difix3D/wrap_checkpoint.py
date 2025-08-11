import torch
from torch.cuda.amp import GradScaler

# 기존 학습된 Diffusers 모델
model = torch.load("output/cglab3_2/checkpoints/model_2001.pkl")

scaler = GradScaler()
scaler_state = scaler.state_dict()

# 포장
checkpoint = {
    "step": 2001,
    "model": model,
    "pipeline": {},
    "optimizers": {},
    "scalers": scaler_state 
}

# 저장
torch.save(checkpoint, "output/cglab3_2/checkpoints/model_difix3d.pt")
print("✅ Difix3D용 체크포인트 변환 완료!")
