from pathlib import Path
import urllib.request
import tarfile
import os
import numpy as np
import sherpa_onnx
import sentencepiece as spm

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "runtime" / "kws_model"
MODEL_URL = "https://github.com/k2-fsa/sherpa-onnx/releases/download/kws-models/sherpa-onnx-kws-zipformer-gigaspeech-3.3M-2024-01-01.tar.bz2"

DEFAULT_KEYWORDS = ["WAIT", "STOP", "VEDAS", "HOLD ON", "PAUSE", "LISTEN", "CANCEL"]


class KeywordSpotterDetector:
    def __init__(self, keywords=None, model_dir=None):
        self.model_dir = Path(model_dir or MODEL_DIR)
        self.keywords = keywords or DEFAULT_KEYWORDS
        self._ensure_model_exists()
        self._ensure_keywords_file()

        # Initialize Sherpa-ONNX KeywordSpotter
        self.kws = sherpa_onnx.KeywordSpotter(
            tokens=str(self.model_dir / "tokens.txt"),
            encoder=str(self.model_dir / "encoder-epoch-12-avg-2-chunk-16-left-64.int8.onnx"),
            decoder=str(self.model_dir / "decoder-epoch-12-avg-2-chunk-16-left-64.int8.onnx"),
            joiner=str(self.model_dir / "joiner-epoch-12-avg-2-chunk-16-left-64.int8.onnx"),
            keywords_file=str(self.model_dir / "my_keywords.txt"),
            num_threads=2,
            provider="cpu",
            keywords_score=1.0,
            keywords_threshold=0.20
        )
        self.stream = self.kws.create_stream()

    def _ensure_model_exists(self):
        if not (self.model_dir / "tokens.txt").exists():
            self.model_dir.parent.mkdir(parents=True, exist_ok=True)
            tar_path = self.model_dir.parent / "kws_model.tar.bz2"
            print(f"[KWS] Downloading offline keyword spotting model to {tar_path}...")
            urllib.request.urlretrieve(MODEL_URL, str(tar_path))
            print("[KWS] Extracting model...")
            with tarfile.open(str(tar_path), "r:bz2") as tar:
                tar.extractall(str(self.model_dir.parent))
            extracted_name = [d for d in os.listdir(self.model_dir.parent) if "sherpa-onnx-kws" in d][0]
            os.rename(self.model_dir.parent / extracted_name, self.model_dir)
            if tar_path.exists():
                os.remove(str(tar_path))
            print("[KWS] Offline keyword model ready.")

    def _ensure_keywords_file(self):
        kw_file = self.model_dir / "my_keywords.txt"
        sp = spm.SentencePieceProcessor()
        sp.load(str(self.model_dir / "bpe.model"))
        tokenized_lines = []
        for kw in self.keywords:
            pieces = sp.encode_as_pieces(kw.upper())
            tokenized_lines.append(" ".join(pieces))
        content = "\n".join(tokenized_lines) + "\n"
        if not kw_file.exists() or kw_file.read_text(encoding="utf-8") != content:
            with open(str(kw_file), "w", encoding="utf-8") as f:
                f.write(content)

    def reset(self):
        """Reset the streaming state."""
        self.stream = self.kws.create_stream()

    def detect(self, audio_chunk: bytes | np.ndarray) -> str | None:
        """
        Feed an audio chunk (16kHz PCM int16 or float32) and return detected keyword if any.
        """
        if isinstance(audio_chunk, (bytes, bytearray)):
            chunk_np = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32) / 32768.0
        else:
            chunk_np = audio_chunk.astype(np.float32)

        self.stream.accept_waveform(16000, chunk_np)

        while self.kws.is_ready(self.stream):
            self.kws.decode_stream(self.stream)
            res = self.kws.get_result(self.stream)
            if res:
                self.kws.reset_stream(self.stream)
                return res.strip()

        return None
