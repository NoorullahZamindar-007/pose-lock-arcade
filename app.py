# Threat Detection prototype by Noorullah Zamindar.

import argparse
import math


SAFETY_DISCLAIMER = (
    "Safety notice: this is a prototype only. Do not use it for real security "
    "or threat decisions."
)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Run the threat detection webcam prototype.")
    parser.add_argument("--camera", type=int, default=0, help="Webcam index to use.")
    parser.add_argument(
        "--shoulder-threshold",
        type=float,
        default=-12,
        help="Threat trigger when left shoulder angle is below this value.",
    )
    parser.add_argument(
        "--arm-threshold",
        type=float,
        default=30,
        help="Threat trigger when left arm angle is below this value.",
    )
    parser.add_argument(
        "--game-damage",
        type=int,
        default=25,
        help="Virtual damage per FIRE click in game overlay mode.",
    )
    return parser.parse_args(argv)


def is_threat(left_shoulder_angle, left_arm_angle, shoulder_threshold, arm_threshold):
    return left_shoulder_angle < shoulder_threshold and left_arm_angle < arm_threshold


def apply_fire(health, locked, damage):
    if not locked:
        return health
    return max(0, health - damage)


def findangle(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return math.degrees(
        math.atan2((y2 - y3), (x2 - x3)) - math.atan2((y2 - y1), (x2 - x1))
    )


def main(argv=None):
    import cv2
    import mediapipe as mp

    args = parse_args(argv)
    print(SAFETY_DISCLAIMER)

    mpface = mp.solutions.face_mesh
    mppose = mp.solutions.pose

    face = mpface.FaceMesh()
    pose = mppose.Pose()
    cap = cv2.VideoCapture(args.camera)
    left_arm_angle = 0
    left_shoulder_angle = 0
    game = {"locked": False, "health": 100, "button": (20, 410, 180, 470)}

    def on_mouse(event, x, y, flags, param):
        x1, y1, x2, y2 = game["button"]
        if event == cv2.EVENT_LBUTTONDOWN and x1 <= x <= x2 and y1 <= y <= y2:
            game["health"] = apply_fire(game["health"], game["locked"], args.game_damage)

    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", on_mouse)

    try:
        while True:
            ok, frame = cap.read()
            if not ok or frame is None:
                print("Could not read from webcam. Exiting.")
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result1 = face.process(rgb)
            result = pose.process(rgb)
            locked = False

            if result.pose_landmarks:
                left_shoulder = (
                    result.pose_landmarks.landmark[11].x,
                    result.pose_landmarks.landmark[11].y,
                )
                left_elbow = (
                    result.pose_landmarks.landmark[13].x,
                    result.pose_landmarks.landmark[13].y,
                )
                left_wrist = (
                    result.pose_landmarks.landmark[15].x,
                    result.pose_landmarks.landmark[15].y,
                )
                left_hip = (
                    result.pose_landmarks.landmark[23].x,
                    result.pose_landmarks.landmark[23].y,
                )

                left_arm_angle = findangle(left_shoulder, left_elbow, left_wrist)
                left_shoulder_angle = findangle(left_hip, left_shoulder, left_elbow)
            else:
                left_arm_angle = 0
                left_shoulder_angle = 0

            if result1.multi_face_landmarks:
                for landmarks in result1.multi_face_landmarks:
                    for id, pos in enumerate(landmarks.landmark):
                        if id == 151:
                            locked = is_threat(
                                left_shoulder_angle,
                                left_arm_angle,
                                args.shoulder_threshold,
                                args.arm_threshold,
                            )
                            if locked:
                                cv2.putText(
                                    frame,
                                    "TARGET LOCKED",
                                    (50, 50),
                                    cv2.FONT_HERSHEY_DUPLEX,
                                    1.5,
                                    (0, 0, 255),
                                    2,
                                )
                                ih, iw, ic = frame.shape
                                cx = int(iw * pos.x)
                                cy = int(ih * pos.y)
                                cv2.circle(frame, (cx, cy), 10, (0, 0, 255), 2)
                                cv2.line(frame, (cx, cy - 5000), (cx, cy), (255, 0, 0), 2)
                                cv2.line(frame, (cx - 5000, cy), (cx, cy), (255, 0, 0), 2)
                                cv2.line(frame, (cx + 5000, cy), (cx, cy), (255, 0, 0), 2)
                                cv2.line(frame, (cx, cy + 5000), (cx, cy), (255, 0, 0), 2)
                                cv2.circle(frame, (cx, cy), 2, (0, 0, 255), 2)
                            else:
                                cv2.putText(
                                    frame,
                                    "NO LOCK",
                                    (50, 50),
                                    cv2.FONT_HERSHEY_DUPLEX,
                                    1.5,
                                    (0, 255, 0),
                                    2,
                                )

            game["locked"] = locked and game["health"] > 0
            if not game["locked"] and not locked:
                game["health"] = 100

            ih, iw, ic = frame.shape
            game["button"] = (20, max(90, ih - 70), 180, max(150, ih - 10))
            x1, y1, x2, y2 = game["button"]
            button_color = (0, 0, 255) if game["locked"] else (80, 80, 80)
            cv2.rectangle(frame, (x1, y1), (x2, y2), button_color, -1)
            cv2.putText(
                frame,
                "FIRE" if game["locked"] else "LOCK FIRST",
                (x1 + 20, y1 + 38),
                cv2.FONT_HERSHEY_DUPLEX,
                0.8,
                (255, 255, 255),
                2,
            )
            cv2.putText(
                frame,
                f"HP: {game['health']}",
                (20, 395),
                cv2.FONT_HERSHEY_DUPLEX,
                0.8,
                (255, 255, 255),
                2,
            )
            if game["health"] == 0:
                cv2.putText(
                    frame,
                    "TARGET DOWN",
                    (50, 100),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1.3,
                    (0, 255, 255),
                    2,
                )

            cv2.imshow("frame", frame)
            if cv2.waitKey(1) == ord("q"):
                break
    finally:
        cap.release()
        pose.close()
        face.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
