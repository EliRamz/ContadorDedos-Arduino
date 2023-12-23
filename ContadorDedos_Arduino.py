import cv2
import mediapipe as mp
import numpy as np
import math
import serial
import time

#Comunicacion serial arduino
ser = serial.Serial('COM9',12900,timeout=1)
time.sleep(1)


def centroide_palma(coordenadas_palma): ##Aqui se envia la lista de datos de los dedos para calcular el centroide
    coordenadas = np.array(coordenadas_palma)
    centroide = np.mean(coordenadas,axis=0) #calculo la media
    centroide = int(centroide[0]), int(centroide[1])
    return centroide

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles= mp.solutions.drawing_styles
mp_hand = mp.solutions.hands

video= cv2.VideoCapture(0)


#Pulgar
Puntos_pulgar = [1, 2, 4]

#Puntos del Indice,medio, anular y meñique
Puntos_palma = [1,2, 5, 9, 13, 17] # base de los dedos, o sea, la palma
Puntas_dedos= [8,12,16,20] #Punta de los dedos 
puntos_falange=[6,10,14,18] #Falange de de los dedos, no se como se llama

with mp_hand.Hands( model_complexity=1,
    max_num_hands=1,
    min_detection_confidence=.5,
    min_tracking_confidence=.5) as hands:
    
    while (video.isOpened()):
        ret,imagen= video.read()
        
        if ret==True:
            imagen= cv2.flip(imagen,1)
            heigth,width, _ = imagen.shape #Toma el alto y ancho de la imagen
            imagen_rgb = cv2.cvtColor(imagen,cv2.COLOR_BGR2RGB) #Convierte la imagen de BGR A RGB
            results = hands.process(imagen_rgb) # Procesa la imagen RGBm usa el objeto hands para ellos detecta 
                                                #Analiza todas las manos presentes en la imagen y retorna el resultados
                                                #este resultado puede incluir las marcas de referencia de la conexion de la mano
        Contador_dedos=' '
        
        if results.multi_hand_landmarks: ##Si existe la deteccion de manos se visualiza
            #Array para obtener las coordenadas de los puntos de los dedos
            coordenadas_pulgar=[]
            coordenadas_palma=[]
            coordenadas_PuntasDedos=[]
            coordenadas_falange=[]
            for hand_landmarks in results.multi_hand_landmarks:
                
                for contadorPuntos in Puntos_pulgar:
                    x= int(hand_landmarks.landmark[contadorPuntos].x * width) # se multiplica la cordenada por el tamaño horizontal
                    y= int(hand_landmarks.landmark[contadorPuntos].y * heigth) # se multiplica la cordenada por el tamaño vertical
                    coordenadas_pulgar.append([x,y])
                
                for contadorPuntos in Puntos_palma :
                    x= int(hand_landmarks.landmark[contadorPuntos].x * width) # se multiplica la cordenada por el tamaño horizontal
                    y= int(hand_landmarks.landmark[contadorPuntos].y * heigth) # se multiplica la cordenada por el tamaño vertical
                    coordenadas_palma.append([x,y])
                    
                for contadorPuntos in Puntas_dedos :
                    x= int(hand_landmarks.landmark[contadorPuntos].x * width) # se multiplica la cordenada por el tamaño horizontal
                    y= int(hand_landmarks.landmark[contadorPuntos].y * heigth) # se multiplica la cordenada por el tamaño vertical
                    coordenadas_PuntasDedos.append([x,y])
                    
                for contadorPuntos in puntos_falange :
                    x= int(hand_landmarks.landmark[contadorPuntos].x * width) # se multiplica la cordenada por el tamaño horizontal
                    y= int(hand_landmarks.landmark[contadorPuntos].y * heigth) # se multiplica la cordenada por el tamaño vertical
                    coordenadas_falange.append([x,y])
                    
                #Calculo del movimiento del pulgar
                
                p1 = np.array(coordenadas_pulgar[0])
                p2 = np.array(coordenadas_pulgar[1])
                p3 = np.array(coordenadas_pulgar[2])
                
                l1 = np.linalg.norm(p2-p3)
                l2 = np.linalg.norm(p1-p3)
                l3 = np.linalg.norm(p1-p2)
                
                #calculo del angulo
                angulo = math.degrees(math.acos((l1**2 + l3**2 - l2**2) / (2 * l1 * l3)))
                dedo_pulgar = np.array(False)
                if angulo > 150:
                    dedo_pulgar = np.array(True)
                
                ##Indice, medio, anular, y meñique-Calculo
                #Centroido-Calculo
                nx,ny = centroide_palma(coordenadas_palma)
                cv2.circle(imagen,(nx,ny),3,(0,0,0),2) #se dibuja un circulo en el centro de la palma
                coordenadas_centroide = np.array([nx,ny]) #se almacenan los arrays numpy de cada punto necesario de los dedos
                coordenadas_PuntasDedos = np.array(coordenadas_PuntasDedos)
                coordenadas_falange = np.array(coordenadas_falange)
                
                #Distancias euclidiana entre cada par de puntos en un eje, el cual devuelve un array
                distancia_centroide_puntasDedos = np.linalg.norm(coordenadas_centroide - coordenadas_PuntasDedos,axis=1)
                distancia_centroide_falange = np.linalg.norm(coordenadas_centroide - coordenadas_falange,axis=1)
                
                diferencia = distancia_centroide_puntasDedos - distancia_centroide_falange
                
                dedos = diferencia > 0
                dedos = np.append(dedo_pulgar, dedos)
                Contador_dedos = str(np.count_nonzero(dedos==True))
                
                if int(Contador_dedos) > -1 :
                    ser.write(Contador_dedos.encode())
                
                mp_drawing.draw_landmarks(imagen,
                                        hand_landmarks,
                                        mp_hand.HAND_CONNECTIONS,
                                        mp_drawing_styles.DrawingSpec(color=(0,0,0),thickness=3,circle_radius=2), #Estilos de los puntso de referencia de las manos
                                        mp_drawing_styles.DrawingSpec(color=(0,0,255),thickness=3)) #Estilos las conexiones a los puntos de las manos
                
        cv2.rectangle(imagen,(10,10),(90,90),(0,0,0),-1)
        cv2.putText(imagen,Contador_dedos,(20,80),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,255),2)
        cv2.imshow("Video",imagen)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
        
video.release()
cv2.destroyAllWindows()
ser.close()