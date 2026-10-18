from pathlib import Path
import urllib.request
import numpy as np
import onnxruntime as ort

MODEL_PATH = Path(__file__).resolve().parent.parent / "runtime" / "silero_vad.onnx"
MODEL_URL = "https://github.com/snakers4/silero-vad/raw/master/src/silero_vad/data/silero_vad.onnx"


class VadDetector:
    def __init__(self, model_path=None, threshold=0.5, sampling_rate=16000):
        self.model_path = Path(model_path or MODEL_PATH)
        self.threshold = threshold
        self.sampling_rate = sampling_rate
        self._ensure_model_exists()

        # Initialize ONNX Runtime session with minimal thread overhead
        opts = ort.SessionOptions()
        opts.inter_op_num_threads = 1
        opts.intra_op_num_threads = 1
        self.session = ort.InferenceSession(str(self.model_path), opts)

        self.state = np.zeros((2, 1, 128), dtype=np.float32)
        self.context = np.zeros((1, 64), dtype=np.float32)
        self.sr = np.array(self.sampling_rate, dtype=np.int64)

    def _ensure_model_exists(self):
        if not self.model_path.exists():
            self.model_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"[VAD] Downloading Silero VAD model to {self.model_path}...")
            urllib.request.urlretrieve(MODEL_URL, str(self.model_path))
            print("[VAD] Model downloaded successfully.")

    def reset(self):
        """Reset recurrent hidden state and context between utterances."""
        self.state = np.zeros((2, 1, 128), dtype=np.float32)
        self.context = np.zeros((1, 64), dtype=np.float32)

    def is_speech(self, audio_chunk: bytes | np.ndarray) -> bool:
        """
        Check if an audio chunk contains human speech.
        Expects 512 samples at 16000 Hz (~32ms).
        audio_chunk can be raw int16 PCM bytes or a float32 numpy array.
        """
        prob = self.get_speech_probability(audio_chunk)
        return prob >= self.threshold

    def get_speech_probability(self, audio_chunk: bytes | np.ndarray) -> float:
        """Calculate speech probability (0.0 to 1.0) for a 512-sample chunk."""
        if isinstance(audio_chunk, (bytes, bytearray)):
            audio_data = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32) / 32768.0
        else:
            audio_data = audio_chunk.astype(np.float32)

        if audio_data.ndim == 1:
            audio_data = np.expand_dims(audio_data, axis=0)

        # Silero VAD v5 requires 512 audio samples per frame at 16kHz
        if audio_data.shape[1] != 512:
            if audio_data.shape[1] > 512:
                audio_data = audio_data[:, :512]
            else:
                audio_data = np.pad(audio_data, ((0, 0), (0, 512 - audio_data.shape[1])))

        # Prepend 64 context samples from previous frame (total 576 samples required by model)
        x = np.concatenate([self.context, audio_data], axis=1)

        try:
            out, self.state = self.session.run(
                None,
                {"input": x, "state": self.state, "sr": self.sr}
            )
            # Update context buffer with the trailing 64 samples
            self.context = x[:, -64:]
            return float(out[0][0])
        except Exception as e:
            print(f"[VAD Error] {e}")
            return 0.0
