import cv2
import numpy as np

# Função vazia pro Trackbar do OpenCV
def nothing(x):
    pass

def gerar_histograma(imagem_cinza):
    hist_w, hist_h = 512, 400
    hist_img = np.zeros((hist_h, hist_w, 3), dtype=np.uint8)

    # Calcula a freq dos tons de cinza (0 a 255)
    hist = cv2.calcHist([imagem_cinza], [0], None, [256], [0, 256])

    # Normaliza os valores para caberem na janela do gráfico.
    cv2.normalize(hist, hist, alpha=0, beta=hist_h, norm_type=cv2.NORM_MINMAX)

    # Desenha as linhas do grafico
    bin_w = int(round(hist_w / 256))
    for i in range(1, 256):
        cv2.line(hist_img,
                (bin_w * (i - 1), hist_h - int(hist[i - 1])),
                (bin_w * (i), hist_h - int(hist[i])),
                (0, 255, 0), thickness=2)
    return hist_img

# Inicializa a webcam
cap = cv2.VideoCapture(0)

# Cria a janela principal e o Trackbar para Threshold
cv2.namedWindow('Threshold')
cv2.createTrackbar('Limite', 'Threshold', 127, 255, nothing)

print("Pressione 'q' para sair.")

while True:
    # Captura o frame da webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Converte para a escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Pega o valor atual do trackbar
    limite = cv2.getTrackbarPos('Limite', 'Threshold')

    # Aplica o Threshold Binário
    # Se o pixel > limite, vira 255 (Branco). 
    # Se <= limite, vira 0 (Preto).
    _, thresh = cv2.threshold(gray, limite, 255, cv2.THRESH_BINARY)

    # Gera o histograma da imagem em cinza
    hist_img = gerar_histograma(gray)

    # Exibe as janelas simultaneamente
    cv2.imshow('1 - Original', frame)
    cv2.imshow('2 - Escala de Cinza', gray)
    cv2.imshow('Threshold', thresh)
    cv2.imshow('Histograma (Bonus)', hist_img)

    # Sai do loop quando aperta 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha as janelas
cap.release()
cv2.destroyAllWindows()