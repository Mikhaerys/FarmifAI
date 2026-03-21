#!/usr/bin/env python3
"""
Enriquecimiento MAXPLUS de KB para cafe.
Agrega una capa extra de cobertura tecnica y conversacional.
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


def toks(*parts: str) -> list[str]:
    items: list[str] = []
    for p in parts:
        items.extend([t for t in normalize(p).split() if len(t) >= 3])
    seen: set[str] = set()
    out: list[str] = []
    for t in items:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def card(category: str, questions: list[str], answer: str, keywords: list[str]) -> dict[str, Any]:
    return {
        "category": category,
        "questions": questions,
        "answer": answer,
        "keywords": keywords,
    }


CARDS: list[dict[str, Any]] = []


PHYSIOLOGY_TOPICS = [
    ("fotosintesis", "produccion de energia y biomasa", "equilibrio de luz, agua y nutricion"),
    ("respiracion", "consumo de energia para mantenimiento", "evitar estres termico y desequilibrios"),
    ("transpiracion", "regulacion hidrica y termica", "manejo de sombra y humedad del suelo"),
    ("apertura estomatica", "intercambio gaseoso y uso de agua", "mantener planta sin estres hidrico"),
    ("potencial hidrico", "estado de agua en tejidos", "definir riego de soporte y cobertura"),
    ("balance fuente-sumidero", "relacion entre hojas activas y carga de frutos", "ajustar poda y nutricion"),
    ("particion de fotoasimilados", "distribucion de carbohidratos en la planta", "evitar exceso de carga"),
    ("reserva de carbohidratos", "capacidad de respuesta en floracion y brotacion", "manejo poscosecha oportuno"),
    ("eficiencia de uso de luz", "conversion de radiacion en produccion", "regular sombra segun ambiente"),
    ("eficiencia de uso de agua", "produccion por unidad de agua consumida", "suelo cubierto y riego oportuno"),
    ("senescencia foliar", "recambio natural de hojas", "diferenciar proceso normal de dano sanitario"),
    ("vigor vegetativo", "capacidad de crecimiento de la planta", "balancear carga productiva y nutricion"),
    ("dominancia apical", "control del crecimiento por eje principal", "definir arquitectura por poda"),
    ("relacion raiz-parte aerea", "equilibrio funcional de absorcion y demanda", "proteger sistema radicular"),
    ("plasticidad fisiologica", "adaptacion de planta al ambiente", "manejo diferenciado por lote"),
    ("aclimatacion al sombreo", "ajuste de la planta a menor radiacion", "regular sombra sin extremos"),
    ("respuesta a deficit hidrico", "reduccion de crecimiento y cuajado", "acciones preventivas por etapa"),
    ("respuesta a calor excesivo", "estres metabolico y baja eficiencia", "manejo de microclima"),
    ("respuesta a frio", "ralentizacion fisiologica", "escoger variedad y manejo adecuados"),
    ("dinamica de floracion", "sincronizacion de eventos reproductivos", "planificar labores por ventana"),
    ("retencion de frutos", "capacidad de mantener carga", "evitar estres en cuajado"),
    ("aborto floral", "perdida de flores sin cuajado", "corregir estres hidrico y nutricional"),
    ("llenado fisiologico de fruto", "acumulacion de materia seca", "priorizar potasio y agua"),
    ("madurez fisiologica", "momento de maximo potencial de calidad", "cosecha en punto adecuado"),
    ("eficiencia radicular", "absorcion efectiva de agua y nutrientes", "suelo aireado y sin compactacion"),
]

for topic, role, management in PHYSIOLOGY_TOPICS:
    CARDS.append(
        card(
            "cultivo",
            [
                f"Como influye {topic} en cafe",
                f"Que es {topic} en cafeto",
                f"Importancia de {topic} para produccion de cafe",
                f"Como manejar {topic} en un cafetal",
            ],
            f"En cafe, {topic} cumple un papel clave en {role}. "
            f"Para sostener buen desempeno conviene {management} con seguimiento por lote.",
            toks("cafe fisiologia", topic, role, management),
        )
    )


CLIMATE_RISK_TOPICS = [
    ("deficit de presion de vapor", "aumenta demanda evaporativa y estres", "regular sombra y humedad de suelo"),
    ("radiacion solar alta", "eleva temperatura foliar y riesgo fisiologico", "microclima con sombreo manejado"),
    ("olas de calor", "afectan floracion, cuajado y llenado", "plan de contingencia hidrica"),
    ("lluvias intensas", "incrementan erosion y enfermedades", "drenaje y cobertura permanente"),
    ("lluvias erraticas", "desincronizan etapas fenologicas", "calendario flexible por senales de campo"),
    ("sequias prolongadas", "reducen vigor y productividad", "conservacion de agua y suelo"),
    ("noches frias", "ralentizan procesos metabolicos", "ajuste de manejo por altura"),
    ("amplitud termica extrema", "genera variacion en desarrollo", "manejo de lote por ambiente"),
    ("vientos fuertes", "causan estres mecanico y evaporativo", "barreras vivas y cobertura"),
    ("humedad relativa muy alta", "favorece enfermedades foliares", "aireacion de copa y vigilancia"),
    ("humedad relativa muy baja", "sube transpiracion y estres", "proteger suelo y sombreo"),
    ("eventos de granizo", "danan tejido y predisponen infecciones", "sanidad inmediata postevento"),
    ("escasez de agua", "limita etapas sensibles", "priorizar uso en momentos criticos"),
    ("exceso de nubosidad", "reduce fotosintesis neta", "ajustar sombra y densidad"),
    ("cambio de patrones de lluvia", "afecta calendario tradicional", "manejo basado en monitoreo"),
    ("riesgo de deslizamiento", "compromete estabilidad de laderas", "obras de conservacion"),
    ("saturacion de suelo", "asfixia radicular y decaimiento", "drenajes funcionales"),
    ("evapotranspiracion elevada", "acelera perdida de agua", "cobertura y manejo hidrico"),
    ("anomalias climaticas", "incrementan incertidumbre", "plan preventivo por escenarios"),
    ("variabilidad intra-anual", "heterogeneiza respuesta de lotes", "sectorizacion de decisiones"),
]

for factor, effect, adaptation in CLIMATE_RISK_TOPICS:
    CARDS.append(
        card(
            "general",
            [
                f"Como afecta {factor} al cafe",
                f"Riesgo de {factor} en caficultura",
                f"Que hacer en cafe frente a {factor}",
                f"Estrategia para manejar {factor} en cafetal",
            ],
            f"En cafe, {factor} puede generar que {effect}. "
            f"Para reducir impacto, conviene {adaptation} y ajustar decisiones por lote.",
            toks("cafe clima riesgo", factor, effect, adaptation),
        )
    )


QUALITY_DEFECT_MATRIX = [
    ("vinagre", "sobrefermentacion o higiene deficiente", "control estricto de tiempos"),
    ("fenolico", "contaminacion o fermentacion indeseada", "limpieza y segregacion de lotes"),
    ("terroso", "secado/almacenamiento inadecuado", "bodega seca y ventilada"),
    ("mohoso", "humedad alta en almacenamiento", "control de humedad final y estibas"),
    ("reposo", "almacenamiento prolongado sin control", "rotacion de inventario"),
    ("quaker", "fruta inmadura en cosecha", "seleccion de madurez"),
    ("pasilla brocada", "incidencia de broca", "manejo integrado y repase"),
    ("fermento excesivo", "tiempo/temperatura fuera de rango", "protocolos por lote"),
    ("astringente", "materia prima o proceso inconsistente", "estandarizar cosecha y beneficio"),
    ("amargor alto", "desbalance de proceso o tueste", "calibrar cadena completa"),
    ("nota ahumada", "exposicion a humo", "secado en ambiente limpio"),
    ("nota medicinal", "contaminacion de proceso", "higiene y control de contacto"),
    ("nota metalica", "equipos en mal estado", "mantenimiento de infraestructura"),
    ("nota a moho", "rehumectacion del pergamino", "control ambiental en bodega"),
    ("nota animal", "mala higiene de area de proceso", "orden y saneamiento"),
    ("nota salina", "agua de proceso no adecuada", "control de calidad de agua"),
    ("nota a heno", "secado irregular", "uniformar capa y volteo"),
    ("nota a madera", "almacenamiento inadecuado", "aislar lotes de olores externos"),
    ("nota avinagrada", "fermentacion excesiva", "seguimiento por horas"),
    ("defecto primario", "fallas graves en materia prima/proceso", "intervenir origen del problema"),
]

for defect, cause, control in QUALITY_DEFECT_MATRIX:
    CARDS.append(
        card(
            "cosecha",
            [
                f"Defecto {defect} en cafe",
                f"Por que aparece {defect} en taza de cafe",
                f"Como prevenir {defect} en cafe",
                f"Que hacer si sale {defect} en un lote de cafe",
            ],
            f"En cafe, el defecto {defect} suele relacionarse con {cause}. "
            f"Para prevenirlo conviene {control}, con trazabilidad desde cosecha hasta bodega.",
            toks("cafe defecto calidad taza", defect, cause, control),
        )
    )


ROOT_CAUSE_PAIRS = [
    ("caida de rendimiento", "lote envejecido, nutricion ineficiente o sanidad tardia"),
    ("uniformidad baja", "fallas de establecimiento y manejo desigual"),
    ("alta incidencia de plaga", "monitoreo insuficiente y controles fuera de tiempo"),
    ("alta incidencia de enfermedad", "ambiente predisponente y falta de prevencion"),
    ("costo elevado por kilo", "reprocesos, ineficiencia y baja productividad"),
    ("precio de venta bajo", "calidad inconsistente y poca trazabilidad"),
    ("mala taza recurrente", "variabilidad de cosecha y poscosecha"),
    ("brotes debiles", "desbalance nutricional y estres hidrico"),
    ("floracion irregular", "estres en fase previa y manejo no sincronizado"),
    ("cuajado bajo", "agua/nutricion inadecuada en etapa critica"),
    ("llenado deficiente", "carga excesiva y desequilibrio de potasio/agua"),
    ("defoliacion acelerada", "presion sanitaria o estres acumulado"),
    ("mortalidad de plantas", "problemas de raiz, drenaje o establecimiento"),
    ("pasilla alta", "cosecha no selectiva o dano de plagas"),
    ("moho en bodega", "humedad y ventilacion insuficiente"),
    ("fermentacion fuera de control", "falta de protocolo y seguimiento"),
    ("tiempos muertos en beneficio", "flujo operativo mal disenhado"),
    ("fatiga del suelo", "baja materia organica y manejo extractivo"),
    ("erosion creciente", "cobertura insuficiente y pendiente sin proteccion"),
    ("rotacion de personal alta", "capacitacion e incentivos inadecuados"),
]

for issue, likely in ROOT_CAUSE_PAIRS:
    CARDS.append(
        card(
            "diagnostico",
            [
                f"Como diagnosticar {issue} en cafe",
                f"Causas de {issue} en cafetal",
                f"Que revisar cuando hay {issue} en cafe",
                f"Plan de accion para {issue} en finca cafetera",
            ],
            f"Cuando aparece {issue} en cafe, normalmente se asocia a {likely}. "
            f"Lo recomendable es validar datos por lote, priorizar causa principal y ejecutar acciones medibles de corto plazo.",
            toks("cafe diagnostico causa", issue, likely),
        )
    )


COST_STRUCTURES = [
    ("mano de obra de cosecha", "productividad por recolector y calidad de seleccion"),
    ("mano de obra de beneficio", "flujo de proceso y reprocesos"),
    ("fertilizantes", "eficiencia de aplicacion y respuesta por lote"),
    ("enmiendas", "impacto en salud de suelo y retorno tecnico"),
    ("control sanitario", "momento de intervencion y foco"),
    ("manejo de arvenses", "frecuencia y metodo de control"),
    ("poda y renovacion", "planificacion anual y escala de ejecucion"),
    ("secado", "energia, tiempo y perdida de calidad"),
    ("almacenamiento", "mermas por humedad y deterioro"),
    ("transporte interno", "organizacion de rutas y tiempos"),
    ("infraestructura de beneficio", "mantenimiento y eficiencia operativa"),
    ("agua de proceso", "consumo por kilo procesado"),
    ("insumos de limpieza", "impacto en inocuidad del proceso"),
    ("costos administrativos", "organizacion de registros y decisiones"),
    ("capacitacion del equipo", "reduccion de errores de operacion"),
    ("seguimiento tecnico", "mejora continua y prevencion de perdidas"),
    ("renovacion de lotes", "retorno de inversion por bloque"),
    ("control de calidad", "diferencial de precio por consistencia"),
    ("comercializacion", "valor agregado por trazabilidad"),
    ("riesgo climatico", "costos evitados por preparacion"),
]

for component, lever in COST_STRUCTURES:
    CARDS.append(
        card(
            "general",
            [
                f"Como optimizar {component} en cafe",
                f"Impacto de {component} en rentabilidad cafetera",
                f"Que medir en {component} para mejorar cafe",
                f"Estrategia para reducir costo de {component} en cafe",
            ],
            f"En cafe, {component} influye directamente en el costo por kilo. "
            f"La palanca principal de mejora es {lever}, con seguimiento por lote y por etapa del proceso.",
            toks("cafe costos rentabilidad", component, lever),
        )
    )


COMPLIANCE_TOPICS = [
    ("buenas practicas agricolas", "ordenar manejo de campo y seguridad"),
    ("buenas practicas de manufactura", "asegurar higiene en beneficio"),
    ("inocuidad", "reducir riesgos de contaminacion"),
    ("trazabilidad documental", "responder auditorias con evidencia"),
    ("seguridad y salud en trabajo", "proteger equipo y continuidad"),
    ("gestion de residuos", "cumplimiento ambiental"),
    ("manejo de aguas residuales", "disminuir impacto en fuentes hidricas"),
    ("proteccion de rondas hidricas", "conservar recurso agua"),
    ("almacenamiento seguro de insumos", "prevenir incidentes"),
    ("calibracion de equipos", "garantizar consistencia operativa"),
    ("control de plagas en bodega", "evitar deterioro del cafe"),
    ("plan de contingencia", "responder ante eventos criticos"),
    ("registro de capacitaciones", "evidenciar mejora de competencias"),
    ("inspecciones internas", "detectar fallas antes de auditoria"),
    ("indicadores de cumplimiento", "medir avance de la finca"),
]

for topic, objective in COMPLIANCE_TOPICS:
    CARDS.append(
        card(
            "general",
            [
                f"Como implementar {topic} en cafe",
                f"Por que es importante {topic} en finca cafetera",
                f"Que exige {topic} para productores de cafe",
                f"Checklist de {topic} para cafetal",
            ],
            f"En caficultura, {topic} sirve para {objective}. "
            f"Implementarlo con responsables y registros claros mejora confiabilidad tecnica y comercial.",
            toks("cafe cumplimiento gestion", topic, objective),
        )
    )


ACRONYM_CARDS = [
    ("VPD", "general", "deficit de presion de vapor entre hoja y aire", "interpretar demanda evaporativa y riesgo de estres"),
    ("BPA", "general", "buenas practicas agricolas", "ordenar manejo tecnico y ambiental en finca"),
    ("BPM", "general", "buenas practicas de manufactura", "asegurar higiene y consistencia en beneficio"),
    ("CIC", "fertilizacion", "capacidad de intercambio cationico del suelo", "entender reserva y retencion de nutrientes"),
    ("CE", "fertilizacion", "conductividad electrica", "detectar riesgo por acumulacion de sales"),
    ("MO", "fertilizacion", "materia organica del suelo", "mejorar estructura y retencion de agua"),
    ("ROI", "general", "retorno sobre la inversion", "priorizar inversiones de mayor impacto"),
    ("pH", "fertilizacion", "medida de acidez o alcalinidad", "ajustar disponibilidad de nutrientes"),
    ("aw", "cosecha", "actividad de agua en cafe", "definir estabilidad de almacenamiento"),
    ("SCA", "general", "criterios de evaluacion sensorial de cafe", "estandarizar lenguaje de calidad"),
    ("MIP", "plagas", "manejo integrado de plagas", "reducir danos con enfoque preventivo"),
    ("SST", "general", "seguridad y salud en trabajo", "proteger personas y continuidad operativa"),
]

for acro, category, meaning, purpose in ACRONYM_CARDS:
    CARDS.append(
        card(
            category,
            [
                f"Que significa {acro} en cafe",
                f"Para que sirve {acro} en caficultura",
                f"Como aplicar {acro} en una finca cafetera",
                f"Importancia de {acro} para productores de cafe",
            ],
            f"En cafe, {acro} se refiere a {meaning}. "
            f"Su valor practico esta en {purpose} para mejorar decisiones en campo y proceso.",
            toks("cafe acronimo", acro, meaning, purpose),
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
    print(f"Entradas nuevas cafe (maxplus): {added}")
    print(f"Total entradas KB: {len(entries)}")
    print(f"Total preguntas KB: {total_q}")


if __name__ == "__main__":
    main()
