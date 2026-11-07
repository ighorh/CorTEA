class GameState:
    """Estados possíveis da máquina de estados do jogo CorTEA."""

    # Telas de menu
    INICIO = "inicio"
    CONFIGURACOES = "configuracoes"
    CONTROLES = "controles"
    PAUSADO = "pausado"
    CONFIRMAR_SAIDA = "confirmar_saida"
    CONCLUSAO = "conclusao"

    # Telas da partida
    INTRO_FASE = "intro_fase"  # "FASE n" com a grade da fase
    MOSTRANDO = "mostrando"  # o sistema exibe o caminho
    JOGO = "jogo"  # o jogador reproduz o caminho
    INTERVALO = "intervalo"  # entre duas rodadas da mesma fase
    FASE_CONCLUIDA = "fase_concluida"
    FASE_NAO_CONCLUIDA = "fase_nao_concluida"

    ENCERRADO = "encerrado"

    # Estados em que a seleção (mouse ou mão) vale para botões
    MENUS = (INICIO, CONFIGURACOES, CONTROLES, PAUSADO, CONFIRMAR_SAIDA, CONCLUSAO)

    # Estados em que a seleção (mouse ou mão) vale para os quadrados
    SELECAO_NA_GRADE = (JOGO,)

    # Estados em que o terapeuta pode pausar a sessão
    PAUSAVEIS = (
        INTRO_FASE,
        MOSTRANDO,
        JOGO,
        INTERVALO,
        FASE_CONCLUIDA,
        FASE_NAO_CONCLUIDA,
    )
