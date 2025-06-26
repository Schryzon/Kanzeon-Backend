"""
Kanzeon API
"Clarity, among chaos."
Backend by I Nyoman Widiyasa Jayananda (Schryzon)
"""
import torch
import uuid
import time
import asyncio
import logging
import pytesseract
import re as regex # Cursed, I know
from PIL import Image
from contextlib import suppress
from langdetect import detect as detect_language, DetectorFactory
from googletrans import Translator # T5 model knows a few languages
from os import remove as remove_file, path, makedirs
from quart import Quart, request, jsonify
from quart_cors import cors as CORS
from transformers import (
    pipeline, 
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)
from peft import (
    LoraConfig, 
    get_peft_model, 
    TaskType,
    PeftModel,
    PeftConfig
)
from pdfminer.high_level import extract_text as extract_pdf

class Kanzeon(Quart):
    """
    Custom class for Kanzeon.
    Inherits the Quart class.
    Wowza!
    """
    def __init__(self, import_name, **kwargs) -> None:
        """
        Initialize Kanzeon class from the inherited class.
        """
        super().__init__(import_name, **kwargs)
        CORS(self, allow_origin = "*")

        # App attributes
        self.project = "Kanzeon"
        self.version = "K-1"
        self.port = 4706
        self.config["MAX_CONTENT_LENGTH"] = 10*1024*1024 # 10 MB max
        self.gpu_recover_threshold = 4 * 1024**3  # 4 GB VRAM threshold

        # Transformers attributes
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = "t5-large" # Pretrained model name
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        self._init_logging() # Start logging

        # Load base model for seq2seq
        base_model = AutoModelForSeq2SeqLM.from_pretrained(
            self.model_name,
            torch_dtype = torch.float16 if self.device.type == "cuda" else torch.float32
        )
        base_model.to(self.device)

        self.adapter_dir = "./kanzeon_adapter"
        # Load or create LoRA adapter
        if path.isdir(self.adapter_dir):
            # Load saved adapter
            self.logger.info("Loading LoRA adapter from disk...")
            peft_config = PeftConfig.from_pretrained(self.adapter_dir)
            base_model = AutoModelForSeq2SeqLM.from_pretrained(peft_config.base_model_name_or_path)
            base_model.to(self.device)
            self.model = PeftModel.from_pretrained(base_model, self.adapter_dir)
            
        else:
            # Create new adapter
            self.logger.info("Creating new LoRA adapter...")
            lora_config = LoraConfig(
                task_type=TaskType.SEQ_2_SEQ_LM,
                inference_mode=False,
                r=8,
                lora_alpha=16,
                lora_dropout=0.05
            )
            self.model = get_peft_model(base_model, lora_config)

        self.max_input_tokens = 1024
        self.max_output_tokens = 520
        self.min_output_tokens = 30
        self.stride = 200

        # Init the summarizer
        self.summarizer = pipeline(
            "summarization", 
            model=self.model, 
            tokenizer=self.tokenizer, 
            device=0 if self.device.type == "cuda" else -1
        )
        self.translator = Translator()
        self.before_serving(self._on_startup)
        self.after_serving(self._on_shutdown)
        self._init_routes()

    async def _on_startup(self):
        self.logger.info(f"Running {self.project} {self.version} at port: {self.port}.")
        self.monitor_task = asyncio.create_task(self.monitor_gpu_memory())

    async def _on_shutdown(self):
        self.logger.info("Server is shutting down gracefully...")
        self.monitor_task.cancel()
        with suppress(asyncio.CancelledError):
            await self.monitor_task
        self.logger.info("GPU monitor stopped.")

    async def monitor_gpu_memory(self) -> None:
        """
        Monitors GPU memory and returns to GPU when safe.
        """
        while True:
            await asyncio.sleep(10)
            if self.device.type == "cuda":
                current_device = next(self.model.parameters()).device.type
                if current_device == "cpu":
                    try:
                        torch.cuda.empty_cache()
                        mem_free = torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated(0)
                        if mem_free > self.gpu_recover_threshold:
                            self.logger.info("GPU has calmed down. Time to use it again.")
                            self.model.to("cuda")
                            self.summarizer = pipeline(
                                "summarization",
                                model = self.model,
                                tokenizer = self.tokenizer,
                                device = 0
                            )

                    except Exception as error:
                        self.logger.warning(f"GPU monitor failed to switch: {error}")

    def save_adapter(self) -> None:
        """
        Save the LoRA adapter weights.
        """
        makedirs(self.adapter_dir, exist_ok=True)
        self.model.save_pretrained(self.adapter_dir)
        self.logger.info(f"Saved LoRA adapter to {self.adapter_dir}")

    def _init_logging(self) -> None:
        """
        Set logging.info() to display to console.
        """
        logging.basicConfig(level = logging.INFO)
        self.logger = logging.getLogger("kanzeon")
        self.logger.info(f"Project {self.project} version {self.version} initialized on {self.device.type.upper()}.")

    def _init_routes(self) -> None:
        """
        Enables all the routes.
        All async for a good flex, lol.
        """
        @self.route("/kanzeon/status")
        async def status():
            mem_total = "None"
            mem_alloc = "None"
            if self.device.type == "cuda":
                mem_total = torch.cuda.get_device_properties(0).total_memory
                mem_alloc = torch.cuda.memory_allocated(0)
            return jsonify({
                "status": 200,
                "condition": "OK",
                "project": self.project,
                "version": self.version,
                "device": self.device.type.upper(),
                "used_memory": mem_alloc,
                "total_memory": mem_total
            }), 200
        
        @self.route("/kanzeon/about")
        async def about():
            return jsonify({
                "backend": "I Nyoman Widiyasa Jayananda (Schryzon)",
                "frontend": "M. Sagos (gasosart)",
                "tagline": "Clarity, among chaos.",
                "tech": [
                    "Python", 
                    "Torch", 
                    "Transformers", 
                    "LoRA", 
                    "Quart"
                ]
            }), 200
        
        @self.route("/kanzeon/save_adapter", methods=["POST"])
        async def save_adapter_route():
            """
            Endpoint to save adapter weights.
            """
            try:
                self.save_adapter()
                return jsonify({
                    "status": 200, 
                    "message": "Adapter saved."
                }), 200
            
            except Exception as error:
                return jsonify({
                    "status": 500, "error": str(error)
                }), 500
        
        @self.route("/kanzeon/summarize", methods = ["POST"])
        async def api_summarize():
            """
            Retrieve a file or text and return result from the model.
            """
            if "multipart/form-data" in request.content_type:
                file = (await request.files).get("file")
                if not file:
                    return jsonify({
                        "status": 400,
                        "error": "Tidak ada file terdeteksi dalam request."
                    }), 400
                
                try:
                    text = await self.extract_text(file)

                except Exception as error:
                    return jsonify({
                        "status": 500, "error": str(error)
                    }), 500

            elif "application/json" in request.content_type:
                data = await request.get_json(force=True)
                text = data.get("text", "").strip()
                if not text:
                    return jsonify({
                        "status": 400,
                        "error": "Tidak ada teks di dalam field 'text'!"
                    }), 400
                
                if len(text) > 10000:
                    return jsonify({
                        "status": 413,
                        "error": "Teks terlalu panjang, maksimal 10.000 karakter!"
                    }), 413
            
            else:
                return jsonify({
                    "status": 415,
                    "error": "Tipe media tidak disupport. Gunakan 'application/json' atau 'multipart/form-data'."
                }), 415
            
            try:
                DetectorFactory.seed = 0
                lang = detect_language(text)
                self.logger.info(f"Detected language: {lang}")

                # Translate to English if needed
                if lang not in ("en", "unknown"):
                    text = self.translate(text, lang, "en")

                # Summarize in chunks with OOM fallback
                summary, time = await self.summarize(text, lang)
                return jsonify({
                    "status": 200,
                    "summary": summary,
                    "time_taken": f"{time} seconds"
                }), 200
            
            except Exception as error:
                return jsonify({
                    "status": 500,
                    "error": str(error)
                }), 500

    def check_device(self) -> None:
        """
        Check which device PyTorch is using.
        Preferably, use CUDA.
        """
        self.logger.info(f"Utilizing the {self.device.type.upper()}!")
        if self.device.type == "cuda" and self.device.index is not None:
            device_name = torch.cuda.get_device_name(self.device.index)
            self.logger.info(f"Found GPU: {device_name}")
        
    def translate(self, text:str, source:str, dest:str) -> str:
        """
        Back and forth translation.
        T5 model is trained on English, that's why.
        """
        if source == "unknown" or dest == "unknown":
            return text
        try:
            result = self.translator.translate(text, dest, source)
            return result.text
        except Exception as error:
            self.logger.warning(f"Translation failed: {error}")
            return text  # Fallback to original

    def clean_summary(self, summary: str) -> str:
        """
        Clean the generated summary.
        """
        summary = summary.strip()
        if summary:
            summary = summary[0].upper() + summary[1:]
        summary = regex.sub(r"\s+\.", ".", summary)
        summary = regex.sub(r"\s+", " ", summary)
        # Uppercase after a period
        summary = regex.sub(r"(?<=\. )([a-z])", lambda m: m.group(1).upper(), summary)
        return summary

    async def extract_text(self, file) -> str:
        """
        Extract text from PDF or perform OCR
        """
        makedirs("./tmp", exist_ok = True)
        file_path = f"./tmp/{uuid.uuid4()}.{file.filename.split('.')[-1]}"
        await file.save(file_path)

        try:
            if file.filename.endswith(".pdf"):
                return extract_pdf(file_path)
            
            elif file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")): # Expects tuple
                image = Image.open(file_path)
                return pytesseract.image_to_string(image)
            
            else:
                raise TypeError("Tipe file yang diupload tidak disupport.")
            
        finally:
            remove_file(file_path)

    async def summarize(self, text: str, language:str) -> str:
        """
        Summarize text using the modified pretrained model.
        """
        start = time.perf_counter()
        self.check_device()
        if language != "en" and language != "unknown":
            text = self.translate(text, language, "en")
        inputs = self.tokenizer(
            text,
            return_overflowing_tokens = True,
            max_length = self.max_input_tokens,
            stride = self.stride,
            truncation = True
        )
        outputs = []
        for idx in inputs["input_ids"]:
            chunk = self.tokenizer.decode(idx, skip_special_tokens = True)
            summary = None
            while not summary:
                try:
                    summary = await asyncio.to_thread(
                        lambda c: self.summarizer(
                            c,
                            max_length = self.max_output_tokens,
                            min_length = self.min_output_tokens,
                            do_sample = False
                        )[0]["summary_text"], chunk
                    )
                except torch.cuda.OutOfMemoryError:
                    summary = None
                    self.logger.warning("GPU out of VRAM. Switching to CPU!")
                    self.model.to("cpu")
                    self.summarizer = pipeline(
                        "summarization", 
                        model = self.model, 
                        tokenizer = self.tokenizer, 
                        device = -1
                    )
            outputs.append(summary)
        text = " ".join(outputs)
        text = self.clean_summary(text)
        if language != "en" and language != "unknown":
            text = self.translate(text, "en", language)
        end = time.perf_counter()
        elapsed = round(end - start, 2)
        return text, elapsed
    

if __name__ == "__main__":
    # Initialize and rev her up!
    kanzeon = Kanzeon(__name__)
    kanzeon.run(
        port = kanzeon.port,
        debug = True
    )