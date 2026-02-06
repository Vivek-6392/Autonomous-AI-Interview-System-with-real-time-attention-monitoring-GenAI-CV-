from streamlit_webrtc import VideoProcessorBase
from vision.face_mesh import VisionPipeline


class VisionWebRTCProcessor(VideoProcessorBase):
    def __init__(self):
        self.vision = None
        self.username = None

    def set_user(self, username: str):
        """
        Initialize VisionPipeline ONCE per WebRTC session.
        """
        if self.vision is None:
            self.username = username
            self.vision = VisionPipeline(username)

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        if self.vision:
            img = self.vision.process_external_frame(img)

        return frame.from_ndarray(img, format="bgr24")
