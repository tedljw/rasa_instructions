from rasa.nlu.components import Component
from typing import Any, Dict, Optional, Text
class PreprocessAnalyzer(Component):
    """A pre-trained sentiment component"""
    name = "my_preproces"
    provides = []
    requires = []
    defaults = {}
    language_list = ["en"]

    def __init__(self, component_config=None):
        super(PreprocessAnalyzer, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        """Not needed, because the the model is pretrained"""
        pass

    def process(self, message, **kwargs):
        """Retrieve the text message, pass it to the classifier
            and append the prediction results to the message class."""
        print(message.text)
        mymeg = {"name": "action_hello_world",
                  "confidence": 1.0,
                  "message": message.text,
                  "extractor": "sentiment_extractor"}

        message.set("intent", [mymeg], add_to_output=True)

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Pass because a pre-trained model is already persisted"""
        pass
