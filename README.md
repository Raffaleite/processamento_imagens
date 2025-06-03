# Projeto de Processamento de Imagens

Este projeto implementa 4 funcionalidades de processamento de imagens:

1. **Clusterização de tons de cinza**
2. **Subtração entre imagens para detecção de corpo**
3. **Aplicação de filtro High-Boost e comparação com filtro Passa Alta**
4. **Benchmark entre convolução espacial e convolução no domínio da frequência**

---

## ✅ Requisitos

Antes de executar, instale as bibliotecas necessárias:

```bash
pip install opencv-python numpy matplotlib
```

ou

```bash
pip install requirements.txt
```

se der erro por conta do windows

```bash
pip install --user opencv-python numpy matplotlib
```

---

## 📁 Estrutura de arquivos

* `main.py`: Código-fonte principal com todas as funcionalidades.
* `README`: Instruções de uso.
* Imagens de entrada: fornecidas por você (ex: `imagem.jpg`, `background.jpg`, `foreground.jpg`) ou utilizar as que já está no repositorio

---

## ▶️ Como executar

### 1. Clusterização de Tons de Cinza

Agrupa os tons de cinza a cada 4 níveis.

```bash
python main.py --gray-cluster imagem.jpg
```

📌 Saída: `clustered_output.png`

---

### 2. Subtração entre imagens para detecção de corpo

Use duas imagens:

* `background.jpg`: apenas o fundo (sem você)
* `foreground.jpg`: com você posicionado no mesmo local

```bash
python main.py --subtract background.jpg foreground.jpg
```

📌 Saída: `body_detection_output.png` (com seu corpo detectado e retângulo vermelho)

---

### 3. Filtro High-Boost e Passa Alta

Aplica os dois filtros para comparação visual:

```bash
python main.py --filter imagem.jpg
```

📌 Saídas:

* `high_boost_output.png`
* `high_pass_output.png`

---

### 4. Benchmark de Convolução

Compara o tempo da convolução espacial vs frequência:

```bash
python main.py --benchmark imagem.jpg
```

📌 Saídas:

* `spatial_convolution_output.png`
* `frequency_convolution_output.png`

⌛ Tempos de execução serão exibidos no terminal.

---

## ❗ Observações

* As imagens devem estar no mesmo diretório que o `main.py`, ou forneça o caminho completo.
* Recomenda-se usar imagens de tamanho moderado (menos de 2MB) para melhor desempenho.
* Para subtração, a câmera deve estar fixa entre as capturas!

---


