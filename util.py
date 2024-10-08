import math
import os
import sys
import time
from contextlib import contextmanager

import psutil
import pyautogui
import win32gui


def get_angle_from_map(origin, target):
    cx, cy = origin
    px, py = target

    dx = px - cx
    dy = py - cy

    angle = math.degrees(math.atan2(-dy, dx))

    angle = (90 - angle) % 360
    if angle < 0:
        angle += 360

    return angle


def get_distance_from_map(origin, target):
    cx, cy = origin
    px, py = target

    dx = px - cx
    dy = py - cy

    # 88 pixels per 200m block
    pixel_distance = math.sqrt(dx ** 2 + dy ** 2)
    distance = pixel_distance * (200 / 88)

    return distance


def shortest_turn_direction(current_dir, target_dir):
    """Determine the shortest turn direction and distance."""
    diff_inside = abs(target_dir - current_dir)
    diff_outside = 360 - max(target_dir, current_dir) + min(target_dir, current_dir)
    if target_dir < current_dir:
        if diff_inside < diff_outside:
            return 'A', diff_inside
        else:
            return 'D', diff_outside
    else:
        if diff_inside < diff_outside:
            return 'D', diff_inside
        else:
            return 'A', diff_outside


def hold_key(key, duration):
    with pyautogui.hold(key):
        print(f"Holding {key}")
        time.sleep(duration)
        print(f"Release {key}")


def do_task_for_time(task, duration, fps=100):
    t0 = time.time()
    while time.time() - t0 < duration:
        task()
        time.sleep(1 / fps)


@contextmanager
def switch_to_second():
    try:
        hold_key('F2', 1.4 + 0.1)
        yield  # This is where foo() will be executed.
    finally:
        hold_key('F1', 1.4 + 0.1)


# Function to set focus to another window (e.g., a game)
def switch_focus_to(game_window_title):
    hwnd = win32gui.FindWindow(None, game_window_title)
    if hwnd != 0:
        try:
            win32gui.ShowWindow(hwnd, 5)
            win32gui.SetForegroundWindow(hwnd)
        except:
            print(f"Failed to switch focus.")
            pass
    else:
        print(f"Window with title '{game_window_title}' not found.")


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # noqa
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def check_process_exists(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        try:
            if process.name() == process_name:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
