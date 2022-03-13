# LITel OSA

Aqui está o meu desenvolvimento do visualizador do Analisador de Espectro Óptico (OSA) para o laboratório LITel da UFJF.

Até o dado momento, o programa funciona lendo arquivos em uma determinada pasta, que deve ser colocada a mesma pasta onde o OSA salva os espectros lidos

## Rodando o programa
Para rodar o programa, basta:
- Instalar os requerimentos (pip install -r requirements.txt)
- Rodar o main.py
- Colocar as configurações adequadas

### Features:
- Calibração (botão com um termômetro):
  - Permite calibrar o sensor usando um caminho determinado de passos. A calibração fica salva e o programa usa a última feita ao abrir
- Dividir janela:
  - Abre uma janela extra para cada vale localizado no espectro, e acompanha seus valores como se fossem o vale principal
