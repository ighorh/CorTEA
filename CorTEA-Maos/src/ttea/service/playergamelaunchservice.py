import json
from typing import List

# Local module import
from ttea.model import Player, Professional
from ttea.util import PathConfig


class PlayerGameLaunchService:
    METADATA_FILENAME = "metadata.json"

    def __init__(self):
        from ttea.service import PlayerService, ProfessionalService

        self.player_service = PlayerService()
        self.professional_service = ProfessionalService()

    def get_all_players(self) -> List[Player]:
        return sorted(
            self.player_service.get_all_players(),
            key=lambda p: p.name,
        )

    def get_all_professionals(self) -> List[Professional]:
        return sorted(
            self.professional_service.get_all_professionals(),
            key=lambda h: h.name,
        )

    def get_games_metadata(self) -> List[dict]:
        games = []
        exergame_dir = PathConfig.EXERGAME_DIR

        for d in exergame_dir.iterdir():
            if d.is_dir():
                meta_path = d / PlayerGameLaunchService.METADATA_FILENAME
                if meta_path.exists():
                    with open(meta_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        data["folder_path"] = str(d)  # Guarda o caminho real
                        games.append(data)
        return games
