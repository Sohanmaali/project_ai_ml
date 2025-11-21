from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

CHUNK = 30 * 16000
texts = []

processor = WhisperProcessor.from_pretrained("openai/whisper-base")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")
model.config.forced_decoder_ids =  processor.get_decoder_prompt_ids(language="hindi", task="translate")
  #None
audio_input, sr = librosa.load("english_2.wav", sr=16000)

for i in range(0, len(audio_input), CHUNK):
    
    chunk = audio_input[i:i+CHUNK]

    input_features = processor(chunk, sampling_rate=16000, return_tensors="pt").input_features
    predicted_ids = model.generate(input_features)
    text = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

    texts.append(text)

full_transcription = " ".join(texts)
print("=======================================English Text=======================================")
print(full_transcription)

client = InferenceClient(
    provider="hf-inference",
    api_key=os.environ["HUGGINGFACEHUB_API_TOKEN"],
)

result = client.translation(full_transcription, model="Helsinki-NLP/opus-mt-en-hi")
print("=======================================Text=======================================")
print(result)