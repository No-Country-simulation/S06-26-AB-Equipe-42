# data/raw/ — Datasets do Projeto AppBit Painel

Esta pasta contém os ficheiros CSV do dataset **Vísent / CDRView AppBiT** que são consumidos directamente pelo backend.

## Ficheiros presentes (versionados no git)

| Ficheiro | Tamanho | Descrição |
|---|---|---|
| `tensor_concentracao.csv` | ~1.1 MB | Concentração de utilizadores por antena, dia e período. **Fonte principal dos endpoints `/dados` e `/mapa`.** |
| `tensor_od.csv` | ~55 KB | Matriz Origem-Destino de fluxos entre clusters. |
| `tensor_fluxo_vias.csv` | ~2.6 MB | Pares de antenas consecutivas com volume de fluxo. |
| `tensor_tempo_deslocamento.csv` | ~28 KB | Distâncias e tempos médios entre clusters. |

## Ficheiros NÃO versionados (demasiado grandes para o git)

Estes ficheiros devem ser descarregados manualmente a partir da pasta partilhada do hackathon e colocados aqui:

| Ficheiro | Tamanho | Descrição |
|---|---|---|
| `tensor_mobilidade.csv` | ~2.7 GB | Base principal de mobilidade (~12M linhas). **Leitura obrigatória em chunks.** |
| `tensor_sequencias.csv` | ~960 MB | Sequência de antenas por assinante/dia. |

> **Atenção:** Ao ler `ecgi`, `ecgi_origem` ou `ecgi_destino` em pandas, force sempre `dtype={'ecgi': str}`. O pandas converte para `float64` por defeito e corrompe o identificador.

## Fonte

Dataset sintético gerado pela Visent / OSX Telecomunicações S/A para o Hackathon App BiT (Junho-Julho 2026).  
Documentação técnica completa: `appbit-main/dataset-visent/docs/CDRView_AppBiT_TechnicalReference_v2.md`
