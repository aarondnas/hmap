import cv2
import depthai as dai # this is the oak-d-lite computer

from hmap import Gradient_Huemap_Stream

def generate():
    pipeline = dai.Pipeline()

    # Create the ColorCamera node and set its properties
    camRgb = pipeline.create(dai.node.ColorCamera)
    camRgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)

    # Create the XLinkOut node for the video stream and set its properties
    xoutRgb = pipeline.create(dai.node.XLinkOut)
    xoutRgb.setStreamName("My first stream")

    # Link the ColorCamera to the XLinkOut node
    camRgb.video.link(xoutRgb.input)

    # Start the pipeline
    with dai.Device(pipeline) as device:
        video_queue = device.getOutputQueue(name="My first stream", maxSize=4, blocking=False) # get the video stream queue
        
        # hmap setup
        scale_factor = 1
        cold_color = (4, 0, 255)
        hot_color = (21, 255, 0)
        #steps = 600
        clockwise = False
        frame = video_queue.get().getCvFrame() # get the video frame
        huemap_instance = Gradient_Huemap_Stream(frame,scale_factor,cold_color,hot_color,clockwise)

        while True:
            frame = video_queue.get().getCvFrame() # get the video frame

          # <you can add fancy processing of the video frame here>
            frame =  huemap_instance.stream_gradient_huemap(frame) # result is rgb format
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            #frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
          # <you can add fancy processing of the video frame here>

            (flag, encodedImage) = cv2.imencode(".jpg", frame) # encode the frame into a jpeg image
            if not flag:
                continue
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')



from dash import html
def simple_layout():
    return html.Div([
            html.Iframe(src="/video_feed", width="1200", height="800", id="video-stream"),
            ], style={'width': '100%', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
            )




import dash
from flask import Response

# replace stream_oak_d_lite with the name of your script in step 2 above
#from streaming_oak_d_lite import generate 

# also for the layout, use the name you used to store the layout code 
#from layout import simple_layout 

app = dash.Dash(__name__)
app.layout = simple_layout()

@app.server.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")

#if __name__ == "__main__":
app.run_server(debug=True)




