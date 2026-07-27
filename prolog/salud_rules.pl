% =========================
% CONDICIONES DE SALUD
% =========================

condicion(diabetes_tipo_2).
condicion(hipertension).
condicion(hipotiroidismo).
condicion(obesidad).
condicion(anemia).
condicion(intolerancia_lactosa).
condicion(celiaquia).

% =========================
% ALIMENTOS RECOMENDADOS
% =========================

alimento_recomendado(diabetes_tipo_2, avena).
alimento_recomendado(diabetes_tipo_2, vegetales_verdes).
alimento_recomendado(diabetes_tipo_2, legumbres).

alimento_recomendado(hipertension, banano).
alimento_recomendado(hipertension, espinaca).
alimento_recomendado(hipertension, avena).

alimento_recomendado(hipotiroidismo, pescado).
alimento_recomendado(hipotiroidismo, huevos).
alimento_recomendado(hipotiroidismo, frutas).

alimento_recomendado(obesidad, proteina_magra).
alimento_recomendado(obesidad, vegetales_verdes).
alimento_recomendado(obesidad, agua).

alimento_recomendado(anemia, carnes_magras).
alimento_recomendado(anemia, lentejas).
alimento_recomendado(anemia, espinaca).

alimento_recomendado(intolerancia_lactosa, leche_deslactosada).
alimento_recomendado(intolerancia_lactosa, yogurt_sin_lactosa).
alimento_recomendado(intolerancia_lactosa, almendras).

alimento_recomendado(celiaquia, arroz).
alimento_recomendado(celiaquia, quinoa).
alimento_recomendado(celiaquia, papa).

% =========================
% ALIMENTOS RESTRINGIDOS
% =========================

alimento_restringido(diabetes_tipo_2, azucar_refinada).
alimento_restringido(diabetes_tipo_2, pan_blanco).
alimento_restringido(diabetes_tipo_2, bebidas_azucaradas).

alimento_restringido(hipertension, sal_excesiva).
alimento_restringido(hipertension, embutidos).
alimento_restringido(hipertension, comida_procesada).

alimento_restringido(hipotiroidismo, ultraprocesados).
alimento_restringido(hipotiroidismo, exceso_soya).

alimento_restringido(obesidad, frituras).
alimento_restringido(obesidad, comida_rapida).
alimento_restringido(obesidad, postres_industriales).

alimento_restringido(anemia, exceso_cafe).
alimento_restringido(anemia, alcohol_excesivo).

alimento_restringido(intolerancia_lactosa, leche_entera).
alimento_restringido(intolerancia_lactosa, queso_regular).

alimento_restringido(celiaquia, trigo).
alimento_restringido(celiaquia, cebada).
alimento_restringido(celiaquia, centeno).

% =========================
% TIPOS DE ACTIVIDAD FISICA
% =========================

actividad(caminata_suave, bajo_impacto).
actividad(yoga, bajo_impacto).
actividad(bicicleta_estatica, moderado).
actividad(natacion, moderado).
actividad(trote_suave, moderado).
actividad(musculacion_ligera, moderado).
actividad(hiit, alta_intensidad).

% =========================
% EJERCICIOS RECOMENDADOS POR CONDICION
% =========================

ejercicio_recomendado(diabetes_tipo_2, sedentario, caminata_suave).
ejercicio_recomendado(diabetes_tipo_2, levemente_activo, bicicleta_estatica).
ejercicio_recomendado(diabetes_tipo_2, moderadamente_activo, trote_suave).

ejercicio_recomendado(hipertension, sedentario, caminata_suave).
ejercicio_recomendado(hipertension, levemente_activo, yoga).
ejercicio_recomendado(hipertension, moderadamente_activo, natacion).

ejercicio_recomendado(hipotiroidismo, sedentario, caminata_suave).
ejercicio_recomendado(hipotiroidismo, levemente_activo, musculacion_ligera).
ejercicio_recomendado(hipotiroidismo, moderadamente_activo, bicicleta_estatica).

ejercicio_recomendado(obesidad, sedentario, caminata_suave).
ejercicio_recomendado(obesidad, levemente_activo, bicicleta_estatica).
ejercicio_recomendado(obesidad, moderadamente_activo, natacion).

ejercicio_recomendado(anemia, sedentario, yoga).
ejercicio_recomendado(anemia, levemente_activo, caminata_suave).
ejercicio_recomendado(anemia, moderadamente_activo, bicicleta_estatica).

ejercicio_recomendado(intolerancia_lactosa, sedentario, caminata_suave).
ejercicio_recomendado(intolerancia_lactosa, levemente_activo, trote_suave).
ejercicio_recomendado(intolerancia_lactosa, moderadamente_activo, natacion).

ejercicio_recomendado(celiaquia, sedentario, caminata_suave).
ejercicio_recomendado(celiaquia, levemente_activo, yoga).
ejercicio_recomendado(celiaquia, moderadamente_activo, trote_suave).

% =========================
% OBJETIVOS DE BIENESTAR
% =========================

objetivo(perdida_peso).
objetivo(ganancia_muscular).
objetivo(mantenimiento).
objetivo(mejora_cardiovascular).
objetivo(reduccion_estres).

ejercicio_por_objetivo(perdida_peso, caminata_suave).
ejercicio_por_objetivo(perdida_peso, bicicleta_estatica).
ejercicio_por_objetivo(ganancia_muscular, musculacion_ligera).
ejercicio_por_objetivo(mantenimiento, yoga).
ejercicio_por_objetivo(mejora_cardiovascular, natacion).
ejercicio_por_objetivo(reduccion_estres, yoga).

% =========================
% DESCANSO Y SUEÑO
% =========================

horas_sueno_recomendadas(adulto, 7, 9).

habito_descanso(alto_estres, meditacion_nocturna).
habito_descanso(alto_estres, evitar_pantallas_antes_dormir).
habito_descanso(pocas_horas_sueno, dormir_horario_regular).
habito_descanso(pocas_horas_sueno, evitar_cafe_nocturno).
habito_descanso(sedentario, pausas_activas_diarias).

% =========================
% REGLAS DE CONSULTA SIMPLE
% =========================

recomendar_alimento(Condicion, Alimento) :-
    alimento_recomendado(Condicion, Alimento).

restringir_alimento(Condicion, Alimento) :-
    alimento_restringido(Condicion, Alimento).

recomendar_ejercicio(Condicion, NivelActividad, Ejercicio) :-
    ejercicio_recomendado(Condicion, NivelActividad, Ejercicio).

recomendar_ejercicio_objetivo(Objetivo, Ejercicio) :-
    ejercicio_por_objetivo(Objetivo, Ejercicio).

recomendar_descanso(Perfil, Habito) :-
    habito_descanso(Perfil, Habito).

% =========================
% INTERSECCIONES DE CONDICIONES
% =========================

recomendar_alimento_multiple(Condicion1, Condicion2, Alimento) :-
    alimento_recomendado(Condicion1, Alimento),
    alimento_recomendado(Condicion2, Alimento).

restringir_alimento_multiple(Condicion1, Condicion2, Alimento) :-
    alimento_restringido(Condicion1, Alimento);
    alimento_restringido(Condicion2, Alimento).

recomendar_ejercicio_seguro(Condicion, NivelActividad, Objetivo, Ejercicio) :-
    ejercicio_recomendado(Condicion, NivelActividad, Ejercicio),
    ejercicio_por_objetivo(Objetivo, Ejercicio).

recomendacion_integral(Condicion, NivelActividad, Objetivo, Alimento, Ejercicio) :-
    recomendar_alimento(Condicion, Alimento),
    recomendar_ejercicio_seguro(Condicion, NivelActividad, Objetivo, Ejercicio).