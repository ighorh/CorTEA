"""Gera o ícone do CorTEA (``CorTea.ico`` e ``CorTea.png``).

Usa o mesmo desenho do fundo da tela inicial (``FundoInicio``): o tabuleiro
de blocos em 3D, visto mais de cima para caber num quadrado, num instante
em que parte do caminho já foi percorrida e o próximo bloco sobe aceso.
Não tem texto, para continuar legível em tamanhos pequenos.

Uso, na raiz do projeto::

    uv run python src/ttea/games/CorTEA/resources/icons/gerar_icone.py
"""

import io
import os
import struct

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame  # noqa: E402
from ttea.games.CorTEA.gameview.fundoinicio import FundoInicio  # noqa: E402

PASTA = os.path.dirname(os.path.abspath(__file__))
TAM_BASE = 512  # desenhado grande e reduzido depois (bordas suaves)
TAMANHOS = [256, 128, 64, 48, 32, 16]


class FundoIcone(FundoInicio):
    """Câmera mais alta e mais perto: o tabuleiro preenche o quadrado."""

    FOCO = 330
    ALTURA_CAMERA = 6.0
    HORIZONTE = -200


def desenhar() -> pygame.Surface:
    base = pygame.Surface((TAM_BASE, TAM_BASE))
    fundo = FundoIcone(base)
    # 1º caminho, no meio do 3º passo: dois blocos percorridos (borda
    # dourada) e o terceiro subindo com brilho.
    fundo.draw(2 * FundoInicio.PASSO_MS + int(FundoInicio.PASSO_MS * 0.3))

    # Cantos arredondados (fundo transparente fora deles)
    icone = pygame.Surface((TAM_BASE, TAM_BASE), pygame.SRCALPHA)
    mascara = pygame.Surface((TAM_BASE, TAM_BASE), pygame.SRCALPHA)
    pygame.draw.rect(
        mascara, (255, 255, 255, 255), mascara.get_rect(), border_radius=96
    )
    icone.blit(base, (0, 0))
    icone.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    return icone


def png_bytes(surface: pygame.Surface) -> bytes:
    arquivo = io.BytesIO()
    pygame.image.save(surface, arquivo, "icone.png")
    return arquivo.getvalue()


def salvar_ico(imagens, caminho: str) -> None:
    """ICO com uma imagem PNG por tamanho (formato aceito pelo Windows e
    pelo Qt)."""
    cabecalho = struct.pack("<HHH", 0, 1, len(imagens))
    deslocamento = 6 + 16 * len(imagens)
    entradas, dados = b"", b""
    for tamanho, png in imagens:
        lado = 0 if tamanho >= 256 else tamanho  # 0 significa 256
        entradas += struct.pack(
            "<BBBBHHII", lado, lado, 0, 0, 1, 32, len(png), deslocamento
        )
        dados += png
        deslocamento += len(png)
    with open(caminho, "wb") as f:
        f.write(cabecalho + entradas + dados)


def main() -> None:
    pygame.init()
    pygame.display.set_mode((1, 1))
    grande = desenhar()
    imagens = [
        (t, png_bytes(pygame.transform.smoothscale(grande, (t, t))))
        for t in TAMANHOS
    ]
    salvar_ico(imagens, os.path.join(PASTA, "CorTea.ico"))
    with open(os.path.join(PASTA, "CorTea.png"), "wb") as f:
        f.write(imagens[0][1])  # 256x256, usado como ícone da janela
    pygame.quit()
    print("Ícones gerados em", PASTA)


if __name__ == "__main__":
    main()
