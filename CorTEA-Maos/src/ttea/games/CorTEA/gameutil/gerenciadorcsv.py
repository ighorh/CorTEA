import csv
import datetime
import os
from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING:  # evita importação circular com gamemodel
    from ttea.games.CorTEA.gamemodel.sessao import Sessao


class GerenciadorCSV:
    """Salva o desempenho da sessão em CSV (classe ``GerenciadorCSV`` do
    diagrama de classes; campos conforme a Tabela 2 do artigo).

    Cada linha é uma tentativa de fase. O arquivo inteiro é reescrito a
    cada tentativa concluída, então, se o jogo fechar de repente, nada que
    já foi jogado se perde (RNF04).
    """

    CAMPOS = [
        "id_sessao",
        "nome_usuario",
        "data_hora",
        "acertos",
        "erros",
        "acertos_consecutivos",
        "fase",
        "tempo_medio_resposta",
    ]

    def __init__(self, sessao: "Sessao", diretorio: Optional[str] = None):
        self.sessao = sessao
        self.diretorio = diretorio  # None = pasta de exportações do T-TEA
        self.linhas: List[Dict] = []
        self.caminho_arquivo: Optional[str] = None
        agora = sessao.data_hora.strftime("%Y%m%d_%H%M%S")
        self._nome = f"relatorio_cortea_{sessao.usuario.id_usuario}_{agora}.csv"

    def salvar_dados(
        self,
        acertos: int,
        erros: int,
        acertos_consecutivos: int,
        fase: int,
        tempo_medio_resposta: float,
    ) -> None:
        """Acrescenta uma tentativa de fase e grava o arquivo."""
        self.linhas.append(
            {
                "id_sessao": self.sessao.id_sessao,
                "nome_usuario": self.sessao.usuario.nome,
                "data_hora": datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "acertos": acertos,
                "erros": erros,
                "acertos_consecutivos": acertos_consecutivos,
                "fase": fase,
                "tempo_medio_resposta": f"{tempo_medio_resposta:.2f}",
            }
        )
        self.exportar_csv()

    def exportar_csv(self) -> Optional[str]:
        """Grava o CSV. Retorna o caminho, ou ``None`` sem nenhuma linha."""
        if not self.linhas:
            return None
        caminho = self._resolver_caminho()
        try:
            self._gravar_com_plataforma(caminho)
        except Exception:
            self._gravar_com_csv_padrao(caminho)
        self.caminho_arquivo = caminho
        return caminho

    def _resolver_caminho(self) -> str:
        if self.diretorio is not None:
            return os.path.join(self.diretorio, self._nome)
        from ttea.util import PathConfig

        return PathConfig.export(self._nome)

    def _gravar_com_plataforma(self, caminho: str) -> None:
        """Usa o CSVHandler da plataforma (mesmo dialeto dos outros jogos)."""
        from ttea.util import CSVHandler

        CSVHandler().write_csv(caminho, self.linhas, headers=self.CAMPOS)

    def _gravar_com_csv_padrao(self, caminho: str) -> None:
        """Alternativa quando a plataforma não está disponível."""
        os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
        with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
            escritor = csv.DictWriter(
                f, fieldnames=self.CAMPOS, delimiter=";", lineterminator="\n"
            )
            escritor.writeheader()
            escritor.writerows(self.linhas)
