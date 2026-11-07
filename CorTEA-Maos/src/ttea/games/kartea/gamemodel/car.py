import pygame

# import arquivo
from ttea.games.kartea.gameutil import GameSettings


class Car:
    """Classe que representa o carro controlado pelo jogador (posição dos pés
    via MediaPipe)."""

    def __init__(self):
        # Carrega a imagem principal do carro
        from ttea.games.kartea.gamemodel import Image

        self.orig_image = Image.load(
            # "Assets/Kartea/Carro.png",
            GameSettings.VEHICLE_IMAGE,
            size=(GameSettings.CAR_SIZE, GameSettings.CAR_SIZE),
        )
        self.image = self.orig_image.copy()
        self.image_smaller = Image.load(
            # "Assets/Kartea/Carro.png",
            GameSettings.VEHICLE_IMAGE,
            size=(GameSettings.CAR_SIZE, GameSettings.CAR_SIZE),
        )

        # Retângulo de colisão (hitbox)
        self.rect = pygame.Rect(
            GameSettings.SCREEN_WIDTH // 2,
            GameSettings.SCREEN_HEIGHT // 2,
            GameSettings.CAR_HITBOX_SIZE[0],
            GameSettings.CAR_HITBOX_SIZE[1],
        )

        # Controle de interação (clique / pés fechados)
        self.left_click = False

        # self.hand_tracking = HandTracking()  # comentado no original

    def follow_mouse(self):
        """Atualiza a posição do carro para seguir o mouse
        (usado para testes)."""
        self.rect.center = pygame.mouse.get_pos()
        # self.hand_tracking.display_hand()  # mantido comentado

    def follow_mediapipe_hand(self, x: int, y: int):
        """Atualiza a posição do carro com base na posição detectada
        pelos pés (MediaPipe)."""
        self.rect.center = (x, y)

    def draw_hitbox(self, surface: pygame.Surface):
        """Desenha a hitbox do carro (ativado pela variável DRAW_HITBOX)."""
        pygame.draw.rect(surface, (200, 60, 0), self.rect)

    def draw(self, surface: pygame.Surface):
        """Desenha o carro na tela."""
        from ttea.games.kartea.gamemodel import Image

        # Desenha a imagem do carro centralizada
        Image.draw(surface, self.image, self.rect.center, pos_mode="center")

        # Desenha a hitbox se estiver ativada nas configurações
        if GameSettings.DRAW_HITBOX:
            self.draw_hitbox(surface)

    def on_target(self, targets):
        """
        Retorna uma lista com todos os alvos/obstáculos que estão colidindo
        com a hitbox do carro.
        """
        return [
            target for target in targets if self.rect.colliderect(target.rect)
        ]

    def kill_targets(
        self, surface: pygame.Surface, targets: list, score: int, sounds: dict
    ) -> int:
        """
        Mata os alvos que colidem com o carro quando
        o jogador "clica" (left_click = True). Retorna o score atualizado.
        """
        for target in self.on_target(targets):
            target_score = target.kill(surface, targets, sounds)
            score += target_score

        return score
