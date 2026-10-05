# 运行命令

- 项目：faster-whisper（SYSTRAN / CTranslate2 Whisper 推理库）
- 生成时间：2026-09-08
- 运行方式：直接运行（`uv` 可编辑安装 + `start.ps1` 示例转写）
- 硬件评估：**满足**（用户选方案 1：腾显存后跑 large-v3 fp16；启动前空闲约 9.7GB）

## 硬件评估依据

| 项 | 项目/官方 | 本机 |
| --- | --- | --- |
| GPU | 官方 GPU 基准在 RTX 3070 Ti **8GB** 上跑 large-v2 | RTX 4080 **16GB** |
| large-v3 显存 | fp16 ≈ **4.5GB** | 启动前空闲 ≈ **9.7GB**（此前曾紧张，已回升） |
| 内存 | 无硬门槛 | 总 ≈ 31.8GB |

用户确认方案：**1 = 腾显存后 large-v3 + float16**（与 README 一致）。

## 环境准备

```powershell
# PyPI 官方可达则直连；慢时可用：
# $env:UV_INDEX_URL = 'https://pypi.tuna.tsinghua.edu.cn/simple'

uv venv --python 3.10
uv pip install -e .
# Windows GPU：ctranslate2 需要 CUDA12 cuBLAS + cuDNN9 DLL
uv pip install nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*"

# Hugging Face 官方超时 → 镜像（start.ps1 默认已设）
$env:HF_ENDPOINT = 'https://hf-mirror.com'
```

样例音频：`tests/data/jfk.flac`（已从 openai/whisper 测试资源拉取）。

## 启动

- 推荐：`pwsh -NoProfile -File .\start.ps1`
- 说明：单服务 `demo`（CLI 转写验证），无参直接启动（跳过菜单）。无 HTTP 端口。
- 可选参数：`-Audio <路径>` `-Model large-v3`
- 等价手动命令：

```powershell
$env:HF_ENDPOINT = 'https://hf-mirror.com'
$env:Path = "E:\AI\local-voice\faster-whisper\.venv\Lib\site-packages\nvidia\cublas\bin;E:\AI\local-voice\faster-whisper\.venv\Lib\site-packages\nvidia\cudnn\bin;E:\AI\local-voice\faster-whisper\.venv\Lib\site-packages\nvidia\cuda_nvrtc\bin;$env:Path"
.\.venv\Scripts\python.exe .\scripts\demo_transcribe.py --model large-v3 --audio .\tests\data\jfk.flac --device cuda --compute-type float16
```

## 验证

- 加载 `large-v3` 无 CUDA OOM
- 对 `jfk.flac` 输出语言（期望 `en`）及若干时间戳文本段
- 进程退出码 0

## 备注

- 分支：`local-custom`
- 本项目是**库**不是 HTTP 服务；`start.ps1` 的 `-Port` 仅兼容模板，实际跑 CLI 演示
- 镜像：HF 用 `https://hf-mirror.com`（官方 huggingface.co 探测超时）；并设 `HF_HUB_DISABLE_XET=1` 避免 Xet CAS 401
- PyPI 官方可达
- Windows 上通过 venv 内 `nvidia-cublas-cu12` / `nvidia-cudnn-cu12` 提供 DLL（`start.ps1` 自动加 PATH）
- ffmpeg：`E:\Programs\ffmpeg-master-latest-win64-gpl\bin`（PyAV 已捆绑解码，非硬依赖）
- 本文件与 `start.ps1` 为本机运行材料，默认不提交
