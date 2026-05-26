import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class Tracker:
    def __init__(self, detector):
        self.result = None
        self.detector = detector

    def handle_result(self, result, _output_image: mp.Image, _timestamp_ms: int):
        self.result = result


class FaceTracker(Tracker):
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path="./face_landmarker.task")
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=self.handle_result,
            # num_faces=2,
        )
        detector = vision.FaceLandmarker.create_from_options(options)
        super().__init__(detector)

    # def handle_result(self, result, _output_image: mp.Image, _timestamp_ms: int):
    #     if self.result is None:
    #         self.result = result
    #
    #     def smooth(a, b):
    #         c = a
    #         c.x += (b.x-a.x)*0.9
    #         c.y += (b.y-a.y)*0.9
    #         return c
    #
    #     # smoothing
    #     self.result.face_landmarks = [
    #         [
    #             smooth(lm_old, lm_new)
    #             for (lm_old, lm_new) in zip(old, new)
    #         ]
    #         for (old, new) in zip(self.result.face_landmarks, result.face_landmarks)
    #     ]


class HandTracker(Tracker):
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path="./hand_landmarker.task")
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=self.handle_result,
            num_hands=2,
        )
        detector = vision.HandLandmarker.create_from_options(options)
        super().__init__(detector)


class PoseTracker(Tracker):
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path="./pose_landmarker.task")
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=self.handle_result,
        )
        detector = vision.PoseLandmarker.create_from_options(options)
        super().__init__(detector)

