# Pipeline de Dados Serverless na AWS para Coleta de Dados Financeiros

## 📖 Visão Geral do Projeto

Este projeto implementa um pipeline de dados 100% serverless na nuvem da AWS para automatizar a coleta, armazenamento e análise de dados financeiros. A solução foi projetada para ser de baixo custo, escalável e de baixa manutenção, utilizando as melhores práticas de engenharia de dados na nuvem.

O pipeline coleta diariamente a cotação do Dólar (PTAX) a partir da API pública do Banco Central do Brasil e armazena os dados em um Data Lake no Amazon S3, tornando-os disponíveis para consulta via SQL.

## 🏗️ Arquitetura da Solução

A arquitetura foi construída utilizando os seguintes serviços da AWS, que interagem de forma orquestrada para compor o fluxo de dados:

<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/b5235e52-7931-435c-ac65-14f22d616473" />


**Fluxo de Dados:**
1.  **Amazon EventBridge:** Atua como o orquestrador (scheduler), disparando o pipeline em uma agenda pré-definida (ex: duas vezes ao dia).
2.  **AWS Lambda:** O coração do pipeline. Uma função Python é executada para fazer a requisição à API externa, processar os dados e salvá-los no S3.
3.  **Amazon S3:** Serve como um Data Lake centralizado, armazenando os arquivos JSON com os dados coletados de forma durável e econômica.
4.  **AWS Glue Crawler:** Um rastreador que escaneia automaticamente os dados no S3, infere o esquema (colunas e tipos de dados) e cria uma tabela no Catálogo de Dados do Glue.
5.  **Amazon Athena:** Permite a execução de consultas SQL padrão diretamente nos arquivos armazenados no S3, utilizando o esquema do Catálogo de Dados do Glue para fornecer respostas rápidas e sob demanda.

## ✨ Features

* **100% Serverless:** Nenhum servidor para gerenciar, com custo zero quando o pipeline não está em execução.
* **Automação Completa:** O agendamento via EventBridge garante que os dados sejam coletados sem qualquer intervenção manual.
* **Descoberta de Esquema Automática:** O Glue Crawler adapta o catálogo de dados a possíveis mudanças no formato dos arquivos.
* **Análise via SQL:** Permite que analistas e cientistas de dados consultem os dados brutos usando uma linguagem familiar e poderosa.

## 🛠️ Tecnologias Utilizadas

* **Cloud:** AWS (Amazon Web Services)
* **Linguagem:** Python 3
* **Principais Serviços AWS:**
    * AWS Lambda
    * Amazon S3
    * Amazon EventBridge
    * AWS Glue (Crawler & Data Catalog)
    * Amazon Athena
    * AWS IAM (Identity and Access Management)

## 🚀 Como Executar (Setup)

Para replicar este projeto, os seguintes passos são necessários:

1.  **Configurar um Bucket S3:** Criar um bucket para servir como Data Lake.
2.  **Criar a Função Lambda:** Fazer o upload do código `lambda_function.py` e configurar as variáveis de ambiente (como o nome do bucket) e as permissões do IAM.
3.  **Criar o Crawler do Glue:** Apontar o crawler para o bucket S3 e configurar um banco de dados de destino.
4.  **Configurar a Regra do EventBridge:** Criar um agendamento para acionar a função Lambda na frequência desejada.

---
*Este projeto foi desenvolvido como um estudo prático de engenharia de dados na AWS. Desenvolvido por João Vítor Sgotti Veiga.*
