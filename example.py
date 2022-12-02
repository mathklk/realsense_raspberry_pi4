#!/usr/bin/python3
print('importing libraries...')
import pyrealsense2 as rs2
import cv2
import numpy as np

print('starting pipeline...')
pipe = rs2.pipeline()
cfg = rs2.config()
cfg.enable_stream(rs2.stream.depth, 640, 480, rs2.format.z16, 30)
profile = pipe.start(cfg)

colorizer = rs2.colorizer()

try:
    for _ in range(5):
        pipe.wait_for_frames() # drop the first few frames
    print('Starting camera, press q to quit')
    while True:
        frameset = pipe.wait_for_frames()
        depth_frame = frameset.get_depth_frame()
        colorized_depth_frame = np.asanyarray(colorizer.colorize(depth_frame).get_data())
        cv2.imshow('Realsense Depth Image', colorized_depth_frame)
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break
finally:
    pipe.stop()
    cv2.destroyAllWindows()