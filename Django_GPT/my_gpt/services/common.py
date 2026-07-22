import torch


def get_pipeline_device():
    """
    현재 환경(CUDA, MPS, CPU)에 맞는 최적의 PyTorch 디바이스를 반환하는 함수
    """
    if torch.cuda.is_available():
        return torch.device("cuda:0")

    # M1/M2/M3 등 Mac Apple Silicon GPU 지원 체크
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")

    return torch.device("cpu")