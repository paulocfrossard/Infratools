"""
InfraTools - Interface GUI com Material Design
Aplicativo de ferramentas de infraestrutura com interface moderna.

Autor: Infratools Team
Licença: MIT
"""

import sys
import os
import subprocess
from datetime import datetime
from typing import Optional, List, Dict, Any, Callable
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame, QDialog,
    QDialogButtonBox, QScrollArea, QGridLayout, QSizePolicy,
    QMessageBox, QTextEdit, QProgressBar, QSplitter
)
from PySide6.QtCore import Qt, QSize, QThreadPool, QRunnable, Slot, Signal, QObject
from PySide6.QtGui import QFont, QIcon, QPalette, QColor

# Biblioteca Material Design - BSD License (comercial permitido)
from qt_material import apply_stylesheet

# Imports locais
from tools.get_ip import get_network_devices
from tools.network import ip_refresh, internal_dns_status


# ============================================================
# CONFIGURAÇÕES GLOBAIS
# ============================================================

# Cores do Material Design
COLORS = {
    "primary": "#1976d2",
    "primary_dark": "#115293",
    "primary_light": "#4791db",
    "accent": "#ff4081",
    "success": "#4caf50",
    "warning": "#ff9800",
    "error": "#f44336",
    "info": "#2196f3"
}

# Dimensões da janela
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700
SIDEBAR_WIDTH = 250


# ============================================================
# CLASSE PARA EXECUÇÃO EM THREAD
# ============================================================

class WorkerSignals(QObject):
    """Sinais para comunicação entre thread e GUI."""
    finished = Signal()
    error = Signal(str)
    result = Signal(object)
    progress = Signal(int)


class Worker(QRunnable):
    """
    Classe para executar funções em background sem travar a GUI.
    
    parm: fn: Função a ser executada
    parm: args: Argumentos posicionais da função
    parm: kwargs: Argumentos nomeados da função
    """
    
    def __init__(self, fn: Callable, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
    
    @Slot()
    def run(self) -> None:
        """Executa a função em thread separada."""
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.signals.result.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self.signals.finished.emit()


# ============================================================
# DIÁLOGO GENÉRICO CUSTOMIZÁVEL
# ============================================================

class MaterialDialog(QDialog):
    """
    Diálogo genérico estilo Material Design.
    Pode ter botões customizáveis: ["OK"], ["Sim", "Não"], ["Sim", "Não", "Cancelar"]
    
    parm: title: Título da janela
    parm: description: Mensagem/descrição
    parm: buttons: Lista de textos dos botões
    parm: icon_type: Tipo do ícone (info, warning, error, success, question)
    parm: parent: Widget pai (opcional)
    
    return: Nome do botão clicado (str)
    
    Exemplo:
        resultado = MaterialDialog.show_dialog(
            "Confirmação",
            "Deseja continuar?",
            ["Sim", "Não"],
            "question"
        )
    """
    
    def __init__(
        self,
        title: str,
        description: str,
        buttons: List[str],
        icon_type: str = "info",
        parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        
        self.title = title
        self.description = description
        self.buttons = buttons
        self.icon_type = icon_type
        self.result_button = ""
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Configura a interface do diálogo."""
        self.setWindowTitle(self.title)
        self.setMinimumSize(400, 200)
        self.setMaximumSize(600, 400)
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Ícone
        icon_label = QLabel(self._get_icon_text())
        icon_label.setAlignment(Qt.AlignCenter)
        icon_font = QFont("Segoe UI Emoji", 48)
        icon_label.setFont(icon_font)
        layout.addWidget(icon_label)
        
        # Título
        title_label = QLabel(self.title)
        title_font = QFont("Segoe UI", 16, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Descrição
        desc_label = QLabel(self.description)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)
        
        # Espaçador
        layout.addStretch()
        
        # Botões
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        for button_text in self.buttons:
            btn = QPushButton(button_text)
            btn.setMinimumSize(100, 36)
            btn.clicked.connect(lambda checked, text=button_text: self._on_button_click(text))
            
            # Botão primário (primeiro da lista) tem estilo diferente
            if button_text == self.buttons[0]:
                btn.setObjectName("primaryButton")
            
            button_layout.addWidget(btn)
        
        layout.addLayout(button_layout)
    
    def _get_icon_text(self) -> str:
        """Retorna o emoji do ícone baseado no tipo."""
        icons = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "success": "✅",
            "question": "❓"
        }
        return icons.get(self.icon_type, "ℹ️")
    
    def _on_button_click(self, button_text: str) -> None:
        """Callback quando um botão é clicado."""
        self.result_button = button_text
        self.accept()
    
    @staticmethod
    def show_dialog(
        title: str,
        description: str,
        buttons: List[str] = None,
        icon_type: str = "info",
        parent: Optional[QWidget] = None
    ) -> str:
        """
        Método estático para exibir o diálogo de forma simples.
        
        parm: title: Título da janela
        parm: description: Mensagem a ser exibida
        parm: buttons: Lista de botões (padrão: ["OK"])
        parm: icon_type: Tipo do ícone
        parm: parent: Widget pai
        
        return: Texto do botão clicado
        """
        if buttons is None:
            buttons = ["OK"]
        
        dialog = MaterialDialog(title, description, buttons, icon_type, parent)
        dialog.exec()
        return dialog.result_button


# ============================================================
# CARD DE STATUS
# ============================================================

class StatusCard(QFrame):
    """
    Card para exibir informações de status.
    
    parm: title: Título do card
    parm: value: Valor a ser exibido
    parm: status: Status (success, warning, error, info)
    parm: parent: Widget pai
    """
    
    def __init__(
        self,
        title: str,
        value: str,
        status: str = "info",
        parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        
        self.title = title
        self.value = value
        self.status = status
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Configura a interface do card."""
        self.setFrameStyle(QFrame.StyledPanel)
        self.setMinimumSize(200, 100)
        self.setMaximumHeight(120)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Título
        title_label = QLabel(self.title)
        title_font = QFont("Segoe UI", 10)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Valor
        value_label = QLabel(self.value)
        value_font = QFont("Segoe UI", 14, QFont.Bold)
        value_label.setFont(value_font)
        layout.addWidget(value_label)
        
        # Cor de acordo com o status
        colors = {
            "success": COLORS["success"],
            "warning": COLORS["warning"],
            "error": COLORS["error"],
            "info": COLORS["info"]
        }
        color = colors.get(self.status, COLORS["info"])
        value_label.setStyleSheet(f"color: {color};")
    
    def update_value(self, value: str, status: str = None) -> None:
        """
        Atualiza o valor exibido no card.
        
        parm: value: Novo valor
        parm: status: Novo status (opcional)
        """
        # Atualiza o valor
        self.value = value
        if status:
            self.status = status
        
        # Recria o card
        # Limpa o layout atual
        while self.layout().count():
            child = self.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self._setup_ui()


# ============================================================
# BOTÃO DA SIDEBAR
# ============================================================

class SidebarButton(QPushButton):
    """
    Botão estilizado para a barra lateral.
    
    parm: text: Texto do botão
    parm: icon: Ícone (emoji ou texto)
    parm: parent: Widget pai
    """
    
    def __init__(self, text: str, icon: str = "", parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        self.setText(f"{icon}  {text}" if icon else text)
        self.setMinimumHeight(48)
        self.setMaximumHeight(48)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        
        # Fonte
        font = QFont("Segoe UI", 11)
        self.setFont(font)
        
        # Alinhamento do texto à esquerda
        self.setStyleSheet("text-align: left; padding-left: 16px;")


# ============================================================
# PÁGINAS DE CONTEÚDO
# ============================================================

class RecoveryPage(QWidget):
    """Página de Recuperação do Sistema."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Configura a interface da página."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Título
        title = QLabel("Recuperação do Sistema")
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Descrição
        desc = QLabel("Executa DISM, SFC e CHKDSK para reparar o sistema.")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Botão de ação
        self.btn_recovery = QPushButton("Iniciar Recuperação e restauração")
        self.btn_recovery.setMinimumHeight(48)
        self.btn_recovery.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.btn_recovery)
        
        # Área de status
        self.status_label = QLabel("Clique no botão acima para iniciar.")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # Log
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setPlaceholderText("Log de execução...")
        self.log_text.setMaximumHeight(200)
        layout.addWidget(self.log_text)
        
        # Espaçador
        layout.addStretch()


class NetworkPage(QWidget):
    """Página de Diagnóstico de Rede."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Configura a interface da página."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Título
        title = QLabel("Diagnóstico de Rede")
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Grid com cards de informação
        cards_layout = QGridLayout()
        cards_layout.setSpacing(16)
        
        # Obtém informações de rede
        try:
            ip, mac = get_network_devices()
        except:
            ip, mac = "N/A", "N/A"
        
        self.card_ip = StatusCard("Endereço IP", ip, "info")
        self.card_mac = StatusCard("Endereço MAC", mac, "info")
        
        cards_layout.addWidget(self.card_ip, 0, 0)
        cards_layout.addWidget(self.card_mac, 0, 1)
        
        layout.addLayout(cards_layout)
        
        # Botão de ping
        self.btn_ping = QPushButton("🌐 Testar Conectividade")
        self.btn_ping.setMinimumHeight(48)
        self.btn_ping.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.btn_ping)
        
        # Resultados
        self.results_label = QLabel("Resultados aparecerão aqui...")
        self.results_label.setWordWrap(True)
        layout.addWidget(self.results_label)
        
        # Espaçador
        layout.addStretch()


class IpRenewPage(QWidget):
    """Página de Renovação de IP."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Configura a interface da página."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Título
        title = QLabel("Renovar IP")
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Descrição
        desc = QLabel("Libera o IP atual e solicita um novo do servidor DHCP.")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Cards
        cards_layout = QHBoxLayout()
        
        try:
            ip, _ = get_network_devices()
        except:
            ip = "N/A"
        
        self.card_current = StatusCard("IP Atual", ip, "info")
        self.card_new = StatusCard("Novo IP", "Aguardando...", "warning")
        
        cards_layout.addWidget(self.card_current)
        cards_layout.addWidget(self.card_new)
        
        layout.addLayout(cards_layout)
        
        # Botão
        self.btn_renew = QPushButton("🔄 Renovar Endereço IP")
        self.btn_renew.setMinimumHeight(48)
        self.btn_renew.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.btn_renew)
        
        # Status
        self.status_label = QLabel("Clique no botão para renovar o IP.")
        layout.addWidget(self.status_label)
        
        # Espaçador
        layout.addStretch()


class SystemInfoPage(QWidget):
    """Página de Informações do Sistema."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Configura a interface da página."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Título
        title = QLabel("Informações do Sistema")
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Grid de cards
        grid = QGridLayout()
        grid.setSpacing(16)
        
        # Cards de informação
        self.card_os = StatusCard("Sistema Operacional", "Detectando...", "info")
        self.card_cpu = StatusCard("Processador", "Detectando...", "info")
        self.card_ram = StatusCard("Memória RAM", "Detectando...", "info")
        self.card_disk = StatusCard("Disco", "Detectando...", "info")
        
        grid.addWidget(self.card_os, 0, 0)
        grid.addWidget(self.card_cpu, 0, 1)
        grid.addWidget(self.card_ram, 1, 0)
        grid.addWidget(self.card_disk, 1, 1)
        
        layout.addLayout(grid)
        
        # Botão de atualizar
        self.btn_refresh = QPushButton("🔄 Atualizar Informações")
        self.btn_refresh.setMinimumHeight(48)
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.btn_refresh)
        
        # Espaçador
        layout.addStretch()


class ServicesPage(QWidget):
    """Página de Verificação de Serviços."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Configura a interface da página."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Título
        title = QLabel("Verificar Serviços")
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Descrição
        desc = QLabel("Verifica o status dos serviços críticos do sistema.")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Lista de serviços (placeholder)
        self.services_list = QTextEdit()
        self.services_list.setReadOnly(True)
        self.services_list.setPlaceholderText("Serviços serão listados aqui...")
        layout.addWidget(self.services_list)
        
        # Botão
        self.btn_check = QPushButton("🔍 Verificar Serviços")
        self.btn_check.setMinimumHeight(48)
        self.btn_check.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.btn_check)
        
        # Espaçador
        layout.addStretch()


class TerminalPage(QWidget):
    """Página de Terminal com comandos e saída."""
    
    COMMANDS = [
        ("ipconfig", "ipconfig"),
        ("ipconfig /all", "ipconfig /all"),
        ("ping localhost", "ping localhost"),
        ("ping 8.8.8.8", "ping 8.8.8.8"),
        ("netstat -an", "netstat -an"),
        ("tracert google.com", "tracert google.com"),
        ("systeminfo", "systeminfo"),
        ("ipconfig /flushdns", "ipconfig /flushdns"),
    ]
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.command_buttons = []
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Configura a interface da página."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(24, 24, 24, 24)
        
        title = QLabel("Terminal")
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        splitter = QSplitter(Qt.Horizontal)
        
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)
        
        for label, cmd in self.COMMANDS:
            btn = QPushButton(label)
            btn.setMinimumHeight(40)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, c=cmd: self._run_command(c))
            self.command_buttons.append(btn)
            left_layout.addWidget(btn)
        
        left_layout.addStretch()
        
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        header = QHBoxLayout()
        header.addWidget(QLabel("Saída:"))
        header.addStretch()
        
        btn_clear = QPushButton("Limpar")
        btn_clear.setMaximumWidth(80)
        btn_clear.clicked.connect(self._clear_terminal)
        header.addWidget(btn_clear)
        
        right_layout.addLayout(header)
        
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("""
            QTextEdit {
                background-color: #0c0c0c;
                color: #00ff00;
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }
        """)
        right_layout.addWidget(self.terminal)
        
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([250, 500])
        
        main_layout.addWidget(splitter)
    
    def _set_buttons_enabled(self, enabled: bool) -> None:
        """ habilita/desabilita botões durante execução."""
        for btn in self.command_buttons:
            btn.setEnabled(enabled)
    
    def _clear_terminal(self) -> None:
        """Limpa o terminal."""
        self.terminal.clear()
    
    def _log(self, msg: str, color: str = "#00ff00") -> None:
        """Adiciona mensagem ao terminal com cor opcional."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.terminal.append(f'<span style="color: #666;">[{timestamp}]</span> <span style="color: {color};">{msg}</span>')
        self.terminal.verticalScrollBar().setValue(self.terminal.verticalScrollBar().maximum())
    
    def _execute_subprocess(self, command: str) -> tuple:
        """Executa o comando em thread separada."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return (command, result.stdout or result.stderr, result.returncode)
        except subprocess.TimeoutExpired:
            return (command, "[Timeout]", 124)
        except Exception as e:
            return (command, f"[Erro: {e}]", 1)
    
    def _run_command(self, command: str) -> None:
        """Executa um comando usando Worker para não travar a GUI."""
        self._log(f"Executando: {command}", "#ffeb3b")
        
        self._set_buttons_enabled(False)
        self.setCursor(Qt.WaitCursor)
        
        worker = Worker(self._execute_subprocess, command)
        worker.signals.result.connect(self._on_command_finished)
        worker.signals.error.connect(self._on_command_error)
        QThreadPool.globalInstance().start(worker)
    
    def _on_command_finished(self, data: tuple) -> None:
        """Callback quando o comando termina."""
        command, output, returncode = data
        
        self.terminal.append(f'\n<span style="color: #00d4ff;">> {command}</span>')
        self.terminal.append(output)
        
        color = "#4caf50" if returncode == 0 else "#f44336"
        self._log(f"Concluído (código: {returncode})", color)
        
        self._set_buttons_enabled(True)
        self.unsetCursor()
    
    def _on_command_error(self, error: str) -> None:
        """Callback quando ocorre erro no worker."""
        self._log(f"Erro: {error}", "#f44336")
        
        self._set_buttons_enabled(True)
        self.unsetCursor()


class CleanTempPage(QWidget):
    """Página de Limpeza de Arquivos Temporários."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Configura a interface da página."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Título
        title = QLabel("Limpar Arquivos Temporários")
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Descrição
        desc = QLabel("Remove arquivos temporários para liberar espaço em disco.")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Cards
        cards_layout = QHBoxLayout()
        
        self.card_space = StatusCard("Espaço a Liberar", "0 MB", "info")
        self.card_files = StatusCard("Arquivos", "0", "info")
        
        cards_layout.addWidget(self.card_space)
        cards_layout.addWidget(self.card_files)
        
        layout.addLayout(cards_layout)
        
        # Botão
        self.btn_clean = QPushButton("🧹 Limpar Arquivos Temporários")
        self.btn_clean.setMinimumHeight(48)
        self.btn_clean.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.btn_clean)
        
        # Espaçador
        layout.addStretch()


class AboutPage(QWidget):
    """Página Sobre."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Configura a interface da página."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Título
        title = QLabel("Sobre")
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Informações
        info = QLabel("""
        <h2>InfraTools</h2>
        <p>Ferramentas de infraestrutura para diagnóstico e manutenção de sistemas.</p>
        <p><b>Versão:</b> 2.0.0</p>
        <p><b>Autor:</b> Infratools Team</p>
        <p><b>Licença:</b> MIT</p>
        <p>Este software é distribuído gratuitamente e pode ser usado para fins comerciais.</p>
        """)
        info.setWordWrap(True)
        info.setTextFormat(Qt.RichText)
        layout.addWidget(info)
        
        # Botão de licença
        self.btn_license = QPushButton("📄 Ver Licença")
        self.btn_license.setMinimumHeight(48)
        self.btn_license.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.btn_license)
        
        # Espaçador
        layout.addStretch()


# ============================================================
# JANELA PRINCIPAL
# ============================================================

class MainWindow(QMainWindow):
    """
    Janela principal do aplicativo InfraTools.
    
    Gerencia a sidebar, navegação entre páginas e tema do sistema.
    """
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("InfraTools")
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMaximumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Pool de threads para execuções em background
        self.thread_pool = QThreadPool()
        
        self._setup_ui()
        self._apply_theme()
    
    def _setup_ui(self) -> None:
        """Configura a interface principal."""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal horizontal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar
        self.sidebar = self._create_sidebar()
        self.sidebar.setFixedWidth(SIDEBAR_WIDTH)
        main_layout.addWidget(self.sidebar)
        
        # Separador visual
        separator = QFrame()
        separator.setFrameStyle(QFrame.VLine)
        separator.setFixedWidth(1)
        main_layout.addWidget(separator)
        
        # Área de conteúdo (StackedWidget)
        self.content_area = self._create_content_area()
        main_layout.addWidget(self.content_area)
    
    def _create_sidebar(self) -> QWidget:
        """Cria a barra lateral com os botões de navegação."""
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        
        layout = QVBoxLayout(sidebar)
        layout.setSpacing(4)
        layout.setContentsMargins(12, 24, 12, 24)
        
        # Logo/Título
        title = QLabel("InfraTools - rápido e fácil")
        title_font = QFont("Segoe UI", 18, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Espaçador
        layout.addSpacing(24)
        
        # Botões do menu
        self.buttons = []
        
        menu_items = [
            ("Recuperação", "🔧", 0),
            ("Diagnóstico Rede", "🌐", 1),
            ("Renovar IP", "🔄", 2),
            ("Info Sistema", "💻", 3),
            ("Terminal", "⌨️", 4),
            ("Verificar Serviços", "🔍", 5),
            ("Limpar Temp", "🧹", 6),
            ("Sobre", "ℹ️", 7)
        ]
        
        for text, icon, index in menu_items:
            btn = SidebarButton(text, icon)
            btn.clicked.connect(lambda checked, i=index: self._change_page(i))
            self.buttons.append(btn)
            layout.addWidget(btn)
        
        # Seleciona o primeiro botão
        self.buttons[0].setChecked(True)
        
        # Espaçador no final
        layout.addStretch()
        
        return sidebar
    
    def _create_content_area(self) -> QStackedWidget:
        """Cria a área de conteúdo com as páginas."""
        stacked = QStackedWidget()
        
        # Cria as páginas
        self.pages = [
            RecoveryPage(),
            NetworkPage(),
            IpRenewPage(),
            SystemInfoPage(),
            TerminalPage(),
            ServicesPage(),
            CleanTempPage(),
            AboutPage()
        ]
        
        # Adiciona ao stacked widget
        for page in self.pages:
            stacked.addWidget(page)
        
        return stacked
    
    def _change_page(self, index: int) -> None:
        """
        Muda para a página selecionada.
        
        parm: index: Índice da página
        """
        # Atualiza o botão selecionado
        for i, btn in enumerate(self.buttons):
            btn.setChecked(i == index)
        
        # Muda a página
        self.content_area.setCurrentIndex(index)
    
    def _apply_theme(self) -> None:
        """Aplica o tema Material Design baseado no tema do Windows."""
        # Detecta se o Windows está em modo escuro
        is_dark = self._is_windows_dark_mode()
        
        # Aplica o tema qt-material
        if is_dark:
            apply_stylesheet(QApplication.instance(), theme='dark_blue.xml')
        else:
            apply_stylesheet(QApplication.instance(), theme='light_blue.xml')
    
    def _is_windows_dark_mode(self) -> bool:
        """
        Detecta se o Windows está usando tema escuro.
        
        return: True se modo escuro, False se modo claro
        """
        try:
            # Tenta detectar via registro do Windows
            import winreg
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            # Se AppsUseLightTheme for 0, está em modo escuro
            return value == 0
        except:
            # Se não conseguir detectar, assume modo claro
            return False
    
    def run_in_thread(self, func: Callable, callback: Callable = None, error_callback: Callable = None) -> None:
        """
        Executa uma função em thread separada.
        
        parm: func: Função a ser executada
        parm: callback: Callback para resultado (opcional)
        parm: error_callback: Callback para erro (opcional)
        """
        worker = Worker(func)
        
        if callback:
            worker.signals.result.connect(callback)
        
        if error_callback:
            worker.signals.error.connect(error_callback)
        
        self.thread_pool.start(worker)


# ============================================================
# FUNÇÃO DE INICIALIZAÇÃO
# ============================================================

def create_application() -> QApplication:
    """
    Cria e configura a aplicação Qt.
    
    return: Instância de QApplication configurada
    """
    app = QApplication(sys.argv)
    
    # Configura fonte padrão
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    return app


def main():
    """
    Função principal de inicialização.
    Cria a aplicação e exibe a janela principal.
    """
    # Cria a aplicação
    app = create_application()
    
    # Cria a janela principal
    window = MainWindow()
    window.show()
    
    # Executa o loop de eventos
    sys.exit(app.exec())


# ============================================================
# PONTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    main()
