# Protocolo de comparação Grad-CAM x máscara tumoral

Definido em 12/10/2026, antes de calcular qualquer métrica XAI. Mudanças posteriores serão declaradas como análise exploratória.

- Modelo: ResNet18, estratégia B, checkpoint da época 7. Conjunto: todo o teste (498 imagens), sem augmentation.
- Grad-CAM: camada-alvo `layer4[-1]`; classe-alvo = classe prevista. Nos erros, também o mapa da classe verdadeira, analisado à parte.
- Mapas em [0, 1], resolução original 7x7 ampliada para 224x224; máscara tumoral em 224x224.
- Binarização: limiar primário 0,5; sensibilidade em 0,3 e 0,7.
- Métricas: IoU (interseção/união entre mapa binarizado e máscara); pointing game (o pixel de maior ativação cai dentro da máscara; reportar a taxa); razão de energia = (soma do mapa dentro da máscara / soma total) / (fração da área ocupada pela máscara).
- Controle: repetir as métricas com a máscara de outra imagem do teste da mesma classe, sorteada com seed 42 (uma por imagem).
- Agregação: média, mediana e dispersão por classe, e separadas entre acertos e erros.
- Comparação real x controle: teste de Wilcoxon pareado (opcional), reportando também a dispersão.
- Seleção de exemplos (Etapa 12): 4 grupos com 3 exemplos cada, sorteados com seed 42. (1) acerto com IoU acima da mediana dos acertos; (2) acerto com IoU abaixo da mediana; (3) erro de classificação; (4) maior diferença média absoluta entre o mapa da classe prevista e o da verdadeira. Qualquer escolha manual será descrita como tal.
- Teste de sanidade (Etapa 13): aleatorizar os pesos da `layer4`, recalcular o Grad-CAM em uma amostra do teste e comparar com o original (correlação de Spearman).
- Cautela: o Grad-CAM mostra regiões relevantes segundo o método, não prova causalidade. O contexto ao redor do tumor pode ser clinicamente relevante, então olhar fora da máscara não implica explicação errada.