# Contratos da API — Especificação Técnica

Esta documentação define a interface de comunicação (API) entre o Frontend (React), o Backend Core (FastAPI) e a camada de Inteligência Artificial (LLM). Todos os endpoints devem validar rigorosamente os dados de entrada e responder utilizando as estruturas abaixo.

---

## 1. Monitorização e Saúde

### `GET /health`
Verifica o estado operacional da API e das suas dependências externas (Base de Dados e Serviço LLM via OpenRouter).

* **Parâmetros de Entrada:** Nenhum.
* **Resposta de Sucesso (`200 OK`):**
  ```json
  {
    "status": "healthy",
    "timestamp": "2026-06-25T13:45:46.000Z",
    "services": {
      "database": "connected",
      "llm": "available"
    }
  }
  ```
* **Resposta de Erro (`503 Service Unavailable`):**
  ```json
  {
    "status": "unhealthy",
    "timestamp": "2026-06-25T13:45:46.000Z",
    "services": {
      "database": "disconnected",
      "llm": "unavailable"
    }
  }
  ```

---

## 2. Consulta Inteligente (Orquestração de IA)

### `POST /dados`
Recebe uma pergunta em linguagem natural, interpreta os parâmetros necessários, consulta a base de dados do Supabase e retorna uma síntese textual gerada pela IA juntamente com os dados brutos e fontes associadas.

* **Parâmetros de Entrada (JSON Body):**
  | Campo | Tipo | Obrigatório | Descrição |
  | :--- | :--- | :--- | :--- |
  | `consulta` | `string` | Sim | Pergunta em português (ex: "Qual é o município com maior congestionamento?") |
  | `filtros` | `object` | Não | Filtros opcionais estruturados (ex: `{"municipio": "Cazenga", "periodo": "noite"}`) |
  | `idioma` | `string` | Não | Idioma da resposta. Padrão: `"pt"` |

* **Exemplo de Pedido (Body):**
  ```json
  {
    "consulta": "Onde há maior concentração de utilizadores com sinal fraco no período da tarde?",
    "filtros": {},
    "idioma": "pt"
  }
  ```

* **Resposta de Sucesso (`200 OK`):**
  ```json
  {
    "resposta_ia": "Com base nos dados analisados para o período da tarde, o município de Viana apresenta a maior concentração de utilizadores (4.500 ativos) expostos a um sinal de rede precário (média de -102 dBm). Recomenda-se o reforço de infraestrutura nesta zona.",
    "dados": [
      {
        "regiao_id": 2,
        "nome_cluster": "Viana_Centro",
        "municipio": "Viana",
        "n_usuarios": 4500,
        "congestionamento_medio": 0.35,
        "cobertura_sinal_dbm": -102.0
      }
    ],
    "fontes": [
      {
        "tabela": "concentracao",
        "descricao": "Dados de tráfego e qualidade de rede do dataset Vísent"
      }
    ]
  }
  ```

* **Respostas de Erro:**
  * **`400 Bad Request`:** Pedido mal estruturado ou consulta vazia.
    ```json
    {
      "detail": "A consulta em linguagem natural não pode estar vazia."
    }
    ```
  * **`500 Internal Server Error`:** Erro inesperado no processamento ou na comunicação com o fornecedor de IA.
    ```json
    {
      "detail": "Falha na comunicação com o serviço de inteligência artificial."
    }
    ```

---

## 3. Dados do Mapa Interativo

### `GET /mapa`
Retorna as coordenadas geográficas, perfis e indicadores consolidados de todas as regiões/clusters para renderização no mapa Leaflet.

* **Parâmetros de Entrada (Query Parameters):**
  | Campo | Tipo | Obrigatório | Descrição |
  | :--- | :--- | :--- | :--- |
  | `indicador` | `string` | Não | Filtro por indicador específico (valores: `n_usuarios`, `congestionamento_medio`, `cobertura_sinal_dbm`) |

* **Resposta de Sucesso (`200 OK`):**
  ```json
  {
    "regioes": [
      {
        "id": 1,
        "nome_cluster": "Cazenga_1",
        "municipio": "Cazenga",
        "latitude": -8.8123,
        "longitude": 13.2945,
        "perfil": "Residencial denso",
        "n_usuarios": 3800,
        "congestionamento_medio": 0.45,
        "cobertura_sinal_dbm": -95.2
      },
      {
        "id": 2,
        "nome_cluster": "Viana_Centro",
        "municipio": "Viana",
        "latitude": -8.9012,
        "longitude": 13.3854,
        "perfil": "Industrial / Comercial",
        "n_usuarios": 4500,
        "congestionamento_medio": 0.35,
        "cobertura_sinal_dbm": -102.0
      }
    ]
  }
  ```

---

## 4. Endpoints de Suporte (Filtros e Metadados)

### `GET /regioes`
Retorna a listagem simplificada de todas as regiões e municípios disponíveis no sistema para preenchimento de seletores no frontend.

* **Resposta de Sucesso (`200 OK`):**
  ```json
  {
    "regioes": [
      {
        "id": 1,
        "nome_cluster": "Cazenga_1",
        "municipio": "Cazenga"
      },
      {
        "id": 2,
        "nome_cluster": "Viana_Centro",
        "municipio": "Viana"
      }
    ]
  }
  ```

### `GET /indicadores`
Retorna os metadados dos indicadores suportados pela plataforma.

* **Resposta de Sucesso (`200 OK`):**
  ```json
  {
    "indicadores": [
      {
        "id": "n_usuarios",
        "nome": "Número de Utilizadores",
        "descricao": "Volume de utilizadores móveis ativos na região"
      },
      {
        "id": "congestionamento_medio",
        "nome": "Congestionamento Médio",
        "descricao": "Taxa média de congestionamento dos canais de tráfego"
      },
      {
        "id": "cobertura_sinal_dbm",
        "nome": "Nível de Sinal (dBm)",
        "descricao": "Qualidade da cobertura de rede em decibéis-miliwatts"
      }
    ]
  }
  ```
