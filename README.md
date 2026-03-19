# InfraTools

Aplicativo de ferramentas de infraestrutura com interface moderna em Material Design.

## 🚀 Características

- **Interface Moderna**: Design Material com suporte a tema escuro/claro
- **8 Funcionalidades**: Recuperação, Diagnóstico de Rede, Renovação de IP, Info do Sistema, Teste de Velocidade, Verificação de Serviços, Limpeza de Temp e Sobre
- **Execução em Background**: Operações não travam a interface
- **Diálogos Customizáveis**: Sistema de diálogos genéricos com botões configuráveis
- **Fácil Manutenção**: Código organizado e comentado para desenvolvedores juniores

## Requisitos

- Python 3.8 ou superior
- Windows 10/11

## Instalação

### 1. Criar ambiente virtual (recomendado)

```bash
python -m venv venv
```

### 2. Ativar ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

## Uso

### Configurar hosts e domínio

Crie um arquivo `config.ini` na mesma pasta do executável:

```ini
[hosts]
ips = 8.8.8.8, 1.1.1.1, 192.168.1.1

[domain]
name = seu-dominio.local
```

## 📁 Estrutura do Projeto

```
Infratools/
├── main.py              # Ponto de entrada
├── gui.py              # Interface principal (nova versão Material)
├── requirements.txt    # Dependências
├── config.ini         # Configuração (criar manualmente)
├── tools/
│   ├── get_ip.py     # Funções de rede
│   ├── network.py    # Ping e renovação de IP
│   ├── cmd_commands.py # Execução de comandos
│   ├── recovery.py   # Recuperação do sistema
│   └── formart.py    # Formatação de dados
└── img/              # Imagens e ícones
```

### Exemplo de diálogo customizável:

```python
from gui import MaterialDialog

# Diálogo simples
MaterialDialog.show_dialog(
    "Sucesso",
    "Operação concluída!",
    ["OK"]
)

# Diálogo de confirmação
resultado = MaterialDialog.show_dialog(
    "Confirmação",
    "Deseja continuar?",
    ["Sim", "Não"],
    "question"
)

if resultado == "Sim":
    print("Usuário confirmou")
```

## 📄 Licença

Este projeto está licenciado sob CC BY-NC-SA 4.0 - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Créditos

- **qt-material**: Biblioteca de Material Design para PySide6 (BSD-2-Clause)
- **PySide6**: Framework Qt para Python

## 📞 Suporte

Para dúvidas ou problemas, consulte:
- GitHub: https://github.com/paulocfrossard/Infratools
- Documentação: README.md

---

**Nota**: Este software é fornecido como está, sem garantias. Use por sua conta e risco.
