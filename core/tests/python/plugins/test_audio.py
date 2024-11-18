import os
import pytest
from unittest.mock import patch, MagicMock
from audio import say, translate_to_english, detect_language_from_command, lang_detector

# Test for lang_detector function
@patch('audio.fasttext.load_model')
def test_lang_detector(mock_load_model):
    mock_model = MagicMock()
    mock_model.predict.return_value = ['__label__en']
    mock_load_model.return_value = mock_model

    result = lang_detector("Hello")
    assert result == "en"  # Expecting English language code

# Test for detect_language_from_command function
def test_detect_language_from_command():
    command = "Please speak in Spanish"
    result = detect_language_from_command(command)
    assert result == "es"  # Expecting Spanish language code

    command = "Hello"
    result = detect_language_from_command(command)
    assert result is None  # No language detected

# Test for translate_to_english function
@patch('audio.translator')
@pytest.mark.asyncio
async def test_translate_to_english(mock_translator):
    mock_translator.return_value = "Hello"

    result = await translate_to_english("Hola", "es")
    assert result == "hello"  # Expecting translated text in lower case

    result = await translate_to_english("Hello", "en")
    assert result == "Hello"  # Expecting the same text back

# Test for say function
@patch('audio.gTTS')
@patch('audio.os.system')
@pytest.mark.asyncio
async def test_say(mock_os_system, mock_gTTS):
    mock_gTTS.return_value.save = MagicMock()

    await say("Hello", "en")

    # Check if gTTS was called with the correct parameters
    mock_gTTS.assert_called_once_with(text="Hello", lang="en", slow=False)

    # Check if the audio file was saved
    mock_gTTS.return_value.save.assert_called_once_with("response.mp3")

    # Check if the audio file was played
    mock_os_system.assert_called_once_with("mpg123 response.mp3")

    # Check if the audio file was removed after playing
    assert not os.path.exists("response.mp3")

# Run the tests
if __name__ == "__main__":
    pytest.main()