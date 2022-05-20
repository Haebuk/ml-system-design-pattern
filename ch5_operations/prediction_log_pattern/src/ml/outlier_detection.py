from logging import getLogger
from typing import List, Tuple

import numpy as np
import onnxruntime as rt
from src.configurations import ModelConfigurations

logger = getLogger(__name__)


class OutlierDetector(object):
    def __init__(self, outlier_model_filepath: str, outlier_lower_threshold: float):
        self.outlier_model_filepath = outlier_model_filepath
        self.outlier_lower_threshold = outlier_lower_threshold
        self.outlier_detector = None
        self.outlier_input_name: str = ""
        self.outlier_output_name: str = ""
        self.load_outlier_model()

    def load_outlier_model(self):
        logger.info(f"Loading outlier model: {self.outlier_model_filepath}")
        self.outlier_detector = rt.InferenceSession(self.outlier_model_filepath)
        self.outlier_input_name = self.outlier_detector.get_inputs()[0].name
        self.outlier_output_name = self.outlier_detector.get_outputs()[0].name
        logger.info("initialized outlier model")

    def predict(self, data: List[List[int]]) -> Tuple[bool, float]:
        np_data = np.array(data).astype(np.float32)
        prediction = self.outlier_detector.run(None, {self.outlier_input_name: np_data})
        output = float(prediction[1][0][0])
        is_outlier = output < self.outlier_lower_threshold
        logger.info(f"outlier score {output}")
        return is_outlier, output


outlier_detector = OutlierDetector(
    ModelConfigurations().outlier_model_filepath,
    ModelConfigurations().outlier_lower_threshold,
)
