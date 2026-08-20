# Medallion Architecture

Projeto de estudo para praticar uma pipeline de dados baseada na arquitetura medalhão, passando por ingestão, limpeza, modelagem analítica, orquestração com Airflow e publicação de métricas em PostgreSQL.

O fluxo principal do projeto é:

```text
RAW -> BRONZE -> SILVER -> GOLD -> METRICS
```

## Objetivo

O objetivo é simular um pipeline de engenharia de dados com fontes em formatos diferentes, dados brutos com inconsistências propositais e camadas progressivas de tratamento até a disponibilização de métricas agregadas para análise.

O projeto começou com execução local via `main.py` e foi evoluído para usar o Apache Airflow como orquestrador da pipeline.

## Arquitetura

O projeto usa a arquitetura medalhão:

| Camada | Papel |
| --- | --- |
| `RAW` | Arquivos originais, mantidos como chegaram |
| `BRONZE` | Ingestão dos dados em Parquet, preservando valores de negócio como string e adicionando metadados |
| `SILVER` | Limpeza, padronização, validações simples e tipagem dos dados |
| `GOLD` | Criação de dimensões, fato de vendas e base analítica |
| `METRICS` | Cálculo e carga das métricas agregadas no PostgreSQL |

## Fontes Ingeridas

Os arquivos originais ficam em `data/raw`:

| Fonte | Formato | Dataset |
| --- | --- | --- |
| `customers.csv` | CSV | Clientes |
| `products.xlsx` | Excel | Produtos |
| `orders.json` | JSON | Pedidos |
| `order_items.csv` | CSV | Itens dos pedidos |

## Camada Bronze

A camada Bronze fica em `src/bronze` e grava os arquivos gerados em `data/bronze`.

Principais tratamentos:

- leitura de arquivos CSV, Excel e JSON;
- normalização de JSON aninhado com separador `__`;
- conversão das colunas de negócio para string;
- inclusão de metadados de ingestão:
  - `_source_file`
  - `_source_extension`
  - `_source_path`
  - `_source_row_number`
  - `_ingestion_batch_id`
  - `_ingested_at_utc`
  - `_record_hash`
- gravação em Parquet.

## Camada Silver

A camada Silver fica em `src/silver` e grava os arquivos gerados em `data/silver`.

Principais tratamentos:

- normalização de identificadores;
- padronização de textos e categorias;
- validação simples de e-mail, CPF e telefone;
- conversão de datas;
- conversão de valores monetários;
- conversão de inteiros e booleanos;
- normalização de percentuais;
- padronização de canais, como `MOBILE APP` para `MOBILE_APP`;
- cálculo das colunas derivadas em `order_items`:
  - `gross_amount`
  - `discount_amount`
  - `net_amount`

## Camada Gold

A camada Gold fica em `src/gold` e grava os arquivos gerados em `data/gold`.

Tabelas criadas:

| Tabela | Descrição |
| --- | --- |
| `dim_customers` | Dimensão de clientes |
| `dim_products` | Dimensão de produtos |
| `dim_date` | Dimensão de datas |
| `fact_sales` | Fato de vendas no nível de item do pedido |

A granularidade da `fact_sales` é:

```text
1 linha = 1 item vendido dentro de um pedido
```

Por isso, campos de cabeçalho do pedido podem aparecer repetidos por item. Para análises de receita, use `gross_amount` e `net_amount`. Para contar pedidos, use contagem distinta de `order_id`.

## Métricas Disponibilizadas

As métricas ficam em `src/metrics` e são publicadas no PostgreSQL.

| Métrica | Descrição |
| --- | --- |
| `gross_revenue` | Receita bruta total |
| `net_revenue` | Receita líquida total |
| `net_revenue_by_channel` | Receita líquida por canal |
| `net_revenue_by_payment_method` | Receita líquida por método de pagamento |
| `orders_by_customer` | Quantidade de pedidos por cliente |
| `orders_by_date` | Quantidade de pedidos por data |
| `orders_by_product` | Quantidade de pedidos por produto |

## Orquestração Com Airflow

A DAG fica em `dags/dag_medallion_ecommerce_pipeline.py`.

Ela orquestra as etapas nesta ordem:

```text
generate_batch_id -> bronze -> silver -> gold -> metrics
```

O `batch_id` é gerado pela própria DAG e enviado diretamente para a task da Bronze usando TaskFlow API.

O ambiente Airflow é definido no `docker-compose.yaml` e possui:

- Airflow API Server;
- Scheduler;
- DAG Processor;
- Worker Celery;
- Triggerer;
- Redis;
- PostgreSQL para metadados do Airflow;
- PostgreSQL separado para as métricas do projeto.

## Configuração De Ambiente

O projeto possui dois exemplos de configuração:

| Arquivo | Uso |
| --- | --- |
| `config/.env.example` | Execução dentro do Docker/Airflow |
| `config/.env.local.example` | Execução local via `python main.py` |

Dentro dos containers, o host do banco de métricas é `postgres`:

```env
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=medallion-architecture
DATABASE_USER=root
DATABASE_PASSWORD=root
```

Na execução local pela máquina host, o banco é acessado via porta exposta `5433`:

```env
DATABASE_HOST=localhost
DATABASE_PORT=5433
DATABASE_NAME=medallion-architecture
DATABASE_USER=root
DATABASE_PASSWORD=root
```

Ao rodar `python main.py`, o projeto define automaticamente `MEDALLION_ENV_FILE=.env.local.example`, então a execução local usa as credenciais locais.

## Como Executar Localmente

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Suba pelo menos o banco PostgreSQL do projeto via Docker Compose:

```powershell
docker compose up postgres -d
```

Execute a pipeline completa localmente:

```powershell
python main.py
```

Esse comando executa Bronze, Silver, Gold e carrega as métricas no PostgreSQL usando `config/.env.local.example`.

## Como Executar Com Airflow

Crie o arquivo `config/.env` com base em `config/.env.example`.

Depois suba os serviços:

```powershell
docker compose up -d
```

Acesse o Airflow em:

```text
http://localhost:8080
```

Usuário e senha padrão definidos no `docker-compose.yaml`:

```text
airflow / airflow
```

No Airflow, habilite e execute a DAG:

```text
dag_medallion_ecommerce_pipeline
```

## Estrutura Principal

```text
config/
  config.py
  .env.example
  .env.local.example

dags/
  dag_medallion_ecommerce_pipeline.py

data/
  raw/
  bronze/
  silver/
  gold/

database/
  session.py
  writer.py

src/
  bronze/
  silver/
  gold/
  metrics/

docker-compose.yaml
main.py
requirements.txt
```
