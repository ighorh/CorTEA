from typing import TYPE_CHECKING

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

if TYPE_CHECKING:
    from ttea.model import AppModel
    from ttea.util import MessageService


class MainService:
    """Serviço global da aplicação principal (saída, futuras funcionalidades globais)"""

    def __init__(self, model: "AppModel", message_service: "MessageService"):
        self.model = model
        self.msg = message_service

    def confirm_exit(self) -> bool:
        """Pergunta ao usuário se deseja realmente sair"""

        return self.msg.question(
            text=QCoreApplication.translate(
                "MainService", "Deseja sair do sistema?"
            ),
            title=QCoreApplication.translate(
                "MainService", "Plataforma T-TEA"
            ),
            default_no=True,
        )

    def quit_application(self) -> None:
        QApplication.quit()
