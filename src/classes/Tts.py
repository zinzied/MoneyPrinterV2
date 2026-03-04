import os
import soundfile as sf
from gtts import gTTS
from moviepy.editor import AudioFileClip

try:
    from kittentts import KittenTTS as KittenModel
except Exception:
    KittenModel = None

from config import ROOT_DIR, get_tts_voice, get_twitter_language

KITTEN_MODEL = "KittenML/kitten-tts-mini-0.8"
KITTEN_SAMPLE_RATE = 24000
GTTTS_LANGUAGE_MAP = {
    "english": "en",
    "french": "fr",
    "german": "de",
    "spanish": "es",
    "italian": "it",
    "portuguese": "pt",
    "hindi": "hi",
}


def _resolve_gtts_lang() -> str:
    configured = str(get_twitter_language() or "").strip().lower()
    return GTTTS_LANGUAGE_MAP.get(configured, "en")

class TTS:
    def __init__(self) -> None:
        self._model = KittenModel(KITTEN_MODEL) if KittenModel is not None else None
        self._voice = get_tts_voice()
        self._lang = _resolve_gtts_lang()

    def synthesize(self, text, output_file=os.path.join(ROOT_DIR, ".mp", "audio.wav")):
        if self._model is not None:
            audio = self._model.generate(text, voice=self._voice)
            sf.write(output_file, audio, KITTEN_SAMPLE_RATE)
            return output_file

        # Python 3.13+ fallback when kittentts dependency stack is unavailable.
        temp_mp3 = output_file + ".tmp.mp3"
        gTTS(text=text, lang=self._lang).save(temp_mp3)
        with AudioFileClip(temp_mp3) as clip:
            clip.write_audiofile(output_file, fps=KITTEN_SAMPLE_RATE, verbose=False, logger=None)
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)
        return output_file
