# 🚴‍♂️ Smart Helmet Bike Simulation 

## 📌 Project Overview  
This project ensures **bike safety using a smart helmet detection system**.  
- If the rider **does not wear a helmet**, the bike **won’t start**.  
- If the rider **removes the helmet while riding**, the bike will **gradually slow down and stop automatically**.  
- Implemented using **YOLOv3 object detection** with OpenCV and Python.  

This project can be extended to real-world **IoT applications** where the helmet communicates with the bike ignition system.

---

## 🎥 Demo Workflow  
1. **Helmet Detected ✅** → Bike starts and speed = 100%.  
2. **No Helmet ❌** → Bike cannot start.  
3. **Helmet removed mid-ride ❌** → Bike slows step by step → stops completely.  

---

## 🛠️ Technologies Used  
- Python 3.x  
- OpenCV (cv2)  
- NumPy  
- YOLOv3 (trained on Helmet vs No-Helmet dataset)  

---

## 📂 Project Structure  
