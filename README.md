## Welcome to the computer vision finger counter project. 📓
### ContadorDedos-Arduino 📖

This project, with the use of the opencv, mediapipe, numpy, serial, time and math Python libraries, is capable of detecting human hands, capturing the coordinate plane in the image captured by the camera and counting the raised fingers.

The number of raised fingers is taken and sent through serial communication to an Arduino Uno, to turn LEDs on and off. This project aims to study artificial vision.
### Hand landmarks 📖
[![Captura.png](https://i.postimg.cc/Yq2Z6g4G/Captura.png)](https://postimg.cc/4nMWZYQs)

These coordinates are painted by Mediapipe, they allow the calculation of the centroid of the palm and obtain the Eucludean distances between each pair of points.
## Example ✏️: 
[![VSIA.jpg](https://i.postimg.cc/fydPLjkk/VSIA.jpg)](https://postimg.cc/Fk9pCSyQ)
