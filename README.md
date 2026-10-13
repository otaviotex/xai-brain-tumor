# Análise de Explicabilidade (XAI) em Classificação de Tumores Cerebrais

Este repositório contém o código, os experimentos e os resultados referentes ao **Artigo 2** da disciplina de Inteligência Artificial II (Universidade de Brasília - UnB). O projeto foca no treinamento de um modelo de *Deep Learning* (ResNet18) para a classificação de tumores cerebrais em imagens de ressonância magnética (MRI) e na aplicação da técnica Grad-CAM para investigar se o modelo utiliza regiões clinicamente relevantes para suas decisões.

## Autores
* Arthur Mezzaroba Scartezini
* Otávio de Paiva Menezes 

## Fonte do Dataset
O projeto utiliza o **Figshare Brain Tumor Dataset**, um conjunto público de imagens de ressonância magnética T1 com contraste. 
* **Referência:** Cheng, J., et al. "Enhanced performance of brain tumor classification via tumor region augmentation and partition". *PLoS ONE*, 2015.
* **Classes presentes:** Glioma, Meningioma e Tumor Pituitário (Hipófise).

## Estrutura de Pastas

    xai-brain-tumor/
    ├── configs/                  # Arquivos JSON de configuração (pré-processamento e treino)
    ├── data/                     
    │   ├── raw/                  # Dataset original (NÃO INCLUÍDO NO GITHUB)
    │   └── splits/               # CSVs com as divisões de treino, validação e teste
    ├── docs/                     # Documentação auxiliar (ex: protocolo_xai.md)
    ├── notebooks/                # Jupyter Notebooks com os experimentos
    ├── results/                  # Saídas do modelo
    │   ├── teste/                # Métricas finais e matriz de confusão
    │   └── gradcam/              # Mapas .npy e figuras de calor (NÃO INCLUÍDO NO GITHUB)
    ├── requirements.txt          # Dependências do projeto
    └── README.md                 # Este documento

## Versões e Ambiente
Este projeto foi desenvolvido e homologado utilizando o ambiente do **Google Colab** e localmente, assegurando compatibilidade com as seguintes versões base:
* **Python:** 3.13 (versão base reportada no Colab via sys.version)
* **PyTorch & Torchvision:** Compatíveis com o ecossistema Colab
* **pytorch-grad-cam:** v1.5.7

## Como Reproduzir os Experimentos

1. **Clone o repositório:**
    Copie o comando abaixo no terminal:
    git clone https://github.com/SEU_USUARIO/xai-brain-tumor.git
    cd xai-brain-tumor

2. **Instale as dependências:**
    Crie um ambiente virtual (recomendado Python 3.13) e instale o pacote de requisitos:
    pip install -r requirements.txt

3. **Obtenha os Dados:**
    Baixe o dataset original do Figshare e aloque os arquivos `.mat` na pasta `data/raw/`.

4. **Ordem de Execução dos Notebooks:**
    Execute os arquivos na pasta `notebooks/` estritamente na seguinte ordem:
    * **`00_ambiente.ipynb`**: Valida a instalação das bibliotecas, verifica o hardware (CUDA), lê o dataset, faz a análise inicial das imagens e gera os arquivos CSV de divisão (train/val/test) agrupados por paciente.
    * **`01_treino.ipynb`**: Carrega as configurações (de `configs/config_preprocessamento.json` e `configs/config_treino.json`), aplica o pré-processamento, instancia a ResNet18 adaptada, realiza o *fine-tuning* e salva o checkpoint do melhor modelo e os resultados de teste na pasta `results/`.
    * **`02_xai.ipynb`** (ou notebook equivalente da Etapa 10): Carrega o checkpoint treinado com os pesos congelados, executa o Grad-CAM nas imagens do conjunto de teste e calcula as métricas de explicabilidade definidas no protocolo.

## Aviso Importante (Arquivos Ignorados)
Devido a restrições de tamanho e boas práticas de versionamento, arquivos muito grandes estão listados no `.gitignore` e **não** estão disponíveis no GitHub. Isso inclui:
* O dataset original completo (`data/raw/*.mat`).
* Os pesos (checkpoints) do modelo treinado (`*.pth`).
* Os mapas numéricos brutos do Grad-CAM (`results/gradcam/*.npy`).

Para analisar o modelo, é estritamente necessário baixar o dataset e rodar os notebooks para gerar os binários localmente.