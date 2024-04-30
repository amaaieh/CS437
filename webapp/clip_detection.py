# pip install git+https://github.com/openai/CLIP.git
import os
import cv2
from PIL import Image
import torch
import clip
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"


class BoxDetector:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.clip_model, self.clip_preprocess = clip.load(
            "ViT-B/32", device=self.device
        )
        self.classes = ["that does not contain a cardboard box", "of a cardboard box"]
        self.text_classes = ["a photo " + c for c in self.classes]
        self.text_inputs = clip.tokenize(self.text_classes).to(self.device)

    def test(self):
        cap = cv2.VideoCapture(0)
        frame_num = 0
        while cap.isOpened():
            ret, frame = cap.read()
            cv2.imshow("Frame", frame)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                break
            if not ret:
                break

            contains_box = self.hasBox(frame)
            print(contains_box)
            # Best is a box
            # print(indices)
            # print("Worse confidence: " + str(values[1].item()))
            # if best == 1 and confidence > .75:
            # print("Box: " + str(confidence))
            # else:
            # print("No box: " + str(confidence))

        cap.release()
        cv2.destroyAllWindows()

    def hasBox(self, frame):
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image_input = self.clip_preprocess(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            image_features = self.clip_model.encode_image(image_input)
            image_features /= image_features.norm(dim=-1, keepdim=True)
            text_features = self.clip_model.encode_text(self.text_inputs)
            text_features /= text_features.norm(dim=-1, keepdim=True)
        similarity = 100.0 * image_features @ text_features.T
        p_class_given_image = similarity.softmax(dim=-1)
        values, indices = p_class_given_image[0].topk(2)

        best = indices[0]
        confidence = values[0].item()
        if best == 1 and confidence > 0.75:
            return True
        else:
            return False


# Example usage:
# detector = BoxDetector()
# detector.test()
