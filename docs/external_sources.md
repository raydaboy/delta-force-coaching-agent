# External sources used by this repository

The local narration setup follows the official `thewh1teagle/kokoro-onnx` README and example:

- Repository and setup instructions: https://github.com/thewh1teagle/kokoro-onnx
- Official save example: https://raw.githubusercontent.com/thewh1teagle/kokoro-onnx/main/examples/save.py
- Model release page: https://github.com/thewh1teagle/kokoro-onnx/releases
- Current v1.1 release assets used for v1.0 English inference: https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.0.int8.onnx and https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.0.bin
- Voice list and language guidance: https://huggingface.co/hexgrad/Kokoro-82M/raw/main/VOICES.md

Verified setup facts from the official README and release page: install `kokoro-onnx` and `soundfile`; instantiate `Kokoro(model_path, voices_path)`; call `create(text, voice='af_sarah' or another supported English voice, speed=1.0, lang='en-us')`; and write the returned samples with `soundfile`. The v1.1 model-files release provides an int8 English model and a v1.0 voice pack.

These URLs are implementation references only. They are not runtime requirements for the evidence resolver or pure-gameplay editing pipeline. Do not download model files automatically in a production deployment without explicit configuration and license review.
