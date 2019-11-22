import json
import logging
import os
from typing import Any, List, Text

from rasa.core.actions.action import ACTION_LISTEN_NAME

import rasa.utils.io

from rasa.core import utils
from rasa.core.domain import Domain
from rasa.core.policies.policy import Policy
from rasa.core.trackers import DialogueStateTracker

logger = logging.getLogger(__name__)


class FqaPolicy(Policy):
    """Policy which predicts fallback actions.

    A fallback can be triggered by a low confidence score on a
    NLU prediction or by a low confidence score on an action
    prediction. """

    @staticmethod
    def _standard_featurizer():
        return None

    def __init__(
        self,
        priority: int = 4,
        nlu_threshold: float = 0.3,
        core_threshold: float = 0.3,
        fallback_action_name: Text = "fqa",
    ) -> None:
        """Create a new Fallback policy.

        Args:
            core_threshold: if NLU confidence threshold is met,
                predict fallback action with confidence `core_threshold`.
                If this is the highest confidence in the ensemble,
                the fallback action will be executed.
            nlu_threshold: minimum threshold for NLU confidence.
                If intent prediction confidence is lower than this,
                predict fallback action with confidence 1.0.
            fallback_action_name: name of the action to execute as a fallback
        """
        super(FqaPolicy, self).__init__(priority=priority)

        self.nlu_threshold = nlu_threshold
        self.core_threshold = core_threshold
        self.fallback_action_name = fallback_action_name

    def train(
        self,
        training_trackers: List[DialogueStateTracker],
        domain: Domain,
        **kwargs: Any
    ) -> None:
        """Does nothing. This policy is deterministic."""

        pass

    def predict_action_probabilities(
        self, tracker: DialogueStateTracker, domain: Domain
    ) -> List[float]:
        """Predicts a fallback action.

        The fallback action is predicted if the NLU confidence is low
        or no other policy has a high-confidence prediction.
        """

        print("in faq policy")
        nlu_data = tracker.latest_message.parse_data
        print("meg need to deal {}".format(nlu_data))
        print("Last tracker state {}".format(tracker.latest_action_name))
        action_name =  tracker.latest_message.intent[0].get("name")
        print("Action name is {}".format(action_name))
        idx = domain.index_for_action(tracker.latest_message.intent[0].get("name"))
        print("indx is {}".format(idx))
        result = [0.0] * domain.num_actions
        result[idx] = 1.0
        print("Result is {}".format(result))

        if tracker.latest_action_name == action_name:
        # predict action_listen after form action
            idx = domain.index_for_action(ACTION_LISTEN_NAME)
            result[idx] = 1.0


        return result

    def persist(self, path: Text) -> None:
        """Only persists the priority."""

        config_file = os.path.join(path, "faq_policy.json")
        meta = {"priority": self.priority}
        rasa.utils.io.create_directory_for_file(config_file)
        utils.dump_obj_as_json_to_file(config_file, meta)

    @classmethod
    def load(cls, path: Text) -> "FqaPolicy":
        """Returns the class with the configured priority."""

        meta = {}
        if os.path.exists(path):
            meta_path = os.path.join(path, "faq_policy.json")
            if os.path.isfile(meta_path):
                meta = json.loads(rasa.utils.io.read_file(meta_path))

        return cls(**meta)
