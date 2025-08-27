# -*- coding: utf-8 -*-
"""
Função AWS Lambda para Coleta de Dados Financeiros.

Esta função é projetada para ser executada em um ambiente AWS Lambda.
Ela coleta a cotação diária do dólar (USD-BRL) da API do Banco Central do Brasil,
formata os dados em JSON e os armazena em um bucket do Amazon S3.

Autor: João Vítor Sgotti Veiga
Data: 27 de Agosto de 2025
"""

import boto3
import requests
import json
from datetime import datetime

# --- Configurações ---
# Nome do bucket S3 onde os dados serão armazenados.
# Este valor DEVE ser alterado para o nome do seu bucket.
BUCKET_NAME = "MY_BUCKET_S3"

# Endpoint da API para a cotação do Dólar (PTAX)
API_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.10813/dados/ultimos/1?formato=json"

# Inicializa o cliente do S3 fora do handler para otimizar a performance
# em execuções subsequentes (reaproveitamento de conexão em "warm starts").
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    Ponto de entrada principal para a execução da função Lambda.

    Args:
        event (dict): Dados do evento que acionou a função (ex: EventBridge).
        context (object): Informações do runtime da execução.

    Returns:
        dict: Um dicionário contendo o statusCode e o body da resposta.
    """
    print("Iniciando a execução do pipeline de coleta de dados.")

    try:
        # 1. Extração (Extract)
        print(f"Buscando dados da API: {API_URL}")
        response = requests.get(API_URL, timeout=10)
        # Lança uma exceção se a requisição falhar (ex: status code 4xx ou 5xx)
        response.raise_for_status()
        
        api_data = response.json()
        if not api_data:
            raise ValueError("A resposta da API está vazia.")
            
        latest_quote = api_data[0]
        print(f"Dados recebidos com sucesso: {latest_quote}")

        # 2. Transformação (Transform)
        # Convertendo o valor para float e criando um dicionário mais robusto.
        transformed_data = {
            "data_cotacao": latest_quote.get("data"),
            "valor_cotacao_dolar": float(latest_quote.get("valor")),
            "fonte_dados": "API do Sistema Gerenciador de Séries Temporais (SGS) - Banco Central do Brasil",
            "timestamp_captura_utc": datetime.utcnow().isoformat()
        }
        
        # Converte o dicionário Python para uma string no formato JSON.
        json_output = json.dumps(transformed_data, indent=2)

        # 3. Carregamento (Load)
        # Define um nome de arquivo único baseado na data e hora da captura.
        current_time = datetime.now()
        file_name = f"cotacao-dolar-{current_time.strftime('%Y-%m-%d-%H%M%S')}.json"
        
        print(f"Salvando arquivo '{file_name}' no bucket '{BUCKET_NAME}'...")
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=json_output,
            ContentType='application/json'
        )
        
        print("Arquivo salvo com sucesso no S3.")
        
        # Retorna uma mensagem de sucesso
        return {
            'statusCode': 200,
            'body': json.dumps(f"Processo finalizado com sucesso! Arquivo '{file_name}' criado.")
        }

    except requests.exceptions.RequestException as e:
        print(f"ERRO: Falha ao acessar a API. {e}")
        return {'statusCode': 503, 'body': json.dumps("Erro de comunicação com a API externa.")}
    except (ValueError, KeyError, IndexError) as e:
        print(f"ERRO: Falha no processamento dos dados da API. {e}")
        return {'statusCode': 500, 'body': json.dumps("Erro no formato dos dados recebidos da API.")}
    except Exception as e:
        print(f"ERRO: Ocorreu um erro inesperado. {e}")
        return {'statusCode': 500, 'body': json.dumps("Ocorreu um erro inesperado no servidor.")}
