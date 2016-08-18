import pyautogui
import cv2
hand_pos = [250, 250, 350, 350]  # hand position
hand_convex_number = 1


class ParcourBearGame:
    def __init__(self, cap, tracker):
        self.cap = cap
        self.tracker = tracker
        self.jump_vertical_ratio = 0.01

    def init_parcour_game(self):
        pyautogui.moveTo(850, 770, 2, pyautogui.easeInQuad)
        pyautogui.click()
        pyautogui.moveTo(800, 600, 2, pyautogui.easeInQuad)
        pyautogui.click()

    def start_game(self, track_pos_prev):
        pyautogui.moveTo(450, 870, 2, pyautogui.easeInQuad)
        pyautogui.click()
        self.track_pos_prev = track_pos_prev

    def update(self, track_pos_prev):
        # cap, tracker, track_pos_prev:
        ret, img = self.cap.read()
        self.tracker.update(img)
        pos = self.tracker.get_position()
        track_pos_current = [(pos.left() + pos.right()) / 2., (pos.top() + pos.bottom()) / 2.]
        vertical_ratio = (track_pos_current[1] - track_pos_prev[1]) / img.shape[1]
        self.track_pos_prev = track_pos_prev
        # we add the velocity is propotional to the hand motion function
        self.flap_up_velocity = vertical_ratio / self.jump_vertical_ratio * 1

        print("Vertical ration is %f" % vertical_ratio)
        # if the ratio is larger than jump_vertical_ratio, then it is a jump
        if vertical_ratio > self.jump_vertical_ratio:
                pyautogui.click()

        cv2.rectangle(img, (int(pos.right()), int(pos.bottom())), (int(pos.left()), int(pos.top())),
                      (255, 0, 0), 0)
        left = max(0, int(pos.left()))
        right = min(img.shape[0], int(pos.right()))
        top = max(0, int(pos.top()))
        bottom = min(img.shape[1], int(pos.bottom()))
        crop_img = img[top:bottom, left:right]
        cv2.imshow('Gesture', img)
        cv2.waitKey(1)
