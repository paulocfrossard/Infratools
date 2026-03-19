# InfraTools - Ponto de entrada principal
# CC BY-NC-SA 4.0
# Create the config.ini file in the executable folder
# Github: https://github.com/paulocfrossard/Infratools/tree/main
# READ readme.md for config

"""
InfraTools - Ferramentas de Infraestrutura
Ponto de entrada principal da aplicação.

Uso:
    python main.py

O aplicativo cria automaticamente arquivos de log com timestamp.
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

import gui


def setup_logging() -> logging.Logger:
    """
    Configura o sistema de logging para console e arquivo.
    Log salvo em: infratools_ddmmyyyy_hhmmss.log
    
    Console mostra apenas INFO e superior.
    Arquivo guarda DEBUG e superior (mais detalhado).
    
    return: Logger configurado
    """
    timestamp = datetime.now().strftime('%d%m%Y_%H%M%S')
    log_filename = f"infratools_{timestamp}.log"
    
    # Cria logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    # Formato das mensagens
    formatter = logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
        datefmt='%d/%m/%Y - %H:%M:%S'
    )
    
    # Handler para arquivo (todos os níveis)
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler para console (apenas INFO e superior)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    logger.debug(f"Arquivo de log criado: {log_filename}")
    return logger


def check_config_file() -> bool:
    """
    Verifica se o arquivo config.ini existe.
    
    return: True se existe, False se não existe
    """
    config_path = Path("config.ini")
    exists = config_path.exists()
    
    logger = logging.getLogger(__name__)
    if exists:
        logger.debug(f"Arquivo config.ini encontrado: {config_path.absolute()}")
    else:
        logger.debug(f"Arquivo config.ini não encontrado em: {config_path.absolute()}")
    
    return exists


def main() -> int:
    """
    Função principal que inicializa a aplicação.
    
    return: Código de saída (0 = sucesso, 1 = erro, 130 = interrompido)
    """
    # Configura logging primeiro
    logger = setup_logging()
    
    try:
        logger.info("=" * 50)
        logger.info("Iniciando InfraTools v2.0.0")
        logger.info("=" * 50)
        logger.debug(f"Diretório atual: {Path.cwd()}")
        logger.debug(f"Python version: {sys.version}")
        
        # Verifica configuração
        if not check_config_file():
            logger.info("⚠️  Aviso: config.ini não encontrado!")
            logger.info("Crie o arquivo na pasta do executável.")
            logger.debug("Verificando README.md para instruções...")
            
            # Pergunta ao usuário via input (mantido para interação)
            response = input("\nDeseja continuar mesmo assim? (s/N): ")
            logger.debug(f"Resposta do usuário: {response}")
            
            if response.lower() != 's':
                logger.info("Aplicação encerrada pelo usuário.")
                return 1
            
            logger.info("Continuando sem arquivo de configuração...")
        
        # Inicia a GUI
        logger.debug("Inicializando interface gráfica...")
        gui.main()
        
        logger.info("Aplicação finalizada com sucesso.")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Aplicação interrompida pelo usuário (Ctrl+C)")
        return 130
        
    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)
        logger.info(f"❌ Erro: {e}")
        logger.info(f"Verifique o arquivo de log para detalhes técnicos.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
