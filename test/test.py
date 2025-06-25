import torch
import asyncio
import logging
from transformers import pipeline, AutoTokenizer
from quart import Quart, request, jsonify

#summarizer = Quart(__name__)

class Summarizer():
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = "t5-base"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)
        self.max_input_tokens = 1024
        self.max_output_tokens = 520
        self.min_output_tokens = 30
        self.stride = 200
        self.summarizer = pipeline(
            "summarization", 
            model=self.model, 
            tokenizer=self.model, 
            device=self.device.index
        )
        self.check_device()

    def check_device(self):
        logging.info(f"Utilizing the {self.device}!")
        try:
            device_name = torch.cuda.get_device_name()
            logging.info(f"Found GPU: {device_name}")

        except:
            pass

    # TODO: change to async
    def summarize(self, text: str) -> str:
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
            summary = self.summarizer(
                chunk,
                max_length = self.max_output_tokens,
                min_length = self.min_output_tokens,
                do_sample = False
            )[0]["summary_text"]
            outputs.append(summary)
        return " ".join(outputs)

long_text = """
The time-displaced Young Xehanort successfully gathers other incarnations of himself from across time, until they total twelve, including himself and the elder Master Xehanort, and is provided with a replica body for his heart when he reaches the present.

At the beginning of Sora and Riku's Mark of Mastery exam, the disembodied Ansem appears, in his robed appearance. He causes Sora to be marked with the Recusant's Sigil, allowing him to be tracked and guided through the Sleeping Worlds by Young Xehanort and his comrades.

He appears before Sora and Riku in several worlds, often accompanied by either Ansem or Xemnas. They taunt the two, Sora about his unknown links to others' hearts, Riku about his dark past, and both about being trapped in their dreams. Young Xehanort chooses to make Sora the thirteenth vessel for Master Xehanort's heart, as Riku had developed a resistance to darkness. In the Symphony of Sorcery, Xehanort confronts Sora, commenting on the idyllic and beautiful dream-like landscape. Xehanort reveals he is not part of Sora's dream and ominously tells Sora to keep sleeping and they will meet again.

Eventually, Sora is brought to the real World that Never Was, where Xigbar explains how his journey had been manipulated all along, and Young Xehanort plunges Sora back into a deep sleep, showing him illusions of his own past. Sora then dreams of the many people connected to him, and when he chases the phantoms in his dream, he falls deeper into sleep. Eventually he confronts Xigbar and Xemnas, who reveals to him the true purpose of Organization XIII and admit that Nobodies can regrow their hearts over time. Although Sora defeats Xemnas, the fight weakens him to the point that he cannot escape from his deep sleep. Young Xehanort reappears before him, and he tells Sora how they had manipulated his journey. As Sora falls unconscious, Xehanort informs him that he will become the thirteenth member of the new Organization XIII.
"""

if __name__ == "__main__":
    model = Summarizer()
    result = model.summarize(long_text)
    print("\n\nORIGINAL TEXT:")
    print(long_text)
    print("\n\nSUMMARIZATION:")
    print(result)
    # summarizer.run(port = 4706)