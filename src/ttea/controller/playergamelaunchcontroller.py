import os
import subprocess
import sys
from datetime import datetime
from typing import TYPE_CHECKING, Optional

# Import opcional do psutil (não quebra o programa se não estiver instalado)
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

from PySide6.QtCore import QObject, Qt, QTimer

from ttea.model import AppModel
from ttea.service import PlayerGameLaunchService
# Local module imports
from ttea.util import MessageService

if TYPE_CHECKING:
    from ttea.view import PlayerGameLaunchView


class PlayerGameLaunchController(QObject):

    def __init__(
        self,
        view: "PlayerGameLaunchView",
        message_service: Optional[MessageService] = None,
        service: Optional[PlayerGameLaunchService] = None,
    ):
        super().__init__()
        self.view = view
        self.msg = message_service or MessageService(view)
        self.service = service or PlayerGameLaunchService()
        self.current_process: Optional[subprocess.Popen] = None
        self.monitor_timer: Optional[QTimer] = None

    def handle_cancel(self) -> None:
        """Trata o clique no botão Cancelar baseado no estado do jogo."""
        if self.is_game_running():
            if self.msg.question(
                self.tr(
                    "Existe um jogo em execução, ele será finalizado. Deseja sair da tela de sessão de jogo?"
                ),
                None,
                True,
            ):
                self.view.reject()
            else:
                return
        else:
            self.view.reject()

    def handle_game_info(self) -> None:
        game_data = self.view.cbx_game.currentData()

        if (
            game_data.get("authors") is not None
            and game_data.get("version") is not None
            and game_data.get("since") is not None
        ):
            self.msg.info(
                self.tr(
                    "Este jogo foi desenvolvido por:\n\n{0}\n\n"
                    "Versão: {1}\n"
                    "Desde: {2} - {3}"
                ).format(
                    "\n".join(game_data.get("authors", [])),
                    game_data.get("version", "N/A"),
                    game_data.get("since", "N/A"),
                    datetime.now().strftime("%Y"),
                )
            )
        else:
            self.msg.warning(
                self.tr(
                    "Informações de autoria do jogo não estão disponíveis.\n"
                    "Verifique se os metadados de configuração estão corretos."
                )
            )

    def launch_game(self):
        """Valida e inicia o processo do jogo selecionado."""
        game_data = self.view.cbx_game.currentData()
        player_id = str(self.view.cbx_player.currentData())
        professional_id = str(self.view.cbx_professional.currentData())

        language_app = AppModel.get_instance().current_language

        if not game_data:
            self.msg.warning(self.tr("Selecione um jogo antes de iniciar."))
            return

        if self.is_game_running():
            self.msg.warning(
                self.tr(
                    "Já existe um jogo em execução.\n"
                    "Feche o jogo atual antes de iniciar outro."
                )
            )
            return

        folder = game_data["folder_path"]
        executable = game_data.get("exec")
        script_path = os.path.join(folder, executable)

        if not os.path.exists(script_path):
            self.msg.critical(
                self.tr(
                    "Erro: Executável do jogo não encontrado em: {0}.\n"
                    "Verifique se o arquivo existe e se os metadados de configuração estão corretos."
                ).format(script_path)
            )
            return

        ext = os.path.splitext(executable.lower())[1] if executable else ""
        if ext in (".py", ".pyw"):
            cmd = [
                sys.executable,
                script_path,
                "--lang",
                language_app,
                "--player_id",
                player_id,
                "--professional_id",
                professional_id,
            ]
        else:
            cmd = [
                script_path,
                "--lang",
                language_app,
                "--player_id",
                player_id,
                "--professional_id",
                professional_id,
            ]

        # UX: desabilita botões durante o lançamento
        self.view.pb_play.setEnabled(False)
        self.view.pb_cancel.setEnabled(False)
        self.view.pb_play.setText(self.tr("Espere"))
        self.view.repaint()

        # Cria um novo grupo de processos (melhora o controle da árvore no Windows)
        creationflags = (
            subprocess.CREATE_NEW_PROCESS_GROUP
            if sys.platform.startswith("win")
            else 0
        )

        # Inicia o processo do jogo
        self.current_process = subprocess.Popen(
            cmd, cwd=folder, creationflags=creationflags
        )

        # Monitora quando o jogo realmente abre a janela
        self.monitor_timer = QTimer(self)
        self.monitor_timer.timeout.connect(self._check_if_game_is_visible)
        self.monitor_timer.start(500)

        # Proteção contra falha no lançamento
        QTimer.singleShot(7000, self._restore_buttons_after_timeout)

    def _restore_buttons_after_timeout(self) -> None:
        """Garante que a interface seja liberada após o tempo limite."""
        if self.monitor_timer and self.monitor_timer.isActive():
            self.monitor_timer.stop()
            self._restore_buttons_state()

    def is_game_running(self) -> bool:
        """Retorna True se existe um jogo realmente em execução."""
        return bool(
            self.current_process and self.current_process.poll() is None
        )

    def _check_if_game_is_visible(self) -> None:
        """Verifica se o processo do jogo já abriu uma janela gráfica."""
        if not self.current_process or self.current_process.poll() is not None:
            if self.monitor_timer and self.monitor_timer.isActive():
                self.monitor_timer.stop()
            self._restore_buttons_state()
            return

        if not PSUTIL_AVAILABLE:
            # Sem psutil, liberamos os botões imediatamente para o usuário
            # já que não temos como monitorar o estado das threads.
            self._game_ready()
            return

        try:
            parent = psutil.Process(self.current_process.pid)
            processes = [parent] + parent.children(recursive=True)

            for proc in processes:
                if sys.platform.startswith("win"):
                    if (
                        proc.num_threads() > 1
                        and proc.status() == psutil.STATUS_RUNNING
                    ):
                        self._game_ready()
                        return
                else:
                    if proc.status() in (
                        psutil.STATUS_RUNNING,
                        psutil.STATUS_SLEEPING,
                    ):
                        self._game_ready()
                        return
        except Exception:
            pass  # fallback silencioso

    def _game_ready(self) -> None:
        """Chamado quando o jogo está pronto (janela visível)."""
        if self.monitor_timer and self.monitor_timer.isActive():
            self.monitor_timer.stop()
        self._restore_buttons_state()

    def _restore_buttons_state(self) -> None:
        """Restaura o estado original dos botões da interface."""
        self.view.pb_play.setText(self.tr("Jogar"))
        self.view.pb_play.setEnabled(True)
        self.view.pb_cancel.setEnabled(True)

    def update_tooltip(self, index):
        """Atualiza o tooltip do combobox quando o jogo selecionado muda."""
        if index >= 0:
            novo_hint = self.view.cbx_game.itemData(
                index, Qt.ItemDataRole.ToolTipRole
            )
            self.view.cbx_game.setToolTip(novo_hint)

    def cleanup(self) -> None:
        """Encerra o jogo e todos os seus processos filhos quando a janela é fechada."""
        if not self.is_game_running():
            # Limpeza final mesmo sem processo rodando
            if self.monitor_timer and self.monitor_timer.isActive():
                self.monitor_timer.stop()
            self.current_process = None
            self._restore_buttons_state()
            return

        try:
            if PSUTIL_AVAILABLE:
                parent = psutil.Process(self.current_process.pid)
                children = parent.children(recursive=True)

                # Tenta encerramento gracioso
                for child in children:
                    child.terminate()
                parent.terminate()

                # Aguarda
                _, alive = psutil.wait_procs(children + [parent], timeout=2.0)

                # Força kill no que sobrar
                for survivor in alive:
                    survivor.kill()
            else:
                # Fallback sem psutil
                self.current_process.terminate()
                self.current_process.wait(timeout=2.0)

        except Exception:
            try:
                self.current_process.kill()
            except Exception:
                pass

        finally:
            if self.monitor_timer and self.monitor_timer.isActive():
                self.monitor_timer.stop()
            self.current_process = None
            self._restore_buttons_state()
