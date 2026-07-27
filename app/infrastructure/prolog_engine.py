from pyswip import Prolog


prolog = Prolog()
prolog.consult("prolog/salud_rules.pl")

progreso_semanal = []


def obtener_recomendaciones_desde_prolog(perfil):
    recomendados = set()
    restringidos = set()
    ejercicios = set()
    descanso = set()

    for condicion in perfil.condiciones:
        consulta_alimentos = list(
            prolog.query(f"recomendar_alimento({condicion}, X)")
        )
        for r in consulta_alimentos:
            recomendados.add(r["X"])

        consulta_restringidos = list(
            prolog.query(f"restringir_alimento({condicion}, X)")
        )
        for r in consulta_restringidos:
            restringidos.add(r["X"])

        consulta_ejercicios = list(
            prolog.query(
                f"recomendar_ejercicio({condicion}, {perfil.nivel_actividad}, X)"
            )
        )
        for r in consulta_ejercicios:
            ejercicios.add(r["X"])

    consulta_objetivo = list(
        prolog.query(f"recomendar_ejercicio_objetivo({perfil.objetivo}, X)")
    )
    ejercicios_objetivo = {r["X"] for r in consulta_objetivo}

    ejercicios_finales = sorted(ejercicios.intersection(ejercicios_objetivo))
    if not ejercicios_finales:
        ejercicios_finales = sorted(ejercicios)

    if perfil.nivel_estres:
        consulta_descanso = list(
            prolog.query(f"recomendar_descanso({perfil.nivel_estres}, X)")
        )
        for r in consulta_descanso:
            descanso.add(r["X"])

    return {
        "perfil": perfil,
        "alimentacion": {
            "recomendados": sorted(recomendados),
            "restringidos": sorted(restringidos)
        },
        "ejercicio": ejercicios_finales,
        "descanso": sorted(descanso)
    }


def guardar_progreso(registro):
    progreso_semanal.append(registro.model_dump())
    return {
        "mensaje": "Progreso semanal registrado correctamente",
        "registro": registro
    }


def listar_progreso():
    return {
        "total_registros": len(progreso_semanal),
        "registros": progreso_semanal
    }