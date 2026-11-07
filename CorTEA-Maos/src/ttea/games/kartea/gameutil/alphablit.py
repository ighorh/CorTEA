import sys

import pygame


def alpha_blit_flags() -> int:
    """Use SDL2's alpha blitter on macOS and preserve defaults elsewhere."""
    if sys.platform == "darwin":
        return pygame.BLEND_ALPHA_SDL2
    return 0


def alpha_blit(
    destination: pygame.Surface,
    source: pygame.Surface,
    position,
) -> pygame.Rect:
    """Blit a per-pixel-alpha surface using the platform-safe blend path."""
    return destination.blit(
        source,
        position,
        special_flags=alpha_blit_flags(),
    )
