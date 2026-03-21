#!/usr/bin/env python3
"""
Enriquecimiento HYPER de la KB con contenido solo de cafe.
Objetivo: ampliar cobertura conversacional en campo tecnico.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
KB_PATH = ROOT / "app" / "src" / "main" / "assets" / "agrochat_knowledge_base.json"


def normalize(text: str) -> str:
    text = text.lower().strip()
    text = (
        text.replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ü", "u")
        .replace("ñ", "n")
    )
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def card(category: str, questions: list[str], answer: str, keywords: list[str]) -> dict[str, Any]:
    return {
        "category": category,
        "questions": questions,
        "answer": answer,
        "keywords": keywords,
    }


def split_tokens(*parts: str) -> list[str]:
    out: list[str] = []
    for p in parts:
        p_norm = normalize(p)
        if not p_norm:
            continue
        out.extend([t for t in p_norm.split() if len(t) >= 3])
    # de-dup conservando orden
    seen: set[str] = set()
    uniq: list[str] = []
    for t in out:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    return uniq


CARDS: list[dict[str, Any]] = []


PESTS = [
    {
        "name": "broca del cafe",
        "signal": "perforaciones en fruto, pasilla y merma de rendimiento",
        "risk": "cosecha incompleta y focos residuales",
        "management": "repase riguroso, monitoreo por lote y corte de ciclo en beneficio",
    },
    {
        "name": "minador de la hoja",
        "signal": "galerias claras en hojas y menor area fotosintetica",
        "risk": "epocas secas con estres de planta",
        "management": "monitoreo temprano, manejo de sombra y conservacion de enemigos naturales",
    },
    {
        "name": "cochinilla de la raiz",
        "signal": "decaimiento progresivo y debilitamiento radicular",
        "risk": "suelos compactados y plantas estresadas",
        "management": "mejorar estructura de suelo, sanear focos y sostener vigor nutricional",
    },
    {
        "name": "cochinilla verde",
        "signal": "melaza, fumagina y brotes debilitados",
        "risk": "sombras densas y poca ventilacion",
        "management": "regular sombra, podar para airear y reforzar control biologico",
    },
    {
        "name": "escamas",
        "signal": "costras en ramas y succion de savia",
        "risk": "copas cerradas y baja inspeccion",
        "management": "podas de saneamiento, limpieza de focos y seguimiento semanal",
    },
    {
        "name": "trips",
        "signal": "raspado de tejidos tiernos y deformaciones",
        "risk": "brotacion tierna en periodos secos",
        "management": "monitoreo en brotes, manejo de estres hidrico y equilibrio biologico",
    },
    {
        "name": "acaro rojo",
        "signal": "bronceado foliar y reduccion de vigor",
        "risk": "sequias y polvo en lotes expuestos",
        "management": "cobertura de suelo, ajuste de sombra y vigilancia de focos",
    },
    {
        "name": "nematodos agalladores",
        "signal": "agallas en raices y crecimiento limitado",
        "risk": "material vegetal sin control sanitario",
        "management": "usar material sano, mejorar suelo y aislar areas afectadas",
    },
    {
        "name": "hormiga arriera",
        "signal": "defoliacion rapida en plantas jovenes",
        "risk": "nidos activos cerca de lotes nuevos",
        "management": "deteccion temprana de hormigueros y manejo integrado del foco",
    },
    {
        "name": "barrenador del tallo",
        "signal": "orificios en tallo y debilitamiento estructural",
        "risk": "plantas con heridas y bajo vigor",
        "management": "podas higienicas, retiro de tejido afectado y seguimiento por lotes",
    },
    {
        "name": "orugas defoliadoras",
        "signal": "consumo de follaje y perdida de area fotosintetica",
        "risk": "focos no detectados a tiempo",
        "management": "inspeccion del follaje, accion temprana y monitoreo continuo",
    },
    {
        "name": "chicharritas",
        "signal": "succion de savia y debilitamiento general",
        "risk": "malezas hospederas sin manejo",
        "management": "manejo de arvenses y vigilancia en bordes del lote",
    },
    {
        "name": "mosca blanca",
        "signal": "debilitamiento foliar y presencia de melaza",
        "risk": "ambientes calidos con alta poblacion",
        "management": "monitoreo, manejo de cobertura y fortalecimiento del balance biologico",
    },
    {
        "name": "pulgones",
        "signal": "enrollamiento de brotes y presencia de melaza",
        "risk": "brotes tiernos en exceso",
        "management": "regular nitrogeno, manejar hormigas y controlar focos tempranos",
    },
    {
        "name": "babosas y caracoles",
        "signal": "dano en tejido tierno de plantas jovenes",
        "risk": "humedad alta y residuos acumulados",
        "management": "orden del lote, barreras fisicas y vigilancia nocturna en focos",
    },
    {
        "name": "grillos cortadores",
        "signal": "cortes en plántulas recien establecidas",
        "risk": "lotes nuevos con cobertura desordenada",
        "management": "proteccion inicial de plantas y monitoreo en establecimiento",
    },
    {
        "name": "comejen",
        "signal": "debilitamiento en madera y raices",
        "risk": "residuos leñosos sin manejo",
        "management": "higiene de lotes, retiro de material comprometido y seguimiento",
    },
    {
        "name": "chinches",
        "signal": "deformaciones en tejido y abortos de fruto",
        "risk": "falta de monitoreo en etapas criticas",
        "management": "muestreo periodico y manejo integrado por umbrales",
    },
    {
        "name": "picudo de ramas",
        "signal": "dano en brotes y ramas productivas",
        "risk": "residuos de poda en el lote",
        "management": "manejo sanitario de residuos y seguimiento de focos",
    },
    {
        "name": "saltahojas",
        "signal": "succion en hojas y perdida de vigor",
        "risk": "desequilibrio de cobertura y hospederos alternos",
        "management": "manejo de arvenses y monitoreo en bordes",
    },
    {
        "name": "gorgojos de almacenamiento",
        "signal": "dano de grano en bodega",
        "risk": "almacenamiento prolongado sin control",
        "management": "higiene de bodega, rotacion de inventario y control de condiciones",
    },
    {
        "name": "roedores en beneficio",
        "signal": "contaminacion y dano de lotes almacenados",
        "risk": "bodegas sin barreras ni orden sanitario",
        "management": "buenas practicas de almacenamiento y control preventivo",
    },
]

for p in PESTS:
    name = p["name"]
    CARDS.append(
        card(
            "plagas",
            [
                f"Como manejar {name} en cafe",
                f"Control de {name} en cafetal",
                f"Que hacer con {name} en cultivo de cafe",
                f"Plan de manejo para {name} en cafe",
            ],
            f"En cafe, {name} suele causar {p['signal']}. El riesgo sube con {p['risk']}. "
            f"Para manejarlo conviene {p['management']} dentro de un esquema de monitoreo por lote.",
            split_tokens("cafe plaga manejo monitoreo", name, p["risk"]),
        )
    )
    CARDS.append(
        card(
            "diagnostico",
            [
                f"Como identificar {name} en cafe",
                f"Sintomas de {name} en cafeto",
                f"Diagnostico de {name} en lote de cafe",
                f"Senales tempranas de {name} en cafe",
            ],
            f"Para diagnosticar {name} en cafe, revisa distribucion del dano, estado del lote y etapa fenologica. "
            f"Las senales mas comunes son {p['signal']}. Si confirmas focos, aplica manejo dirigido y registra evolucion semanal.",
            split_tokens("cafe diagnostico plaga foco", name, p["signal"]),
        )
    )


DISEASES = [
    {
        "name": "roya del cafe",
        "signal": "manchas amarillas y polvo anaranjado en hojas",
        "risk": "alta humedad con tejido susceptible",
        "management": "variedad adaptada, nutricion balanceada y control oportuno por focos",
    },
    {
        "name": "cercospora",
        "signal": "manchas en hojas y frutos, con deterioro de calidad",
        "risk": "estres nutricional y radiacion fuerte",
        "management": "corregir nutricion, reducir estres y vigilar periodos criticos",
    },
    {
        "name": "ojo de gallo",
        "signal": "lesiones circulares y defoliacion",
        "risk": "sombras densas y humedad persistente",
        "management": "regular sombra, airear copa y retirar focos severos",
    },
    {
        "name": "antracnosis",
        "signal": "lesiones oscuras en brotes y frutos",
        "risk": "lluvias frecuentes con tejido estresado",
        "management": "higiene de poda, monitoreo y manejo preventivo",
    },
    {
        "name": "mal rosado",
        "signal": "costra rosada en ramas y secamiento",
        "risk": "ambientes humedos con copas cerradas",
        "management": "podas sanitarias y mejora de ventilacion",
    },
    {
        "name": "llaga negra",
        "signal": "decaimiento y perdida de raices funcionales",
        "risk": "suelos con mal drenaje",
        "management": "recuperar drenaje y sanear focos en campo",
    },
    {
        "name": "llaga estrellada",
        "signal": "marchitez y muerte regresiva en focos",
        "risk": "compactacion y exceso de humedad",
        "management": "manejar suelo, aislar focos y renovar cuando aplique",
    },
    {
        "name": "muerte descendente",
        "signal": "secamiento de puntas hacia ramas productivas",
        "risk": "estrés acumulado y heridas sin manejo",
        "management": "poda limpia, desinfeccion y recuperacion del vigor",
    },
    {
        "name": "pudricion de raiz",
        "signal": "amarillamiento, marchitez y pobre anclaje",
        "risk": "encharcamiento y baja aireacion del suelo",
        "management": "mejorar estructura del suelo y drenaje",
    },
    {
        "name": "mancha aureolada",
        "signal": "lesiones con halo clorotico",
        "risk": "heridas de labor y humedad alta",
        "management": "higiene en labores y control preventivo",
    },
    {
        "name": "necrosis de ramas",
        "signal": "secamiento localizado de ramas productivas",
        "risk": "copas densas y manejo tardio",
        "management": "poda sanitaria y apertura de copa",
    },
    {
        "name": "hongo de almacigo",
        "signal": "damping off y muerte de plantulas",
        "risk": "sustrato contaminado y exceso de humedad",
        "management": "desinfeccion, buen drenaje y manejo higienico de vivero",
    },
    {
        "name": "moho de pergamino",
        "signal": "olor a humedad y deterioro fisico del grano",
        "risk": "secado insuficiente o bodega humeda",
        "management": "secado uniforme y almacenamiento seguro",
    },
    {
        "name": "fermentacion no deseada",
        "signal": "olores avinagrados e inconsistencia en taza",
        "risk": "tiempos excesivos y mala higiene en beneficio",
        "management": "controlar tiempo, limpieza y trazabilidad del proceso",
    },
    {
        "name": "contaminacion cruzada en beneficio",
        "signal": "defectos repetitivos en lotes de taza",
        "risk": "mezcla de lotes y equipos sin limpieza",
        "management": "flujo limpio por lotes y protocolos de higiene",
    },
    {
        "name": "mildew en bodega",
        "signal": "olor a moho y perdida de frescura",
        "risk": "humedad relativa alta en almacenamiento",
        "management": "ventilacion, control de humedad y estibas",
    },
    {
        "name": "marchitez vascular",
        "signal": "decaimiento y baja transpiracion",
        "risk": "estres acumulado y suelo degradado",
        "management": "diagnostico de raiz, manejo de suelo y renovacion de focos",
    },
    {
        "name": "necrosis foliar por estres",
        "signal": "bordes secos y lesion en hojas expuestas",
        "risk": "radiacion alta y desbalance hidrico",
        "management": "ajustar sombra, agua y nutricion de soporte",
    },
]

for d in DISEASES:
    name = d["name"]
    CARDS.append(
        card(
            "enfermedad",
            [
                f"Como manejar {name} en cafe",
                f"Tratamiento de {name} en cafetal",
                f"Control integrado de {name} en cafe",
                f"Que hacer con {name} en cultivo de cafe",
            ],
            f"En cafe, {name} puede mostrar {d['signal']}. Se favorece con {d['risk']}. "
            f"El manejo recomendado es {d['management']} y seguimiento tecnico por lote.",
            split_tokens("cafe enfermedad manejo sanidad", name, d["risk"]),
        )
    )
    CARDS.append(
        card(
            "diagnostico",
            [
                f"Como identificar {name} en cafeto",
                f"Sintomas de {name} en cafe",
                f"Diagnostico de {name} en lote cafetero",
                f"Senales de {name} en cafe",
            ],
            f"Para diagnosticar {name}, revisa patron del dano, historial de clima y manejo reciente del lote. "
            f"Una senal tipica es {d['signal']}. Confirma focos y prioriza acciones preventivas en el bloque.",
            split_tokens("cafe diagnostico enfermedad", name, d["signal"]),
        )
    )


DEFICIENCIES = [
    ("nitrogeno", "N", "hojas viejas palidas y bajo crecimiento", "fraccionar nitrogeno y reforzar materia organica"),
    ("fosforo", "P", "desarrollo radicular debil y baja floracion", "ajustar pH y reponer fosforo segun analisis"),
    ("potasio", "K", "bordes necróticos y menor llenado", "incrementar potasio de forma balanceada"),
    ("calcio", "Ca", "tejidos nuevos debiles", "usar enmiendas calcicas y mejorar suelo"),
    ("magnesio", "Mg", "clorosis internerval en hojas maduras", "corregir balance cationico con Mg"),
    ("azufre", "S", "amarillamiento en hojas jovenes", "integrar fuentes con azufre"),
    ("boro", "B", "brotes deformes y bajo cuajado", "corregir con dosis bajas y precisas"),
    ("zinc", "Zn", "hojas pequenas y entrenudos cortos", "suplementar Zn segun analisis foliar"),
    ("hierro", "Fe", "clorosis en hojas nuevas", "recuperar salud radicular y ajustar pH"),
    ("manganeso", "Mn", "moteado clorotico", "balancear nutricion y acidez"),
    ("cobre", "Cu", "brotacion debil", "aplicar micronutriente con criterio tecnico"),
    ("molibdeno", "Mo", "ineficiencia en uso de nitrogeno", "ajustar micronutricion de precision"),
]

for name, sym, signal, action in DEFICIENCIES:
    CARDS.append(
        card(
            "fertilizacion",
            [
                f"Deficiencia de {name} en cafe",
                f"Falta de {sym} en cafeto",
                f"Como corregir carencia de {name} en cafe",
                f"Sintomas por baja de {name} en cafe",
            ],
            f"En cafe, la deficiencia de {name} ({sym}) suele verse como {signal}. "
            f"Para corregirla conviene {action} y validar respuesta del lote con seguimiento tecnico.",
            split_tokens("cafe fertilizacion nutricion deficiencia", name, sym),
        )
    )
    CARDS.append(
        card(
            "diagnostico",
            [
                f"Como diferenciar deficiencia de {name} en cafe",
                f"Diagnostico de carencia de {name} en cafetal",
                f"Como reconocer baja de {sym} en cafe",
                f"Patrones de falta de {name} en cafe",
            ],
            f"Para diagnosticar falta de {name} en cafe, revisa distribucion del sintoma en el lote, etapa fenologica y analisis de suelo/hoja. "
            f"Si predomina {signal}, conviene ajustar nutricion de forma dirigida.",
            split_tokens("cafe diagnostico nutricion", name, sym, signal),
        )
    )


SYMPTOM_CASES = [
    ("hojas amarillas en tercio inferior", "deficiencia nutricional o raiz estresada", "revisar drenaje, analisis de suelo y plan de fertilizacion"),
    ("manchas circulares en hojas", "enfermedad foliar", "identificar patron, mejorar aireacion y actuar por focos"),
    ("frutos con perforaciones", "plaga perforadora", "muestrear incidencia y ejecutar manejo integrado"),
    ("caida prematura de frutos", "estres hidrico, nutricional o sanitario", "evaluar carga, agua y sanidad del lote"),
    ("brotes deformes", "deficiencia de micronutrientes o dano de plaga", "verificar brotes nuevos y ajustar plan de correccion"),
    ("marchitez en horas de calor", "problema radicular o deficit de agua", "chequear humedad de suelo y estado de raices"),
    ("bajo llenado de grano", "desbalance de potasio o estres en llenado", "alinear nutricion y manejo de agua en etapa critica"),
    ("defoliacion acelerada", "presion de enfermedad o plaga", "inspeccionar hojas caidas y focos activos"),
    ("muerte de plantas en focos", "problema de suelo o patogeno radicular", "aislar foco, revisar drenaje y renovar puntos criticos"),
    ("sabor avinagrado en taza", "fermentacion fuera de control", "estandarizar tiempos y limpieza de proceso"),
    ("olor a humedad en pergamino", "secado o almacenamiento deficiente", "corregir humedad final y condiciones de bodega"),
    ("grano con moho", "rehumectacion o mala ventilacion", "secar nuevamente solo si es viable y corregir bodega"),
    ("lote muy disparejo", "fallas de establecimiento y manejo desigual", "sectorizar y manejar sublotes"),
    ("arboles con poco vigor", "nutricion insuficiente o suelo limitado", "priorizar recuperacion de suelo y fertilizacion dirigida"),
    ("flores que no cuajan", "estres en floracion", "revisar agua, boro y sanidad en fase floral"),
    ("puntas de ramas secas", "muerte descendente o estres severo", "hacer poda sanitaria y recuperar vigor"),
    ("amarillamiento en hojas nuevas", "deficiencia de micronutrientes", "apoyarse en analisis foliar y ajuste puntual"),
    ("encharcamiento frecuente", "drenaje insuficiente", "abrir drenajes funcionales y proteger estructura del suelo"),
    ("erosion en ladera", "suelo sin cobertura ni barreras", "implementar curvas a nivel, cobertura y barreras vivas"),
    ("incremento rapido de broca", "fruta residual y repase insuficiente", "cosecha sanitaria y control de focos"),
    ("alto porcentaje de pasilla", "problemas de sanidad o cosecha", "mejorar manejo de broca y seleccion de madurez"),
    ("baja productividad sostenida", "lotes envejecidos o limitantes de manejo", "evaluar renovacion escalonada"),
    ("frutos inmaduros en cosecha", "mala seleccion de recoleccion", "capacitar recolectores y programar pases"),
    ("secado muy lento", "capa gruesa o baja ventilacion", "ajustar espesor de capa y frecuencia de volteo"),
    ("secado demasiado rapido", "temperatura alta sin control", "moderar carga termica para proteger calidad"),
    ("brote tierno con dano de raspado", "trips u otros chupadores", "monitorear y actuar temprano por foco"),
    ("planta con anclaje debil", "raiz comprometida", "revisar sanidad radicular y estructura de suelo"),
    ("follaje opaco y sin brillo", "estres nutricional o hidrico", "ajustar riego de apoyo y nutricion"),
]

for symptom, probable, action in SYMPTOM_CASES:
    CARDS.append(
        card(
            "diagnostico",
            [
                f"En cafe tengo {symptom}, que puede ser",
                f"Que significa {symptom} en cafeto",
                f"Como actuar si hay {symptom} en cafe",
                f"Diagnostico para {symptom} en cafetal",
            ],
            f"Cuando en cafe aparece {symptom}, suele estar asociado a {probable}. "
            f"Lo recomendable es {action} y registrar resultados para ajustar la decision tecnica.",
            split_tokens("cafe diagnostico sintoma", symptom, probable),
        )
    )


POSTHARVEST_TOPICS = [
    ("proceso lavado", "control de fermentacion, limpieza y secado uniforme", "consistencia de taza y menor riesgo de defectos"),
    ("proceso honey", "manejo preciso de mucilago y secado lento", "dulzor y perfil diferenciado"),
    ("proceso natural", "cosecha muy limpia y control estricto de secado", "perfil frutal con mayor riesgo si no hay control"),
    ("fermentacion anaerobia", "tiempo, temperatura e inocuidad del proceso", "complejidad sensorial con alto control tecnico"),
    ("despulpado", "calibracion de maquina y limpieza constante", "menos danos mecanicos y mejor calidad fisica"),
    ("lavado de cafe", "uso racional de agua y manejo higienico", "estabilidad de proceso y menor contaminacion"),
    ("clasificacion de cereza", "separar verdes, maduros y sobremaduros", "mejor rendimiento y taza"),
    ("clasificacion de pergamino", "homogeneizar lote por humedad y calidad", "mejor consistencia comercial"),
    ("secado en marquesina", "capas controladas y volteo frecuente", "humedad final mas uniforme"),
    ("secado mecanico", "temperatura moderada y control de flujo", "reduccion de tiempos sin deteriorar calidad"),
    ("almacenamiento en bodega", "ambiente seco, limpio y ventilado", "proteccion de calidad y vida util"),
    ("trazabilidad de lotes", "registro desde cosecha hasta venta", "mejor negociacion comercial"),
    ("catacion interna", "evaluar aroma, sabor y defectos de manera periodica", "decisiones de mejora por lote"),
    ("control de humedad final", "medicion objetiva antes de almacenar", "evitar mohos y sobresecado"),
    ("control de actividad de agua", "validar estabilidad de almacenamiento", "reducir deterioro del perfil"),
    ("separacion por altitud y lote", "procesar lotes sin mezclar origen", "mejor diferenciacion de calidad"),
    ("limpieza de equipos de beneficio", "rutinas diarias de higiene", "menos contaminacion cruzada"),
    ("manejo de subproductos", "aprovechamiento tecnico de pulpa y mucilago", "menor impacto ambiental y mejor circularidad"),
]

for topic, control, value in POSTHARVEST_TOPICS:
    CARDS.append(
        card(
            "cosecha",
            [
                f"Como manejar {topic} en cafe",
                f"Buenas practicas de {topic} para cafetal",
                f"Que cuidar en {topic} de cafe",
                f"Mejoras para {topic} en cafe",
            ],
            f"En cafe, {topic} requiere {control}. Esto aporta {value} si se ejecuta con protocolos claros por lote.",
            split_tokens("cafe cosecha poscosecha calidad", topic, control),
        )
    )
    CARDS.append(
        card(
            "general",
            [
                f"Por que es clave {topic} en calidad de cafe",
                f"Impacto de {topic} en taza de cafe",
                f"Como mejora el precio el buen {topic}",
                f"Relación entre {topic} y valor comercial del cafe",
            ],
            f"{topic.capitalize()} impacta directamente la calidad y consistencia del cafe. "
            f"Cuando se controla bien ({control}), aumenta la probabilidad de {value}.",
            split_tokens("cafe calidad taza precio", topic, value),
        )
    )


SOIL_WATER_TOPICS = [
    ("analisis de suelo por lotes", "tomar decisiones de fertilizacion con evidencia"),
    ("analisis foliar", "ajustar correcciones nutricionales en momentos oportunos"),
    ("estructura del suelo", "favorecer raices activas y mejor infiltracion"),
    ("materia organica", "retener humedad y sostener vida microbiana"),
    ("cobertura del suelo", "reducir erosion y amortiguar temperatura"),
    ("curvas a nivel", "frenar escorrentia en laderas"),
    ("drenajes funcionales", "evitar anoxia radicular en epocas de lluvia"),
    ("riego suplementario", "proteger floracion y llenado en deficit hidrico"),
    ("cosecha de agua", "aumentar resiliencia frente a sequias"),
    ("manejo de compactacion", "mejorar crecimiento radicular"),
    ("mulch organico", "conservar humedad y reducir malezas"),
    ("enmiendas de acidez", "equilibrar disponibilidad de nutrientes"),
    ("balance calcio magnesio potasio", "evitar antagonismos nutricionales"),
    ("muestreo representativo", "evitar errores de recomendacion"),
    ("zonificacion de suelos", "manejo diferenciado por ambiente"),
    ("proteccion de nacimientos", "sostener servicio hidrico de la finca"),
    ("franjas de amortiguacion", "disminuir riesgo de contaminacion"),
    ("coberturas nobles", "controlar arvenses sin suelo desnudo"),
    ("manejo de escorrentia", "reducir perdida de fertilidad"),
    ("bioinsumos de suelo", "complementar estrategia nutricional"),
    ("uso racional de agua en beneficio", "mejorar eficiencia hidrica"),
    ("medicion de humedad de suelo", "tomar decisiones de riego con criterio"),
]

for topic, benefit in SOIL_WATER_TOPICS:
    CARDS.append(
        card(
            "cultivo",
            [
                f"Como aplicar {topic} en cafe",
                f"Recomendaciones de {topic} para cafetal",
                f"Importancia de {topic} en cultivo de cafe",
                f"Plan practico de {topic} en finca cafetera",
            ],
            f"En caficultura, {topic} ayuda a {benefit}. Implementarlo por lotes con seguimiento tecnico mejora estabilidad productiva.",
            split_tokens("cafe suelo agua cultivo manejo", topic, benefit),
        )
    )


PRUNING_TOPICS = [
    ("poda de formacion", "definir arquitectura productiva desde etapas tempranas"),
    ("poda de mantenimiento", "equilibrar carga y vigor del arbol"),
    ("poda sanitaria", "retirar tejido enfermo y bajar inoculo"),
    ("deschuponado", "evitar competencia de brotes improductivos"),
    ("renovacion por zoca", "rejuvenecer lotes envejecidos"),
    ("renovacion por siembra", "actualizar material vegetal del lote"),
    ("renovacion escalonada", "evitar caida brusca del flujo de caja"),
    ("seleccion de ejes productivos", "mejorar aireacion y cosecha"),
    ("poda postcosecha", "recuperar planta para siguiente ciclo"),
    ("manejo de residuos de poda", "reducir focos sanitarios"),
    ("desinfeccion de herramientas", "disminuir diseminacion de problemas"),
    ("apertura de copa", "mejorar luz y ventilacion"),
    ("equilibrio entre vegetativo y productivo", "sostener estabilidad anual"),
    ("calendario de poda por lote", "ordenar labores segun fenologia"),
    ("podas en lotes sombreados", "reducir humedad excesiva en copa"),
    ("podas en lotes a sol", "regular estres y conservar estructura"),
]

for topic, objective in PRUNING_TOPICS:
    CARDS.append(
        card(
            "cultivo",
            [
                f"Como manejar {topic} en cafe",
                f"Objetivo de {topic} en cafeto",
                f"Cuando aplicar {topic} en cafetal",
                f"Errores frecuentes en {topic} de cafe",
            ],
            f"En cafe, {topic} se usa para {objective}. Conviene ejecutarla por lote, con criterios de edad, vigor y estado sanitario.",
            split_tokens("cafe poda renovacion manejo", topic, objective),
        )
    )


NURSERY_TOPICS = [
    ("seleccion de semilla", "arrancar con material de buena calidad"),
    ("manejo de semillero", "obtener chapolas uniformes"),
    ("trasplante a bolsa", "evitar estres temprano de plantula"),
    ("calidad del sustrato", "favorecer raiz sana y drenaje"),
    ("riego en vivero", "evitar exceso o deficit hidrico"),
    ("sombra en vivero", "proteger plantulas sin ahilar"),
    ("fertilizacion en vivero", "promover vigor equilibrado"),
    ("control sanitario en almacigo", "evitar diseminacion de problemas"),
    ("seleccion negativa de plantulas", "descartar material debil"),
    ("endurecimiento de colinos", "mejor adaptacion al campo"),
    ("logistica de transporte de colinos", "reducir dano mecanico"),
    ("siembra en epoca de lluvias", "mejorar prendimiento"),
    ("reposicion de fallas", "conservar uniformidad del lote"),
    ("proteccion inicial del colino", "disminuir mortalidad temprana"),
    ("registro de lote de vivero", "trazar origen y calidad de material"),
]

for topic, objective in NURSERY_TOPICS:
    CARDS.append(
        card(
            "siembra",
            [
                f"Como manejar {topic} en cafe",
                f"Recomendacion para {topic} en vivero de cafe",
                f"Buenas practicas de {topic} para colinos",
                f"Errores comunes de {topic} en establecimiento de cafe",
            ],
            f"Para cafe, {topic} es clave para {objective}. Un buen manejo en vivero y establecimiento reduce problemas en los primeros anos del lote.",
            split_tokens("cafe siembra vivero colinos", topic, objective),
        )
    )


CLIMATE_BUSINESS_TOPICS = [
    ("adaptacion al cambio climatico", "combinar sombra regulada, suelo vivo y gestion de agua"),
    ("plan de riesgo climatico", "definir acciones antes de sequia o lluvias extremas"),
    ("resiliencia del cafetal", "integrar practicas de suelo, agua y sanidad"),
    ("gestion de mano de obra en cosecha", "mejorar eficiencia sin sacrificar calidad"),
    ("registro de costos por lote", "identificar fugas y mejorar rentabilidad"),
    ("costo por kilo de cafe", "tomar decisiones economicas basadas en datos"),
    ("trazabilidad para venta", "abrir mercados con mejor precio"),
    ("preparacion para certificaciones", "ordenar evidencia tecnica y ambiental"),
    ("economia circular en finca", "aprovechar subproductos y reducir desperdicio"),
    ("plan anual de labores", "coordinar poda, nutricion, sanidad y cosecha"),
    ("extension tecnica con productores", "traducir recomendacion en acciones simples"),
    ("adopcion de recomendaciones", "hacer seguimiento corto y medible"),
    ("evaluacion de renovacion", "comparar costo de sostener vs renovar lotes"),
    ("negociacion comercial de lotes", "apoyarse en datos de calidad y trazabilidad"),
    ("diferenciacion por calidad", "separar lotes y repetir protocolos exitosos"),
    ("control de desperdicios de proceso", "subir eficiencia del beneficio"),
    ("seguridad laboral en finca", "proteger personas y continuidad operativa"),
    ("plan de capacitacion de cuadrillas", "estandarizar criterios de calidad"),
    ("gestion de inventario en bodega", "evitar perdida de valor por almacenamiento"),
    ("control de indicadores tecnicos", "medir productividad, sanidad y calidad"),
    ("estrategia de mercado para cafe especial", "alinear proceso y trazabilidad con demanda"),
    ("priorizacion de inversiones", "enfocar recursos en cuellos de botella"),
]

for topic, action in CLIMATE_BUSINESS_TOPICS:
    CARDS.append(
        card(
            "general",
            [
                f"Como mejorar {topic} en cafe",
                f"Estrategia para {topic} en finca cafetera",
                f"Recomendaciones de {topic} para productores de cafe",
                f"Plan practico de {topic} en caficultura",
            ],
            f"Para fortalecer {topic} en cafe, conviene {action}. Aplicarlo por lotes con registros claros mejora decisiones y resultados.",
            split_tokens("cafe gestion estrategia", topic, action),
        )
    )


def main() -> None:
    kb = json.loads(KB_PATH.read_text(encoding="utf-8"))
    entries = kb.get("entries", [])
    categories = kb.get("categories", [])

    existing_q = {normalize(q) for e in entries for q in e.get("questions", [])}
    existing_answer = {normalize(e.get("answer", "")) for e in entries if e.get("answer")}

    next_id = max((e.get("id", 0) for e in entries), default=0) + 1
    added = 0

    for c in CARDS:
        unique_questions = []
        for q in c["questions"]:
            nq = normalize(q)
            if nq and nq not in existing_q:
                unique_questions.append(q)

        if not unique_questions:
            continue

        n_answer = normalize(c["answer"])
        if n_answer in existing_answer:
            continue

        category = c["category"]
        if category not in categories:
            categories.append(category)

        entries.append(
            {
                "id": next_id,
                "category": category,
                "questions": unique_questions,
                "answer": c["answer"],
                "keywords": c["keywords"],
            }
        )
        for q in unique_questions:
            existing_q.add(normalize(q))
        existing_answer.add(n_answer)
        next_id += 1
        added += 1

    kb["entries"] = entries
    kb["categories"] = categories
    KB_PATH.write_text(json.dumps(kb, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    total_q = sum(len(e.get("questions", [])) for e in entries)
    print(f"Entradas nuevas cafe (hyper): {added}")
    print(f"Total entradas KB: {len(entries)}")
    print(f"Total preguntas KB: {total_q}")


if __name__ == "__main__":
    main()

