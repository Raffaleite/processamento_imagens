import cv2
import numpy as np
import time
import argparse
from numpy.fft import fft2, ifft2
import matplotlib.pyplot as plt

# 1. Clusterização de Tons de Cinza
def gray_cluster(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clustered = (gray // 4) * 4
    cv2.imwrite("clustered_output.png", clustered)
    print("Imagem clusterizada salva como 'clustered_output.png'")


# ---------------------------------------------------------------------------------
# 2. Subtração para Detecção de Corpo
def subtract_and_detect(background_path, foreground_path, threshold=30):
    bg = cv2.imread(background_path, cv2.IMREAD_GRAYSCALE)
    fg = cv2.imread(foreground_path, cv2.IMREAD_GRAYSCALE)
    diff = cv2.absdiff(fg, bg)
    _, binary = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    result = cv2.cvtColor(fg, cv2.COLOR_GRAY2BGR)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(result, (x, y), (x+w, y+h), (0, 0, 255), 2)
    cv2.imwrite("body_detection_output.png", result)
    print("Resultado da subtração salvo como 'body_detection_output.png'")


# ---------------------------------------------------------------------------------
# 3. Filtro High-Boost e Passa Alta
def high_boost_filter(img, A=1.5):
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    mask = cv2.subtract(img, blurred)
    high_boost = cv2.addWeighted(img, A, mask, 1, 0)
    return high_boost

def high_pass_filter(img):
    kernel = np.array([[-1, -1, -1],
                       [-1,  8, -1],
                       [-1, -1, -1]])
    return cv2.filter2D(img, -1, kernel)

def apply_filters(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    high_boost = high_boost_filter(img)
    high_pass = high_pass_filter(img)
    cv2.imwrite("high_boost_output.png", high_boost)
    cv2.imwrite("high_pass_output.png", high_pass)
    print("Filtro High-Boost salvo como 'high_boost_output.png'")
    print("Filtro Passa Alta salvo como 'high_pass_output.png'")

    print("\n--- Análise dos Resultados ---")
    print("O filtro Passa Alta enfatiza principalmente as bordas, gerando uma imagem com contornos destacados,")
    print("mas pode deixar a imagem com aspecto mais áspero e ruidoso.")
    print("O filtro High-Boost combina o realce das bordas com a imagem original, mantendo a naturalidade")
    print("e melhorando a nitidez geral sem perder o contexto da imagem.")


# ---------------------------------------------------------------------------------
# 4. Teorema da Convolução - Comparação de Tempos
def time_convolution(img, kernel):
    start = time.time()
    result = cv2.filter2D(img, -1, kernel)
    end = time.time()
    return result, end - start

def time_freq_convolution(img, kernel):
    start = time.time()
    dft_size = tuple(np.array(img.shape) + np.array(kernel.shape) - 1)
    fft_img = fft2(img, dft_size)
    fft_ker = fft2(kernel, dft_size)
    fft_result = fft_img * fft_ker
    result = np.abs(ifft2(fft_result))
    result = result[:img.shape[0], :img.shape[1]]
    end = time.time()
    return result.astype(np.uint8), end - start

def benchmark_convolutions(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    kernel = np.ones((15, 15), np.float32) / 225
    conv_result, conv_time = time_convolution(img, kernel)
    fft_result, fft_time = time_freq_convolution(img, kernel)
    cv2.imwrite("spatial_convolution_output.png", conv_result)
    cv2.imwrite("frequency_convolution_output.png", fft_result)
    print(f"Tempo domínio espacial: {conv_time:.4f} segundos")
    print(f"Tempo domínio da frequência: {fft_time:.4f} segundos")

    print("\n--- Análise dos Tempos de Execução ---")
    print("A convolução no domínio espacial é direta e pode ser eficiente para kernels pequenos,")
    print("mas seu custo cresce com o tamanho do kernel e da imagem.")
    print("A convolução no domínio da frequência, baseada no Teorema da Convolução, tem custo inicial maior")
    print("devido à FFT e iFFT, porém escala melhor para kernels maiores, resultando em ganho computacional")
    print("quando aplicados filtros grandes ou em imagens maiores.")
    print("Os tempos exibidos demonstram essas características, e a escolha do método depende do contexto de uso.")

# Execução por linha de comando
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--gray-cluster", help="Caminho da imagem para clusterização de tons de cinza")
    parser.add_argument("--subtract", nargs=2, help="Imagens de background e foreground para subtração")
    parser.add_argument("--filter", help="Imagem para aplicar filtros High-Boost e Passa Alta")
    parser.add_argument("--benchmark", help="Imagem para benchmarking de convolução")
    args = parser.parse_args()

    if args.gray_cluster:
        gray_cluster(args.gray_cluster)
    elif args.subtract:
        subtract_and_detect(args.subtract[0], args.subtract[1])
    elif args.filter:
        apply_filters(args.filter)
    elif args.benchmark:
        benchmark_convolutions(args.benchmark)
    else:
        print("Nenhuma operação especificada. Use --help para ver as opções.")
