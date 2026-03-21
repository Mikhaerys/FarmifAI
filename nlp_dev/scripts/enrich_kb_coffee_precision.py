#!/usr/bin/env python3
"""
Enriquecimiento PRECISION para cafe.
Cubre huecos avanzados: fermentaciones, calidad, torrefaccion, barismo,
agrobiodiversidad y decisiones tecnicas de alto nivel.
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


def make_tokens(*parts: str) -> list[str]:
    seq: list[str] = []
    for p in parts:
        seq.extend([t for t in normalize(p).split() if len(t) >= 3])
    seen: set[str] = set()
    out: list[str] = []
    for t in seq:
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


ADV_FERMENTATIONS = [
    ("fermentacion carbonica", "atmosfera controlada rica en CO2", "diferenciar perfil sensorial con control estricto"),
    ("fermentacion lactica", "microbiota orientada a acidez limpia", "cuidar inocuidad y tiempos"),
    ("fermentacion acetica controlada", "evitar notas avinagradas dominantes", "vigilar pH y temperatura"),
    ("fermentacion anaerobica en tanque", "bajo oxigeno y seguimiento continuo", "trazabilidad minuto a minuto"),
    ("fermentacion en cereza entera", "proceso con fruta completa", "control de temperatura y sanidad"),
    ("fermentacion en pergamino", "procesamiento tras despulpado", "evitar desviaciones por lote"),
    ("fermentacion con levaduras seleccionadas", "inoculacion dirigida de microbiota", "estandarizar dosificacion y limpieza"),
    ("fermentacion espontanea", "microbiota nativa del entorno", "aumentar monitoreo para evitar defectos"),
    ("fermentacion por lotes pequenos", "control detallado de microproceso", "evaluacion sensorial posterior"),
    ("fermentacion escalonada", "etapas con objetivos diferentes", "registro de cada fase"),
    ("fermentacion en frio", "temperaturas moderadas para mayor control", "ajustar tiempos de proceso"),
    ("fermentacion termica", "manejo con ventana de temperatura definida", "evitar sobrecalentamiento"),
    ("fermentacion con recirculacion", "uniformidad de medio fermentativo", "evitar contaminaciones"),
    ("fermentacion con control de brix", "seguimiento de azucares disponibles", "tomar decisiones segun curva"),
    ("fermentacion con control de pH", "seguimiento acido-base del proceso", "detectar desviaciones tempranas"),
    ("fermentacion con control de aw", "estabilidad microbiologica progresiva", "proteger inocuidad"),
    ("fermentacion en bolsas", "microambiente controlado", "limpieza y manejo cuidadoso"),
    ("fermentacion en barrica", "aporte de complejidad si se controla bien", "evitar contaminacion cruzada"),
    ("co-fermentacion controlada", "proceso con coadyuvantes permitidos", "documentar origen y metodologia"),
    ("fermentacion de experimentacion", "ensayo de procesos en pequeno volumen", "comparar con lote testigo"),
]

for method, core, caution in ADV_FERMENTATIONS:
    CARDS.append(
        card(
            "cosecha",
            [
                f"Como hacer {method} en cafe",
                f"Que cuidar en {method} para cafe",
                f"Riesgos de {method} en poscosecha de cafe",
                f"Control de calidad en {method} de cafe",
            ],
            f"En cafe, {method} se basa en {core}. "
            f"Para que sea estable y repetible, conviene {caution} y llevar trazabilidad por lote.",
            make_tokens("cafe fermentacion avanzada", method, core, caution),
        )
    )


PROCESS_METRICS = [
    ("brix en mosto", "dinamica de azucares fermentables", "ajustar punto de corte de fermentacion"),
    ("pH de fermentacion", "evolucion acida del proceso", "detectar desviaciones y riesgo de defecto"),
    ("temperatura de masa", "velocidad microbiologica", "evitar picos no deseados"),
    ("tiempo efectivo de fermentacion", "desarrollo de compuestos sensoriales", "estandarizar protocolo"),
    ("actividad de agua aw", "estabilidad microbiologica", "proteger calidad en almacenamiento"),
    ("humedad final del pergamino", "seguridad de bodega", "evitar moho y deterioro"),
    ("uniformidad de secado", "consistencia entre granos", "mejorar estabilidad de taza"),
    ("curva de secado", "transicion de humedad en el tiempo", "controlar calidad fisica y sensorial"),
    ("ratio de rendimiento", "eficiencia entre cereza y pergamino", "evaluar impacto operativo"),
    ("defectos fisicos por lote", "calidad comercial del grano", "priorizar acciones de mejora"),
    ("score de catacion interno", "resultado sensorial de referencia", "comparar procesos"),
    ("variabilidad interlote", "consistencia del sistema productivo", "estandarizar decisiones"),
    ("tiempo en bodega", "frescura y estabilidad", "rotar inventario"),
    ("consumo de agua por kg", "eficiencia hidrica en beneficio", "optimizar uso del recurso"),
    ("consumo de energia en secado", "costo de proceso", "mejorar eficiencia termica"),
]

for metric, insight, action in PROCESS_METRICS:
    CARDS.append(
        card(
            "cosecha",
            [
                f"Como medir {metric} en cafe",
                f"Para que sirve {metric} en beneficio de cafe",
                f"Como usar {metric} para mejorar calidad de cafe",
                f"Errores comunes al interpretar {metric} en cafe",
            ],
            f"En cafe, {metric} permite entender {insight}. "
            f"Con ese dato puedes {action}, siempre comparando resultados por lote.",
            make_tokens("cafe metrica proceso", metric, insight, action),
        )
    )


CUPPING_CALIBRATION = [
    ("calibracion de catadores", "alinear criterios sensoriales del equipo", "reducir sesgo entre evaluaciones"),
    ("rueda de sabores", "lenguaje comun para describir taza", "mejorar comunicacion tecnica"),
    ("formato de cupping", "registro estandar de atributos", "comparar lotes de forma objetiva"),
    ("muestra de control", "referencia para consistencia", "detectar deriva de evaluacion"),
    ("triangulacion sensorial", "validar diferencias entre lotes", "evitar conclusiones apresuradas"),
    ("control de temperatura de taza", "consistencia de lectura sensorial", "evitar variaciones metodologicas"),
    ("control de molienda", "uniformidad de extraccion", "comparaciones mas justas"),
    ("control de agua en catacion", "repetibilidad del resultado", "reducir ruido del metodo"),
    ("analisis de defectos", "identificar causas de baja calidad", "priorizar correcciones"),
    ("analisis de atributos positivos", "reconocer fortalezas de lote", "replicar buenas practicas"),
    ("tracking de puntajes", "historial de evolucion", "tomar decisiones de mejora continua"),
    ("perfil por origen de lote", "diferenciacion comercial", "segmentar estrategia de venta"),
    ("consistencia semanal", "estabilidad operativa", "anticipar desviaciones"),
    ("cata comparativa de procesos", "evidencia para decidir protocolo", "seleccionar metodo mas robusto"),
    ("retroalimentacion campo-beneficio", "cerrar ciclo tecnico", "conectar manejo agronomico con taza"),
]

for topic, purpose, result in CUPPING_CALIBRATION:
    CARDS.append(
        card(
            "general",
            [
                f"Como hacer {topic} en cafe",
                f"Importancia de {topic} para calidad de cafe",
                f"Que mejora {topic} en la evaluacion de cafe",
                f"Como aplicar {topic} con productores de cafe",
            ],
            f"En cafe, {topic} sirve para {purpose}. "
            f"Bien implementado, permite {result} y mejora decisiones de lote.",
            make_tokens("cafe catacion calidad", topic, purpose, result),
        )
    )


ROAST_BASICS = [
    ("curva de tueste", "trayectoria termica del grano", "adaptarla al perfil del lote"),
    ("punto de primer crack", "hito fisico del tueste", "controlar desarrollo posterior"),
    ("tiempo de desarrollo", "fase final que define expresion sensorial", "evitar sub o sobre desarrollo"),
    ("carga termica inicial", "energia al inicio del tueste", "proteger integridad del grano"),
    ("tasa de aumento de temperatura", "ritmo de avance del tueste", "mantener curva estable"),
    ("tiempo total de tueste", "duracion completa del proceso", "alinear con objetivo de taza"),
    ("enfriado rapido", "detencion de reacciones", "fijar perfil logrado"),
    ("reposo post-tueste", "desgasificacion controlada", "mejorar estabilidad en preparacion"),
    ("molienda para filtrado", "granulometria para extraccion limpia", "ajustar segun metodo"),
    ("molienda para espresso", "granulometria fina para extraccion concentrada", "calibrar por flujo y sabor"),
    ("uniformidad de molienda", "consistencia de extraccion", "reducir variabilidad de taza"),
    ("perfil claro", "resaltar acidez y notas aromaticas", "evitar subdesarrollo"),
    ("perfil medio", "balance entre acidez, dulzor y cuerpo", "buscar versatilidad"),
    ("perfil oscuro", "mayor desarrollo termico", "evitar notas quemadas"),
    ("control de color de tueste", "referencia visual de desarrollo", "estandarizar produccion"),
]

for topic, base, objective in ROAST_BASICS:
    CARDS.append(
        card(
            "general",
            [
                f"Que es {topic} en cafe",
                f"Como manejar {topic} para cafe de calidad",
                f"Errores en {topic} al tostar cafe",
                f"Para que sirve {topic} en torrefaccion de cafe",
            ],
            f"En cafe, {topic} se relaciona con {base}. "
            f"Su manejo adecuado ayuda a {objective} segun el perfil del lote.",
            make_tokens("cafe torrefaccion", topic, base, objective),
        )
    )


BREW_BASICS = [
    ("ratio cafe-agua", "balance de concentracion y sabor", "ajustar segun objetivo de taza"),
    ("tiempo de extraccion", "cantidad de compuestos extraidos", "evitar subextraccion o sobreextraccion"),
    ("temperatura de agua", "solubilidad de compuestos", "controlar expresion sensorial"),
    ("calidad de agua", "composicion mineral del preparado", "mejorar claridad de taza"),
    ("agitación", "uniformidad de contacto agua-cafe", "estabilizar extraccion"),
    ("tamano de molienda", "velocidad de extraccion", "afinar metodo"),
    ("preinfusion", "humectacion inicial del lecho", "mejorar consistencia"),
    ("rendimiento de extraccion", "porcentaje de solubles extraidos", "diagnosticar preparacion"),
    ("TDS", "concentracion de solubles en bebida", "calibrar receta"),
    ("flujo en espresso", "dinamica de extraccion bajo presion", "lograr taza balanceada"),
    ("distribucion en portafiltro", "homogeneidad del puck", "reducir canalizacion"),
    ("tampeo", "compactacion del cafe molido", "estabilizar flujo"),
    ("canalizacion", "paso preferencial de agua", "corregir tecnica y molienda"),
    ("receta base de filtrado", "parametros iniciales de preparacion", "ajustar al perfil del lote"),
    ("receta base de espresso", "parametros de referencia en maquina", "calibrar servicio"),
]

for topic, meaning, use in BREW_BASICS:
    CARDS.append(
        card(
            "general",
            [
                f"Como controlar {topic} en cafe",
                f"Que significa {topic} al preparar cafe",
                f"Como mejorar {topic} en barismo de cafe",
                f"Errores comunes con {topic} en preparacion de cafe",
            ],
            f"En preparacion de cafe, {topic} define {meaning}. "
            f"Dominarlo permite {use} y mayor consistencia en taza.",
            make_tokens("cafe barismo preparacion", topic, meaning, use),
        )
    )


AGROBIODIVERSITY_TOPICS = [
    ("agrobiodiversidad", "diversidad funcional en sistema cafetero", "resiliencia ecologica y productiva"),
    ("corredores biologicos", "conectividad para fauna util", "servicios ecosistemicos en finca"),
    ("enemigos naturales", "control biologico de plagas", "reduccion de presion sanitaria"),
    ("polinizadores", "apoyo a procesos reproductivos", "estabilidad del agroecosistema"),
    ("diversidad de sombra", "modulacion de microclima", "adaptacion al cambio climatico"),
    ("cobertura viva diversa", "proteccion de suelo y habitat", "menor erosion y mejor infiltracion"),
    ("setos vivos", "barreras ecologicas y funcionales", "proteccion de lotes y biodiversidad"),
    ("areas de conservacion", "refugio de especies utiles", "equilibrio del sistema"),
    ("manejo de borde", "transicion entre lote y entorno", "reduccion de riesgos"),
    ("reciclaje de biomasa", "retorno de carbono al suelo", "mejor salud edafica"),
    ("servicios ecosistemicos", "beneficios de procesos naturales", "menor dependencia de insumos"),
    ("diversificacion productiva", "fuentes multiples de ingreso", "menor vulnerabilidad economica"),
    ("restauracion de suelos", "recuperacion de funcion productiva", "sostenibilidad del cafetal"),
    ("paisaje cafetero resiliente", "integracion de produccion y conservacion", "estabilidad a largo plazo"),
    ("indicadores de biodiversidad", "medicion de estado ecologico", "toma de decisiones informada"),
]

for topic, concept, benefit in AGROBIODIVERSITY_TOPICS:
    CARDS.append(
        card(
            "cultivo",
            [
                f"Que es {topic} en cafe",
                f"Como aplicar {topic} en finca cafetera",
                f"Beneficios de {topic} para caficultura",
                f"Que medir para mejorar {topic} en cafe",
            ],
            f"En caficultura, {topic} se refiere a {concept}. "
            f"Su implementacion aporta {benefit} y fortalece el sistema productivo.",
            make_tokens("cafe biodiversidad agroecologia", topic, concept, benefit),
        )
    )


ROOT_CAUSE_VARIANTS = [
    ("produccion alta pero margen bajo", "costos ocultos, ineficiencia de proceso o venta sin diferenciacion"),
    ("calidad alta pero volumen bajo", "limitantes de manejo agronomico y renovacion"),
    ("volumen alto pero taza baja", "falta de control en cosecha y beneficio"),
    ("buen manejo de campo pero defectos en bodega", "brecha de control poscosecha"),
    ("buen cupping interno pero rechazo comercial", "falta de estandarizacion de entrega"),
    ("incidencia sanitaria repetitiva", "manejo reactivo y no preventivo"),
    ("mucha variacion entre lotes vecinos", "falta de sectorizacion tecnica"),
    ("finca con buen potencial sin mejora real", "ausencia de seguimiento de indicadores"),
    ("inversion alta sin retorno", "priorizacion incorrecta de recursos"),
    ("adopcion baja de recomendaciones", "falta de acciones simples y medibles"),
    ("problemas recurrentes en temporada de lluvia", "drenaje, ventilacion y protocolos insuficientes"),
    ("problemas recurrentes en temporada seca", "manejo hidrico y cobertura insuficientes"),
    ("equipo tecnico desalineado", "criterios distintos y poca calibracion"),
    ("cosecha desordenada", "falta de plan operativo y roles claros"),
    ("beneficio inconsistente", "protocolos no estandarizados"),
    ("feedback positivo sin mejora productiva", "acciones no aterrizadas en campo"),
]

for symptom, likely in ROOT_CAUSE_VARIANTS:
    CARDS.append(
        card(
            "diagnostico",
            [
                f"En cafe tengo {symptom}, como lo diagnostico",
                f"Causas de {symptom} en finca cafetera",
                f"Plan tecnico para corregir {symptom} en cafe",
                f"Que indicadores revisar si hay {symptom} en cafe",
            ],
            f"Cuando en cafe aparece {symptom}, suele deberse a {likely}. "
            f"La mejor ruta es definir causa prioritaria por lote, ejecutar una accion concreta y medir resultado en corto plazo.",
            make_tokens("cafe diagnostico gestion", symptom, likely),
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
    print(f"Entradas nuevas cafe (precision): {added}")
    print(f"Total entradas KB: {len(entries)}")
    print(f"Total preguntas KB: {total_q}")


if __name__ == "__main__":
    main()

