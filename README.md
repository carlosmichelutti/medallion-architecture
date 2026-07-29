# Medallion Architecture

Projeto de estudo para praticar uma pipeline de dados baseada na arquitetura medalhão, passando por camadas de ingestão, limpeza, modelagem analítica e publicação de métricas em banco de dados.

O objetivo principal e entender o papel de cada etapa em um fluxo de engenharia de dados:

```text
RAW -> BRONZE -> SILVER -> GOLD -> METRICS
```

## Arquitetura Usada

O projeto usa uma arquitetura medalhão com quatro momentos principais:

- **RAW**: arquivos originais, mantidos como chegaram.
- **BRONZE**: dados ingeridos em Parquet, com valores de negócio preservados como string e metadados de rastreabilidade.
- **SILVER**: dados limpos, padronizados e tipados.
- **GOLD**: modelo analítico com dimensões, fato de vendas e métricas.

As métricas finais são publicadas em um banco de dados PostgreSQL usando `pandas.to_sql`.

## Fontes Ingeridas

Os arquivos originais ficam em `data/raw`:

| Fonte | Formato | Dataset |
| --- | --- | --- |
| `customers.csv` | CSV | Clientes |
| `products.xlsx` | Excel | Produtos |
| `orders.json` | JSON | Pedidos |
| `order_items.csv` | CSV | Itens dos pedidos |

## Camada Bronze

A camada Bronze lê os arquivos da RAW e grava os dados em `data/bronze`.

Tratamentos aplicados:

- leitura de CSV, Excel e JSON;
- achatamento do JSON com campos aninhados usando separador `__`;
- conversão das colunas de negócio para string;
- inclusão de metadados:
  - `_source_file`
  - `_source_extension`
  - `_source_path`
  - `_source_row_number`
  - `_ingestion_batch_id`
  - `_ingested_at_utc`
  - `_record_hash`
- gravação em Parquet.

## Camada Silver

A camada Silver lê os Parquets da Bronze e grava dados tratados em `data/silver`.

Tratamentos aplicados:

- normalização de identificadores;
- padronização de textos e categorias;
- validação simples de e-mail, CPF e telefone;
- conversão de datas;
- conversão de valores monetarios;
- conversão de inteiros e booleanos;
- normalização de percentuais;
- padronização de canais, como `MOBILE APP` para `MOBILE_APP`;
- calculo de colunas derivadas em `order_items`:
  - `gross_amount`
  - `discount_amount`
  - `net_amount`

## Camada Gold

A camada Gold lê os dados da Silver e cria tabelas analíticas em `data/gold`.

Tabelas criadas:

| Tabela | Descricao |
| --- | --- |
| `dim_customers` | Dimensão de clientes |
| `dim_products` | Dimensão de produtos |
| `dim_date` | Dimensão de datas |
| `fact_sales` | Fato de vendas no nível de item do pedido |

A granularidade da `fact_sales` e:

```text
1 linha = 1 item vendido dentro de um pedido
```

Por isso, campos de cabecalho do pedido, como `total_amount` e `shipping_fee`, podem aparecer repetidos por item. Para analises de receita, use `gross_amount` e `net_amount`. Para contar pedidos, use contagem distinta de `order_id`.

## métricas Disponibilizadas

As métricas ficam em `scripts/gold/metrics` e sao publicadas no banco de dados PostgreSQL.

| Metrica | Descricao |
| --- | --- |
| `gross_revenue` | Receita bruta total |
| `net_revenue` | Receita liquida total |
| `net_revenue_by_channel` | Receita liquida por canal |
| `net_revenue_by_payment_method` | Receita liquida por metodo de pagamento |
| `orders_by_customer` | Quantidade de pedidos por cliente |
| `orders_by_date` | Quantidade de pedidos por data |
| `orders_by_product` | Quantidade de pedidos por produto |

## Como Executar

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Crie o arquivo `scripts/configuration/.env` com as credenciais do banco, usando `scripts/configuration/.env.example` como referência:

```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=medallion
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
```

Execute a pipeline completa:

```powershell
python main.py
```

## Estrutura Principal

```text
data/
  raw/
  bronze/
  silver/
  gold/

scripts/
  bronze/
  silver/
  gold/
    metrics/
  configuration/
  database/

main.py
requirements.txt
```
