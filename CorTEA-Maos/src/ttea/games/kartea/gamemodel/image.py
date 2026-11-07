import io
from typing import Literal, Tuple, Union

import pygame
from PySide6.QtCore import QFile, QIODevice

from ttea.games.kartea.gameutil.alphablit import alpha_blit
from ttea.games.kartea.util import KarteaPathConfig


class Image:
    """
    Classe utilitária para carregamento, escala e desenho de imagens.
    Suporta caminhos físicos e recursos Qt (.qrc).
    """

    IMAGE_SIZE_DEFAULT_NAME = "default"
    IMAGE_CONVERT_ALPHA = "alpha"
    IMAGE_CONVERT_BASE: str = "base"

    IMAGE_POS_TOP_LEFT = "top_left"
    IMAGE_POS_CENTER = "center"
    IMAGE_POS_BOTTOM_CENTER = "bottom_center"

    @staticmethod
    def load(
        img_name: str,
        size: Union[
            Literal["default"], Tuple[int, int]
        ] = IMAGE_SIZE_DEFAULT_NAME,
        convert: str = IMAGE_CONVERT_ALPHA,
        flip: bool = False,
    ) -> pygame.Surface:
        """Carrega imagem (física ou Qt), aplica conversão, flip e scale."""
        full_path = KarteaPathConfig.game_builtin_image(img_name)

        if (img_name) and (not full_path):
            full_path = img_name

        if not full_path:
            return Image._fallback_surface()

        try:
            # Verificação: Se o caminho for um recurso do Qt
            if full_path.startswith(":/"):
                img = Image._load_from_qt_resource(full_path)
            else:
                # Caminho físico normal
                img = pygame.image.load(full_path)

            # Conversão de pixel format
            if convert == Image.IMAGE_CONVERT_ALPHA:
                img = img.convert_alpha()
            elif convert == Image.IMAGE_CONVERT_BASE:
                img = img.convert()
            else:
                img = img.convert_alpha()

            # Transformações
            if flip:
                img = pygame.transform.flip(img, True, False)

            if size != Image.IMAGE_SIZE_DEFAULT_NAME:
                if isinstance(size, (tuple, list)) and len(size) == 2:
                    img = Image.scale(img, size)

            return img
        except Exception as e:
            print(f"[Image.load] Erro ao carregar '{img_name}': {e}.")
            return Image._fallback_surface()

    @staticmethod
    def _load_from_qt_resource(resource_path: str) -> pygame.Surface:
        """Carrega recurso Qt via QFile."""
        file = QFile(resource_path)
        if not file.open(QIODevice.ReadOnly):
            raise FileNotFoundError(
                f"Não foi possível abrir recurso Qt: {resource_path}."
            )

        img_data = file.readAll().data()
        file.close()
        return pygame.image.load(io.BytesIO(img_data))

    @staticmethod
    def scale(img: pygame.Surface, size: Tuple[int, int]) -> pygame.Surface:
        """Redimensiona com smoothscale e tamanho mínimo seguro."""
        width = max(1, int(size[0]))
        height = max(1, int(size[1]))
        return pygame.transform.smoothscale(img, (width, height))

    @staticmethod
    def draw(
        surface: pygame.Surface,
        img: pygame.Surface,
        pos: Tuple[int, int],
        pos_mode: str = IMAGE_POS_TOP_LEFT,
    ):
        """Desenha a imagem com diferentes modos de ancoragem."""
        if not isinstance(pos, (tuple, list)) or len(pos) != 2:
            raise ValueError(
                "POS deve ser uma tupla/lista com exatamente 2 valores (x, y)."
            )

        render_pos = list(pos)
        mode = pos_mode.lower()

        # TODO verificar se precisa manter o IMAGE_POS_BOTTOM_CENTER
        # no código original não tinha
        if mode == Image.IMAGE_POS_CENTER:
            render_pos[0] -= img.get_width() // 2
            render_pos[1] -= img.get_height() // 2
        elif mode == Image.IMAGE_POS_BOTTOM_CENTER:  # new position mode
            render_pos[0] -= img.get_width() // 2
            render_pos[1] -= img.get_height()

        alpha_blit(surface, img, render_pos)

    @staticmethod
    def _fallback_surface() -> pygame.Surface:
        """Superfície magenta 32x32 para facilitar identificação de imagens faltantes."""
        surf = pygame.Surface((32, 32))
        surf.fill((255, 0, 255))
        return surf
