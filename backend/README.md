# 🚀 AppBit Painel — Backend Core

Bem-vindo ao repositório do **Backend do AppBit Painel**! Esta aplicação foi desenvolvida em **FastAPI** para fornecer uma API robusta, rápida e documentada, que serve dados de telecomunicações e mobilidade integrados com um assistente inteligente de IA.

O projeto já está integrado na branch `dev` e pronto a ser utilizado pela equipa de Frontend e Base de Dados.

---

## 🛠️ O Que Foi Feito

1. **Estrutura Base FastAPI**:
   - Inicialização e configuração de CORS para integração com o Frontend.
   - Suporte nativo a encoding UTF-8 em todas as respostas JSON, prevenindo corrupção de caracteres no PowerShell do Windows.
   - Documentação OpenAPI automática acessível em `/docs` (Swagger UI) e `/redoc`.

2. **Rotas e Endpoints**:
   - `GET /health`: Verifica o estado do servidor, da base de dados e do serviço de IA.
   - `GET /mapa`: Retorna os dados agregados dos clusters de rede reais (Florianópolis) com coordenadas de latitude/longitude e métricas de desempenho.
   - `GET /regioes`: Devolve a lista das regiões (municípios) disponíveis no dataset.
   - `GET /indicadores`: Devolve a lista de indicadores disponíveis para consulta.
   - `POST /dados`: Endpoint de consulta em linguagem natural que interpreta a pergunta com IA, pesquisa nos dados reais de rede e gera uma síntese informativa em Português.

3. **Integração com IA (OpenRouter)**:
   - Configurado para utilizar o modelo gratuito de alto desempenho **`google/gemini-2.5-flash:free`** (ou alternativas configuráveis via `.env`).
   - Fallback inteligente que garante o funcionamento da API e a resposta em linguagem natural mesmo se a quota do OpenRouter ou a ligação à internet falhar.

4. **Qualidade e Testes**:
   - Implementação de **20 testes automatizados** com `pytest` cobrindo a integridade dos dados, validação de limites, deteção automática de ordenação (maior/menor), e tratamento de erros.

---

## ⚙️ Configuração e Instalação

Siga estes passos simples para colocar o servidor a correr localmente no seu computador:

### 1. Clonar e Aceder ao Diretório do Backend
No seu terminal, certifique-se de que está na pasta `backend`:
```bash
cd backend
```

### 2. Criar e Ativar um Ambiente Virtual (Recomendado)
Para isolar as dependências:
* **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar as Dependências
Instale todos os pacotes necessários listados em [requirements.txt](file:///c:/Users/User/Documents/Hackathon_Wongola/backend/requirements.txt):
```bash
pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente
Copie o ficheiro `.env.example` para `.env`:
```bash
cp .env.example .env
```
Abra o ficheiro `.env` criado e preencha com a sua chave do **OpenRouter** para poder testar a IA:
```env
OPENROUTER_API_KEY=sk-or-v1-a_tua_chave_aqui
```
> [!NOTE]
> Podes obter uma chave gratuita registando-te em [openrouter.ai](https://openrouter.ai).

---

## 🏃 Como Executar o Servidor

Com o ambiente virtual ativo e o `.env` configurado, inicie o servidor de desenvolvimento:
```bash
python -m uvicorn app.main:app --reload --port 8000
```
O servidor ficará disponível em **`http://127.0.0.1:8000`**.

---

## 🧪 Como Testar

Pode testar o backend usando qualquer um dos métodos abaixo:

### 1. Documentação Interativa (Swagger UI) 🌟
Abra o navegador em:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

Esta é a forma mais simples e visual de ver todos os endpoints, testar os parâmetros e analisar as respostas JSON detalhadas.

### 2. Testes Automáticos
Corra a suite de 20 testes unitários e de integração para garantir que está tudo operacional:
```bash
python -m pytest tests/ -v --tb=short
```

### 3. Testes Manuais rápidos via PowerShell
Abra uma janela de PowerShell e execute estes comandos para testar os endpoints:

* **Teste de Saúde (`/health`):**
  ```powershell
  Invoke-RestMethod http://127.0.0.1:8000/health
  ```

* **Obter os dados agregados para o mapa (`/mapa`):**
  ```powershell
  $mapa = Invoke-RestMethod http://127.0.0.1:8000/mapa
  $mapa.regioes[0] # Mostra o primeiro cluster real
  ```

* **Consulta Inteligente com IA (Maior Congestionamento):**
  ```powershell
  # Força o PowerShell a ler UTF-8 correctamente
  [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
  
  $corpo = @{ consulta = "Qual o cluster com maior congestionamento?" } | ConvertTo-Json
  $res = Invoke-RestMethod -Method POST http://127.0.0.1:8000/dados -ContentType "application/json" -Body $corpo
  
  Write-Host "Resposta da IA:" $res.resposta_ia
  Write-Host "Dados retornados:" ($res.dados | Out-String)
  ```

* **Consulta Inteligente com IA (Menor Congestionamento):**
  ```powershell
  $corpo = @{ consulta = "Qual o cluster com menor congestionamento?" } | ConvertTo-Json
  $res = Invoke-RestMethod -Method POST http://127.0.0.1:8000/dados -ContentType "application/json" -Body $corpo
  
  Write-Host "Resposta da IA:" $res.resposta_ia
  Write-Host "Cluster identificado:" $res.dados[0].cluster
  Write-Host "Valor:" $res.dados[0].congestionamento_medio
  ```

---

## 📁 Estrutura de Código Relevante

- [app/main.py](file:///c:/Users/User/Documents/Hackathon_Wongola/backend/app/main.py): Ponto de entrada FastAPI.
- [app/api/routers/](file:///c:/Users/User/Documents/Hackathon_Wongola/backend/app/api/routers/): Pasta que contém as rotas individuais.
- [app/services/llm_service.py](file:///c:/Users/User/Documents/Hackathon_Wongola/backend/app/services/llm_service.py): Comunicação com a IA e formatação de saídas estruturadas.
- [app/services/data_service.py](file:///c:/Users/User/Documents/Hackathon_Wongola/backend/app/services/data_service.py): Leitura, filtragem e agregação de dados reais do arquivo CSV.
- [tests/](file:///c:/Users/User/Documents/Hackathon_Wongola/backend/tests/): Testes automatizados da API.

Qualquer dúvida ou sugestão de melhoria, entrem em contacto ou submetam um PR para a branch `dev`! 🤝
