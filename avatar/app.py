import importlib
import cv2
import mediapipe as mp
import pygame as pg
from . import avatar
from .tracker import HandTracker, FaceTracker, PoseTracker


class App:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode(flags=pg.RESIZABLE)
        pg.mouse.set_visible(False)

        self.face_tracker = FaceTracker()
        self.hand_tracker = HandTracker()
        self.pose_tracker = PoseTracker()

        self.capture_device = cv2.VideoCapture(0)
        self.running = True

        self.result = None
        self.toggles = {
            "landmarks": False,
            "avatar": True,
            "wireframe": False,
        }
        self.frame = None


    def run(self):
        while self.running:
            for ev in pg.event.get():
                self._handle_event(ev)

            self._detect()
            self._render()

        self.capture_device.release()
        cv2.destroyAllWindows()


    def _toggle(self, name: str):
        self.toggles[name] = not self.toggles[name]


    def _render(self):
        self.screen.fill(0x181818)
        if self.face_tracker.result is not None:
            for face_landmarks in self.face_tracker.result.face_landmarks:
                self._draw_face(face_landmarks)

        if self.hand_tracker.result is not None:
            for hand_landmarks in self.hand_tracker.result.hand_landmarks:
                self._draw_hand(hand_landmarks)

        if self.pose_tracker.result is not None:
            for pose_landmarks in self.pose_tracker.result.pose_landmarks:
                self._draw_pose(pose_landmarks)

        pg.display.update()


    def _detect(self):
        success, frame = self.capture_device.read()

        if not success:
            return

        frame = cv2.flip(frame, 1)
        self.frame = frame
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
        mp_image = mp.Image(mp.ImageFormat.SRGB, rgb_frame)

        self.face_tracker.detector.detect_async(mp_image, timestamp_ms)
        self.hand_tracker.detector.detect_async(mp_image, timestamp_ms)
        self.pose_tracker.detector.detect_async(mp_image, timestamp_ms)


    def _handle_event(self, ev):
        if ev.type == pg.QUIT:
            self.running = False
        elif ev.type == pg.KEYDOWN:
            if ev.key in (pg.K_q, pg.K_ESCAPE):
                self.running = False
            elif ev.key == pg.K_j:
                self._toggle("landmarks")
            elif ev.key == pg.K_k:
                self._toggle("avatar")
            elif ev.key == pg.K_l:
                self._toggle("wireframe")


    def _to_screen(self, p):
        assert self.frame is not None
        w, h = self.screen.size
        fw, fh, _ = self.frame.shape
        return (
            p.x * fh / fw * h + (w-h)/2,
            p.y * h
        )


    def _draw_face(self, landmarks: list):
        if not landmarks:
            return

        if self.toggles["avatar"]:
            self._draw_avatar(landmarks)

        if self.toggles["landmarks"]:
            for lm in landmarks:
                x, y = self._to_screen(lm)
                pg.draw.circle(self.screen, "green", (x, y), 2)


    def _draw_avatar(self, landmarks: list):
        # TODO: display errors on-screen

        try:
            importlib.reload(avatar)
        except Exception as e:
            print("can't reload avatar -", e)

        try:
            avatar.draw_avatar(self, landmarks, wireframe=self.toggles["wireframe"])
        except Exception as e:
            print("can't draw avatar -", e)


    def _draw_hand(self, landmarks: list):
        # https://ai.google.dev/static/edge/mediapipe/images/solutions/hand-landmarks.png

        lines = [
            (
                0 if lm_idx == 0 else (4*finger_idx + lm_idx),
                4*finger_idx + lm_idx + 1
            )
            for finger_idx in range(5)
            for lm_idx in range(4)
        ] + [
            (1, 5),
            # (2, 5),
            (5, 9),
            (9, 13),
            (13, 17)
        ]

        for (idx_a, idx_b) in lines:
            a = self._to_screen(landmarks[idx_a])
            b = self._to_screen(landmarks[idx_b])
            pg.draw.aaline(self.screen, "white", a, b, 2)

        for landmark in landmarks:
            point = self._to_screen(landmark)
            pg.draw.circle(self.screen, "green", point, 5)


    def _draw_pose(self, landmarks: list):

        lines = [
            (11, 12),
            (11, 23),
            (12, 24),
            (23, 24),

            # left arm
            (12, 14),
            (14, 16),
            (16, 20),
            (16, 18),
            (16, 22),
            (18, 20),

            # right arm
            (11, 13),
            (13, 15),

            # left leg
            (24, 26),
            (26, 28),

            # right leg
            (23, 25),
            (25, 27),
        ]

        for (idx_a, idx_b) in lines:
            a = self._to_screen(landmarks[idx_a])
            b = self._to_screen(landmarks[idx_b])
            pg.draw.aaline(self.screen, "white", a, b, 2)


