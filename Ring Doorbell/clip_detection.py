import os
import cv2
from PIL import Image
import torch
import clip
     
# Load CLIP model and preprocessor
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)

# Define classes
classes = ["that does not contain a cardboard box", "of a cardboard box"]

# Open the video file
video_path = "packages.mp4"
cap = cv2.VideoCapture(video_path)

# Text to match to image
text_classes = ["a photo " + c for c in classes]
text_inputs = clip.tokenize(text_classes).to(device)

# Process each frame

frame_num = 0
while cap.isOpened():
    ret, frame = cap.read()
    frame_num+=1

    if frame_num % 10 != 0:
        cv2.imshow('Frame', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
          break
        continue
    if not ret:
        break
    
    # Convert frame to PIL image
    frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    # Preprocess frame
    image_input = clip_preprocess(frame_pil).unsqueeze(0).to(device)
    
    # Calculate image features
    with torch.no_grad():
        image_features = clip_model.encode_image(image_input)
        image_features /= image_features.norm(dim=-1, keepdim=True)
    
        # Calculate text features
        text_features = clip_model.encode_text(text_inputs)
        text_features /= text_features.norm(dim=-1, keepdim=True)
    
    # Calculate similarity with classes
    similarity = (100.0 * image_features @ text_features.T)
    p_class_given_image = similarity.softmax(dim=-1)
    values, indices = p_class_given_image[0].topk(2)
    
    # Print prediction results
    print("\nTop predictions:\n")
    for value, index in zip(values, indices):
        print(f"{classes[index]:>16s}: {100 * value.item():.2f}%")
    
    # Display frame
    cv2.imshow('Frame', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
