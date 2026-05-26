import typing
import pygame as pg

if typing.TYPE_CHECKING:
    from .app import App

left_eye = [
    133, 173, 157, 158,
    159, 160, 161, 246,
     33,   7, 163, 144,
    145, 153, 154, 155
]

right_eye = [
    362, 398, 384, 385,
    386, 387, 388, 466,
    263, 249, 390, 373,
    374, 380, 381, 382
]

left_eyebrow = [46, 53, 52, 65, 55, 107, 66, 105]
right_eyebrow = [285, 295, 282, 283, 276, 334, 296, 336]

vampire_tooth_left = [310, 311, 402]
vampire_tooth_right = [80, 81, 178]

mouth = [
    78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308,
    78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308,
]

upper_lip = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291]
lower_lip = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291]

right_face_base = [
    # 10, 338, 297, 332, 284, 251, 454,
    151, 338, 337, 297, 299, 332, 333, 284, 251,
    288, 397, 365, 379, 378, 400, 377,
    152, 17, 14, 94, 1, 6
]

left_face_base = [
    151, 109, 108, 67, 69, 103, 104, 54, 162,
    58, 172, 136, 150, 149, 176, 148,
    152, 17, 14, 94, 1, 6,
]

def draw_avatar(app: App, landmarks: list, wireframe=False):
    def draw_polygon(color, indices):
        points = [app._to_screen(landmarks[idx]) for idx in indices]
        w = int(5) if wireframe else 0
        pg.draw.polygon(app.screen, color, points, w)

    # https://storage.googleapis.com/mediapipe-assets/documentation/mediapipe_face_landmark_fullsize.png

    draw_polygon("#ffffff", left_face_base)
    draw_polygon("#ec5245", right_face_base)

    draw_polygon("#222222", left_eye)
    draw_polygon("#222222", right_eye)

    # irises
    draw_polygon("white", [474, 475, 476, 477])
    draw_polygon("#ec5245", [469, 470, 471, 472])

    draw_polygon("#222222", left_eyebrow)
    draw_polygon("#222222", right_eyebrow)

    # nose
    draw_polygon("#ec5245", [1, 440, 6])
    draw_polygon("#dddddd", [1, 220, 6])

    draw_polygon("#444444", lower_lip)
    draw_polygon("#444444", upper_lip)
    draw_polygon("#333333", mouth)

    draw_polygon("white", vampire_tooth_left)
    draw_polygon("#ec5245", vampire_tooth_right)


# simple one
# def draw_avatar(app: App, landmarks: list, wireframe=False):
#     def draw_polygon(color, indices):
#         points = [app._to_screen(landmarks[idx]) for idx in indices]
#         w = int(5) if wireframe else 0
#         pg.draw.polygon(app.screen, color, points, w)
#
#     # https://storage.googleapis.com/mediapipe-assets/documentation/mediapipe_face_landmark_fullsize.png
#
#     for p in [
#         left_eye, right_eye,
#         mouth,
#         left_eyebrow, right_eyebrow
#     ]:
#         draw_polygon("white", p)

