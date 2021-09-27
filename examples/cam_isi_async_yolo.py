"""
This is the example for cam isi async yolo.
"""
import ctypes
import sys
import cv2
import time
from common import constants
from python_wrapper import kdp_wrapper

def handle_result(inf_res, r_size, frames):
    """Handle the detected results returned from the model.

    Arguments:
        inf_res: Inference result data.
        r_size: Inference data size.
        frames: List of frames captured by the video capture instance.
    """
    if r_size >= 4:
        header_result = ctypes.cast(
            ctypes.byref(inf_res), ctypes.POINTER(constants.ObjectDetectionRes)).contents
        box_result = ctypes.cast(
            ctypes.byref(header_result.boxes),
            ctypes.POINTER(constants.BoundingBox * header_result.box_count)).contents
        for box in box_result:
            x1 = int(box.x1)
            y1 = int(box.y1)
            x2 = int(box.x2)
            y2 = int(box.y2)
            frames[0] = cv2.rectangle(frames[0], (x1, y1), (x2, y2), (0, 0, 255), 3)

        cv2.imshow('detection', frames[0])
        del frames[0]
        key = cv2.waitKey(1)

        if key == ord('q'):
            sys.exit()
    return 0

def user_test_cam_yolo(dev_idx, _user_id, test_loop):
    """User test cam yolo."""
    image_source_h = 480
    image_source_w = 640
    app_id = constants.APP_TINY_YOLO3
    image_size = image_source_w * image_source_h * 2
    frames = []

    # Setup video capture device.
    capture = kdp_wrapper.setup_capture(0, image_source_w, image_source_h)
    if capture is None:
        return -1

    # Start ISI mode.
    if kdp_wrapper.start_isi(dev_idx, app_id, image_source_w, image_source_h):
        return -1


    start_time = time.time()
    # Fill up the image buffers.
    ret, img_id_tx, img_left, buffer_depth = kdp_wrapper.fill_buffer(
        dev_idx, capture, image_size, frames)
    if ret:
        return -1

    # Send the rest and get result in loop, with 2 images alternatively
    print("Companion image buffer depth = ", buffer_depth)
    kdp_wrapper.pipeline_inference(
        dev_idx, app_id, test_loop - buffer_depth, image_size,
        capture, img_id_tx, img_left, buffer_depth, frames, handle_result)

    end_time = time.time()
    diff = end_time - start_time 
    estimate_runtime = float(diff/test_loop)
    fps = float(1/estimate_runtime)    
    print("Pipeline inference average estimate runtime is ", estimate_runtime)
    print("Average FPS is ", fps)

    return 0   

def user_test_cam_isi_yolo(dev_idx, user_id):
    """User test cam isi yolo."""
    #for i in range(10):
    user_test_cam_yolo(dev_idx, user_id, 1000)
    return    
