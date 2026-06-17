from __future__ import annotations

import sys
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.datos import load_dataset, repo_root
from app.defensa import narrativa_markdown
from app.graficos import CHAPTER_ORDER, ChartGuide, chart_guides
from app.metricas import MetricResult, compute_metrics


ROOT = repo_root()
CASE_ID = "tecnohogar"
NOTES_DIR = ROOT / "docs" / "notas"
GRAPHICS_DIR = NOTES_DIR / "assets" / "graficos"


CHAPTER_STUDY = {
    "5 - Controles Organizativos": {
        "foco": "gobierno, políticas, roles, activos, proveedores, incidentes, continuidad, cumplimiento y mejora.",
        "aplicado": "se usó para evaluar si TecnoHogar tiene responsabilidades claras, inventario y clasificación de información, gestión de accesos, relación con proveedores, preparación ante incidentes, continuidad y cumplimiento.",
        "defensa": "este capítulo explica la parte de gobierno del tablero: sin políticas, roles, activos y responsables, los controles técnicos quedan aislados.",
    },
    "6 - Controles de Personas": {
        "foco": "ciclo de vida laboral, concientización, confidencialidad, trabajo remoto, desvinculación y reporte de eventos.",
        "aplicado": "se usó para medir prácticas de Recursos Humanos (RRHH) y usuarios: verificación de antecedentes, términos de empleo, capacitación, acuerdos de confidencialidad, teletrabajo y canales de reporte.",
        "defensa": "este capítulo muestra que seguridad no es sólo tecnología; las personas pueden reducir o amplificar la exposición del negocio.",
    },
    "7 - Controles Físicos": {
        "foco": "perímetros, ingresos, oficinas, salas, instalaciones, equipamiento, cableado, almacenamiento y mantenimiento.",
        "aplicado": "se usó para evaluar oficinas, depósito, centros de distribución, protección de equipos, control de ingreso físico, áreas seguras y soporte ambiental.",
        "defensa": "este capítulo conecta seguridad de la información con el mundo físico: si se comprometen equipos, medios o instalaciones, también se compromete la información.",
    },
    "8 - Controles Tecnológicos": {
        "foco": "endpoints, accesos privilegiados, autenticación, malware, vulnerabilidades, configuración, backup, logs, redes, criptografía y desarrollo seguro.",
        "aplicado": "se usó para medir la postura técnica del e-commerce y la operación: hardening, gestión de identidades y accesos (IAM), autenticación multifactor (MFA), registros, monitoreo, vulnerabilidades, segregación de redes, ciclo de vida de desarrollo seguro (SDLC seguro) y protección de aplicaciones.",
        "defensa": "este capítulo concentra muchos controles operativos y por eso es clave para explicar brechas técnicas, monitoreo, vulnerabilidades y seguridad de aplicaciones.",
    },
}


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def export_graphics(result: MetricResult, guides: list[ChartGuide]) -> None:
    GRAPHICS_DIR.mkdir(parents=True, exist_ok=True)
    for guide in guides:
        fig = guide.factory(result, None)
        fig.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff")
        output = GRAPHICS_DIR / guide.filename
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                fig.write_image(str(output), width=1280, height=720, scale=2)
        except Exception as exc:
            raise RuntimeError(
                "No se pudieron exportar los gráficos. Ejecutá `pip install -r requirements.txt` "
                "para instalar Kaleido y volvé a correr `make notas`."
            ) from exc


def render_graph_guide(result: MetricResult, guides: list[ChartGuide]) -> str:
    resumen = result.resumen
    effort = int(resumen["esfuerzo_total"])
    lines = [
        "# Guía de gráficos del tablero",
        "",
        "Esta guía explica cada gráfico visual del tablero de TecnoHogar. Cada screenshot se genera desde las mismas funciones Plotly que usa Streamlit, por eso sirve como plan B para la defensa si la demo en vivo falla. Si aparece una sigla, buscarla en `glosario-abreviaturas.md`.",
        "",
        f"Valores base del caso: **{resumen['controles_evaluados']} controles**, **{resumen['madurez_global_pct']}% madurez**, **{resumen['brecha_global_pct']}% brecha**, **{resumen['proyectos']} iniciativas**, **{resumen['quick_wins']} quick wins** y **{effort} jornadas**.",
        "",
    ]
    for guide in guides:
        lines.extend(
            [
                f"## {guide.title}",
                "",
                f"![{guide.title}](assets/graficos/{guide.filename})",
                "",
                f"**Dónde aparece:** Tab {guide.tab}, sección {guide.section}.",
                "",
                f"**Para qué sirve:** {guide.purpose}",
                "",
                f"**Base teórica:** {guide.theory}",
                "",
                f"**Cómo se lee:** {guide.reading}",
                "",
                f"**Qué dicen los datos de TecnoHogar:** {guide.insight(result)}",
                "",
                f"**Cómo explicarlo en la defensa:** {guide.defense}",
                "",
                f"**Pregunta probable:** {guide.question}",
                "",
                f"**Respuesta sugerida:** {guide.answer}",
                "",
            ]
        )
    return "\n".join(lines)


def render_readme(result: MetricResult, guides: list[ChartGuide]) -> str:
    resumen = result.resumen
    effort = int(resumen["esfuerzo_total"])
    return f"""# Notas de defensa TP2

Este directorio es el paquete de estudio para defender el tablero de control de seguridad. Está pensado para preparar la presentación, entender cada gráfico y tener un plan B si la demo en vivo no funciona.

## Orden recomendado

1. Leer `glosario-abreviaturas.md` para tener a mano qué significa cada sigla o abreviatura.
2. Leer `conceptos-clave.md` para entender la lógica completa, desde seguridad de la información hasta tablero, brechas y plan.
3. Leer `iso-27002-guia.md` para estudiar la norma aplicada, los capítulos 5 a 8 y cómo se usaron en TecnoHogar.
4. Leer `narrativa-presentacion.md` para practicar la historia slide por slide.
5. Leer `guia-graficos.md` para entender qué dice cada gráfico y cómo responder preguntas.
6. Leer `demo-en-vivo.md` para practicar el recorrido del tablero y preparar el plan B.

## Números que conviene recordar

- Madurez global: **{resumen['madurez_global_pct']}%**.
- Brecha global: **{resumen['brecha_global_pct']}%**.
- Controles evaluados: **{resumen['controles_evaluados']}**.
- Iniciativas del plan: **{resumen['proyectos']}**.
- Quick wins: **{resumen['quick_wins']}**.
- Esfuerzo total estimado: **{effort} jornadas**.
- Gráficos documentados: **{len(guides)}**.

## Idea central de la defensa

El tablero no es solamente una visualización. Es una forma de convertir el contexto de TecnoHogar en una cadena defendible: **activo y proceso -> control ISO -> evidencia -> nivel CMMI -> brecha -> proyecto -> seguimiento**.
"""


def render_glossary() -> str:
    return """# Glosario de abreviaturas

Esta lista reúne las abreviaturas que aparecen en las notas, el tablero, los datos o la defensa. No hace falta recitarlas todas, pero sí conviene poder explicar las principales si aparecen en una pregunta.

| Abreviatura | Significado | Cómo entenderla en este trabajo |
| --- | --- | --- |
| API | Application Programming Interface, interfaz de programación de aplicaciones | Forma en que sistemas o aplicaciones se comunican entre sí. Aparece asociada a seguridad de aplicaciones e integración. |
| CID | Confidencialidad, Integridad y Disponibilidad | Tres propiedades básicas para valorar activos y controles de seguridad de la información. |
| CI | Continuous Integration, integración continua | Automatización que valida y construye el proyecto cuando se sube código. |
| CD | Continuous Delivery/Deployment, entrega o despliegue continuo | Automatización que publica o deja listo el resultado luego de pasar validaciones. En este repo aplica al deploy del tablero y entregables. |
| CI/CD | Continuous Integration / Continuous Delivery, integración continua y entrega continua | Forma corta de hablar del pipeline completo: validar, construir y publicar resultados automáticamente. |
| CMMI | Capability Maturity Model Integration | Modelo de madurez usado como escala 0 a 5 para medir qué tan implementado está cada control. |
| CSF | Critical Success Factor, factor crítico de éxito | Condición clave que debe cumplirse para que la gestión de seguridad funcione. |
| CSV | Comma-Separated Values, valores separados por coma | Formato simple de datos tabulares usado como fuente del tablero. |
| HTML | HyperText Markup Language | Formato web usado para algunas salidas, como slides Reveal.js o informe HTML. |
| IAM | Identity and Access Management, gestión de identidades y accesos | Prácticas y herramientas para administrar usuarios, permisos y autenticación. |
| IEC | International Electrotechnical Commission | Organismo internacional que publica normas junto con ISO. |
| ISO | International Organization for Standardization | Organización internacional de normalización. En el trabajo se usa la familia ISO/IEC 27000. |
| ISO/IEC | International Organization for Standardization / International Electrotechnical Commission | Forma conjunta en que se publican normas como ISO/IEC 27001 e ISO/IEC 27002. |
| KGI | Key Goal Indicator, indicador clave de resultado | Indicador que dice si se alcanzó un objetivo. Ejemplo: madurez global. |
| KPI | Key Performance Indicator, indicador clave de desempeño | Indicador usado para seguir desempeño o avance. Ejemplo: brecha por capítulo o avance del plan. |
| KPI/KGI | Key Performance Indicator / Key Goal Indicator | Par de indicadores usado para separar seguimiento del desempeño y resultado final esperado. |
| MFA | Multi-Factor Authentication, autenticación multifactor | Uso de más de un factor para validar identidad, por ejemplo contraseña más código o aplicación móvil. |
| PDF | Portable Document Format | Formato final del informe descargable. |
| PII | Personally Identifiable Information, información de identificación personal | Datos que pueden identificar a una persona. Se vincula con privacidad y protección de datos. |
| PNG | Portable Network Graphics | Formato de imagen usado para los screenshots de gráficos en las notas. |
| PPTX | Formato de presentación de Microsoft PowerPoint | Formato final de la presentación descargable. |
| RRHH | Recursos Humanos | Área/proceso asociado a controles de personas: altas, bajas, capacitación, confidencialidad y desvinculación. |
| S.A. | Sociedad Anónima | Tipo societario usado en el nombre TecnoHogar S.A. |
| SDLC | Software Development Life Cycle, ciclo de vida de desarrollo de software | Proceso de diseño, construcción, prueba y mantenimiento de software. En seguridad se habla de SDLC seguro. |
| SGSI | Sistema de Gestión de Seguridad de la Información | Sistema de gestión para dirigir, medir y mejorar seguridad de la información. ISO 27001 define requisitos para un SGSI. |
| SI | Seguridad de la Información | Protección de la información y sus propiedades: confidencialidad, integridad y disponibilidad. |
| SMART | Specific, Measurable, Achievable, Relevant, Time-bound | Criterios para que un indicador sea específico, medible, alcanzable, relevante y temporal. |
| TIC | Tecnologías de la Información y las Comunicaciones | Sistemas, infraestructura, redes, aplicaciones y servicios tecnológicos. |
| TP | Trabajo Práctico | Entrega académica de la materia. |
| URL | Uniform Resource Locator | Dirección web, por ejemplo la URL del tablero Streamlit. |
| WAF | Web Application Firewall, firewall de aplicaciones web | Control para filtrar y proteger tráfico hacia aplicaciones web. |

## Las siglas más importantes para defender

Si hay poco tiempo, priorizar estas:

- **ISO/IEC 27002:** catálogo de controles usado como referencia.
- **CMMI:** escala de madurez 0 a 5 que usamos para medir controles.
- **CID:** confidencialidad, integridad y disponibilidad.
- **SGSI:** sistema de gestión de seguridad de la información.
- **KPI/KGI:** indicadores de desempeño y de resultado.
- **SI:** seguridad de la información.
"""


def render_iso_guide(result: MetricResult) -> str:
    resumen = result.resumen
    controls = result.controles.copy()
    chapters = result.capitulos.set_index("capitulo")
    top_gaps = result.top_brechas.copy().head(10)

    lines = [
        "# Guía ISO/IEC 27002:2022 para la defensa",
        "",
        "Esta guía resume lo que conviene saber de ISO/IEC 27002:2022 para defender el tablero. No reemplaza a la norma oficial: sirve para explicar qué es, qué parte usamos y cómo se tradujo en métricas, brechas y proyectos dentro del caso TecnoHogar. Para siglas y abreviaturas, usar `glosario-abreviaturas.md`.",
        "",
        "## Qué tenés que poder decir en 30 segundos",
        "",
        "ISO/IEC 27002:2022 es un catálogo de controles de seguridad de la información. En este TP la usamos como **estructura de referencia**: cada control se convirtió en una unidad evaluable, se le asignó una madurez CMMI, se calculó una brecha y se vinculó con proyectos de mejora. Para TecnoHogar se evaluaron los **93 controles** de los capítulos **5 Organizativos**, **6 Personas**, **7 Físicos** y **8 Tecnológicos**.",
        "",
        "## ISO 27001 vs ISO 27002",
        "",
        "- **ISO/IEC 27001** define requisitos para un SGSI y es la norma típica contra la que una organización puede certificarse.",
        "- **ISO/IEC 27002** es una guía/catálogo de controles. No certifica por sí sola; ayuda a seleccionar, implementar e interpretar controles.",
        "- En este trabajo no hacemos una certificación. Hacemos un **tablero de control** basado en controles ISO 27002, con medición de madurez y plan de mejora.",
        "",
        "## Qué parte de ISO aplicamos",
        "",
        f"- Estándar del tablero: **{resumen['estandar_id']}**.",
        f"- Caso principal: **{resumen['empresa_nombre']}**.",
        f"- Controles evaluados: **{resumen['controles_evaluados']}**.",
        f"- Capítulos evaluados: **{resumen['capitulos_evaluados']}**.",
        "- Unidad de análisis: cada control ISO es una métrica/control evaluable.",
        "- Capa de medición agregada por nosotros: nivel Capability Maturity Model Integration (CMMI), madurez, brecha, peso, brecha ponderada, hallazgo, evidencia y proyecto asociado.",
        "- Atributos usados para vistas transversales: tipo preventivo/detectivo/correctivo, confidencialidad, integridad y disponibilidad (CID), funciones de ciberseguridad, capacidades operacionales y dominios ejecutivos.",
        "",
        "## Resumen por capítulo",
        "",
        "| Capítulo | Controles | Madurez | Brecha | Qué representa |",
        "| --- | ---: | ---: | ---: | --- |",
    ]

    for chapter in CHAPTER_ORDER:
        row = chapters.loc[chapter]
        study = CHAPTER_STUDY[chapter]
        lines.append(
            f"| {chapter} | {int(row['controles'])} | {float(row['madurez_pct']):.1f}% | {float(row['brecha_pct']):.1f}% | {study['foco']} |"
        )

    lines.extend(
        [
            "",
            "## Cómo defender cada capítulo",
            "",
        ]
    )

    for chapter in CHAPTER_ORDER:
        row = chapters.loc[chapter]
        study = CHAPTER_STUDY[chapter]
        chapter_controls = controls[controls["capitulo"] == chapter].sort_values("peso_brecha", ascending=False).head(5)
        lines.extend(
            [
                f"### {chapter}",
                "",
                f"**Qué cubre:** {study['foco']}",
                "",
                f"**Qué aplicamos en TecnoHogar:** {study['aplicado']}",
                "",
                f"**Lectura del tablero:** {int(row['controles'])} controles, madurez **{float(row['madurez_pct']):.1f}%** y brecha **{float(row['brecha_pct']):.1f}%**.",
                "",
                f"**Cómo explicarlo:** {study['defensa']}",
                "",
                "**Controles concretos para tener presentes:**",
                "",
            ]
        )
        for control in chapter_controls.itertuples(index=False):
            lines.append(
                f"- **{control.control_id} - {control.control_nombre}:** madurez {float(control.cumplimiento_pct):.1f}%, brecha ponderada {float(control.peso_brecha):.2f}. Hallazgo: {control.hallazgo}"
            )
        lines.append("")

    lines.extend(
        [
            "## Controles que más tenés que saber explicar",
            "",
            "Estos son los controles que aparecen arriba en el ranking de brecha ponderada. No son los únicos importantes, pero sí los más probables para preguntas porque justifican prioridades del plan.",
            "",
            "| Control | Capítulo | Madurez | Brecha ponderada | Interpretación |",
            "| --- | --- | ---: | ---: | --- |",
        ]
    )
    for control in top_gaps.itertuples(index=False):
        lines.append(
            f"| {control.control_id} - {control.control_nombre} | {control.capitulo} | {float(control.cumplimiento_pct):.1f}% | {float(control.peso_brecha):.2f} | {control.hallazgo} |"
        )

    lines.extend(
        [
            "",
            "## Cómo convertimos ISO en datos",
            "",
            "1. **Catálogo:** `datos/estandares/iso27002_2022/catalogo_controles.csv` define los controles, capítulo, nombre, propósito, pregunta de evaluación, atributos, peso y mapeos auxiliares.",
            "2. **Diagnóstico:** `datos/casos/tecnohogar/diagnostico.csv` asigna nivel Capability Maturity Model Integration (CMMI), hallazgo, observaciones, fuente y entrevistado por control.",
            "3. **Métrica:** el motor calcula madurez, brecha y brecha ponderada.",
            "4. **Plan:** `datos/casos/tecnohogar/proyectos.csv` define iniciativas, esfuerzo, plazo y aporte esperado.",
            "5. **Trazabilidad:** `datos/casos/tecnohogar/proyecto_control.csv` vincula controles ISO con proyectos concretos.",
            "",
            "## Cómo se relaciona ISO con CMMI",
            "",
            "ISO 27002 aporta el catálogo y dice **qué controles mirar**. Capability Maturity Model Integration (CMMI) nos da una escala para expresar **qué tan maduro está cada control**. Por eso no decimos que ISO tenga niveles 0 a 5; esa escala la agregamos nosotros para transformar el catálogo en indicadores de tablero.",
            "",
            "## Qué significa aplicar un control",
            "",
            "En este tablero, aplicar un control no significa que TecnoHogar ya lo cumple. Significa que el control es relevante para el caso, fue incluido en el universo evaluado y recibió una medición de madurez. Después, si la madurez es baja, aparece como brecha y puede disparar un proyecto.",
            "",
            "## Qué NO conviene decir",
            "",
            "- No decir que ISO 27002 certifica a TecnoHogar.",
            "- No decir que el tablero demuestra cumplimiento legal completo.",
            "- No decir que CMMI es parte textual de ISO 27002.",
            "- No decir que todos los controles tienen la misma importancia: por eso usamos peso y brecha ponderada.",
            "- No recitar los 93 controles: conviene explicar estructura, capítulos, controles críticos y trazabilidad.",
            "",
            "## Preguntas probables sobre ISO",
            "",
            "**¿Por qué eligieron ISO 27002?**",
            "",
            "Porque es un catálogo reconocido de controles de seguridad de la información y permite cubrir gobierno, personas, seguridad física y tecnología en una misma estructura.",
            "",
            "**¿Evaluaron toda la norma?**",
            "",
            f"Para el tablero se evaluaron los {resumen['controles_evaluados']} controles cargados de los capítulos 5 a 8 de ISO/IEC 27002:2022. Es el universo definido para este TP.",
            "",
            "**¿Esto es una auditoría ISO?**",
            "",
            "No. Es un diagnóstico académico/profesional basado en controles ISO. Una auditoría formal requeriría evidencia real validada, alcance aprobado, criterios de auditoría y posiblemente ISO 27001 si se busca certificación del SGSI.",
            "",
            "**¿Por qué no muestran todos los controles en la presentación?**",
            "",
            "Porque la presentación cuenta una historia ejecutiva. Los 93 controles están en el tablero y en la trazabilidad; las slides muestran los patrones y prioridades.",
            "",
            "**¿Dónde se ve qué aplicaron de cada control?**",
            "",
            "En el tablero: Mapa ISO muestra controles por capítulo, Brechas muestra los controles con mayor distancia, Trazabilidad conecta control con proyecto y Descargas permite bajar los CSV.",
            "",
            "**¿Qué pasa si cambia el estándar o el caso?**",
            "",
            "El repo separa estándar, caso, diagnóstico y proyectos. Para otro caso se cargan nuevos CSV con el mismo formato y se regeneran tablero, informe, slides y notas.",
            "",
            "## Checklist de estudio antes de defender",
            "",
            "- Saber explicar la diferencia entre ISO 27001 e ISO 27002.",
            "- Saber nombrar los cuatro capítulos usados: 5 Organizativos, 6 Personas, 7 Físicos y 8 Tecnológicos.",
            "- Saber decir que ISO aporta el catálogo y CMMI aporta la escala de madurez.",
            "- Saber explicar por qué hay 93 controles y dónde se ven en el tablero.",
            "- Saber conectar capítulo -> control -> hallazgo -> brecha -> proyecto.",
            "- Saber defender que la brecha ponderada prioriza mejor que mirar sólo porcentaje de brecha.",
            "- Saber decir que el tablero no certifica, pero sí ordena diagnóstico, priorización y seguimiento.",
        ]
    )
    return "\n".join(lines)


def render_concepts(result: MetricResult) -> str:
    resumen = result.resumen
    return f"""# Conceptos clave

Esta nota está escrita para estudiar desde cero. La idea es entender primero la lógica general y después conectar cada concepto con el tablero de TecnoHogar.

Para siglas y abreviaturas, leer también `glosario-abreviaturas.md`.

## 1. Qué estamos tratando de proteger

La seguridad de la información busca proteger la información que una organización necesita para operar. En TecnoHogar eso incluye datos de clientes, ventas, e-commerce, inventario, proveedores, accesos, sistemas internos y continuidad del negocio.

La forma clásica de explicar esa protección es **CID**:

- **Confidencialidad:** que la información no sea vista por quien no corresponde.
- **Integridad:** que la información no sea modificada de forma indebida o accidental.
- **Disponibilidad:** que la información y los sistemas estén accesibles cuando el negocio los necesita.

En el TP1 usamos CID para entender activos. En el TP2 usamos controles ISO para medir qué tan protegida está esa información.

## 2. Qué es ISO/IEC 27002:2022 en este trabajo

**ISO/IEC 27002:2022** es un catálogo de controles de seguridad de la información. No lo usamos como certificación, sino como lista ordenada de cosas que conviene mirar.

La idea simple es:

1. ISO 27002 nos dice **qué controles evaluar**.
2. El caso TecnoHogar nos da contexto de negocio.
3. Nosotros asignamos un nivel de madurez a cada control.
4. El tablero calcula brechas, prioridades y proyectos.

Para TecnoHogar evaluamos **{resumen['controles_evaluados']} controles** de los capítulos:

- **5 - Organizativos:** gobierno, políticas, roles, proveedores, incidentes, continuidad y cumplimiento.
- **6 - Personas:** empleados, capacitación, confidencialidad, trabajo remoto y desvinculación.
- **7 - Físicos:** oficinas, accesos físicos, equipos, salas, instalaciones y soportes.
- **8 - Tecnológicos:** endpoints, accesos, redes, logs, vulnerabilidades, backup, criptografía y desarrollo seguro.

La explicación completa de ISO está en `iso-27002-guia.md`.

## 3. Qué es un control

Un **control** es una práctica, proceso, medida técnica o regla de gestión que ayuda a reducir una exposición de seguridad.

Ejemplos:

- Tener política de seguridad.
- Revisar accesos de usuarios.
- Hacer backups.
- Registrar eventos en logs.
- Capacitar a empleados.
- Proteger físicamente oficinas y equipos.

En el tablero, cada control ISO se convirtió en una unidad evaluable. Por eso cuando decimos “93 controles” estamos diciendo que medimos 93 puntos concretos del catálogo.

## 4. Qué significa madurez

La **madurez** responde esta pregunta: “qué tan instalado y controlado está este control en la organización”.

No alcanza con que algo exista de forma informal. Un control maduro debería estar definido, repetirse, tener responsables, evidencia, medición y mejora.

Usamos una escala tipo **CMMI** de 0 a 5:

- **0 - Inexistente:** no hay práctica identificable.
- **1 - Inicial:** existe algo informal o reactivo.
- **2 - Gestionado:** se hace de forma repetible, pero todavía limitada.
- **3 - Definido:** hay proceso documentado y más consistente.
- **4 - Cuantitativo:** se mide con indicadores.
- **5 - Optimizado:** se revisa y mejora de forma continua.

Importante para defender: CMMI no es “la ISO”. ISO nos da los controles; CMMI es la escala que usamos para medirlos.

## 5. Qué es una medida y qué es una métrica

Una **medida** es un dato base. Por ejemplo:

- nivel CMMI de un control;
- peso del control;
- cantidad de controles evaluados;
- esfuerzo estimado en jornadas;
- cantidad de proyectos.

Una **métrica** es un cálculo o lectura que se obtiene usando medidas. Por ejemplo:

- madurez global;
- brecha global;
- brecha ponderada;
- prioridad de proyecto;
- madurez por capítulo.

Ejemplo simple: si un control tiene nivel CMMI bajo, eso es una medida. Cuando calculamos cuánto falta para llegar al objetivo, eso ya es una métrica de brecha.

## 6. Qué es brecha

La **brecha** es la distancia entre la situación actual y el objetivo esperado.

En el tablero usamos esta idea:

- si un control está muy maduro, la brecha es baja;
- si un control está poco maduro, la brecha es alta.

En TecnoHogar, la madurez global es **{resumen['madurez_global_pct']}%** y la brecha global es **{resumen['brecha_global_pct']}%**.

Cómo explicarlo en voz alta:

“No estamos diciendo que TecnoHogar no tenga nada. Estamos diciendo que, frente a un objetivo optimizado, todavía falta formalización, medición y mejora continua”.

## 7. Qué es brecha ponderada

La **brecha ponderada** evita tratar todos los controles como si pesaran igual.

Dos controles pueden tener la misma brecha porcentual, pero no necesariamente tienen el mismo impacto para el diagnóstico. Por eso multiplicamos la brecha por un peso del control.

Idea simple:

```text
brecha ponderada = brecha * peso del control
```

Esto ayuda a ordenar prioridades. En vez de mirar solamente “qué control está peor”, miramos “qué control combina mala madurez con mayor peso relativo”.

## 8. Qué son KPI, KGI y CSF

Estas siglas aparecen mucho cuando se habla de métricas y tablero:

- **KPI - Key Performance Indicator:** indicador clave de desempeño. Sirve para seguir cómo viene la gestión. Ejemplo: brecha por capítulo o avance de proyectos.
- **KGI - Key Goal Indicator:** indicador clave de resultado. Sirve para ver si se alcanzó un objetivo. Ejemplo: madurez global.
- **CSF - Critical Success Factor:** factor crítico de éxito. Es algo que debe funcionar para que el objetivo se cumpla. Ejemplo: que haya responsables definidos para sostener el plan.

Forma fácil de recordarlo:

- KPI mira el camino.
- KGI mira el resultado.
- CSF marca condiciones necesarias para que el camino funcione.

## 9. Qué significa SMART

SMART es una regla práctica para armar buenos indicadores:

- **Specific - específico:** debe decir claramente qué mide.
- **Measurable - medible:** debe poder calcularse.
- **Achievable - alcanzable:** debe ser realista.
- **Relevant - relevante:** debe importar para la gestión.
- **Time-bound - temporal:** debe poder revisarse en un período.

En este repo intentamos que los indicadores sean defendibles porque salen de CSV, fórmulas y generación automática, no de celdas editadas a mano.

## 10. Qué es un tablero de control de seguridad

Un **tablero de control de seguridad** sirve para convertir muchos datos técnicos en una lectura útil para decidir.

Debe permitir dos movimientos:

1. **Subir a una lectura ejecutiva:** madurez global, brecha global, quick wins, plan.
2. **Bajar al detalle:** capítulo, control, hallazgo, evidencia, proyecto y trazabilidad.

Por eso el tablero no es solamente “gráficos lindos”. Es una herramienta para gobernar seguridad: mirar estado, priorizar, ejecutar y volver a medir.

## 11. Qué es riesgo

El **riesgo** aparece cuando hay algo valioso que puede verse afectado por una amenaza aprovechando una debilidad.

En forma simple:

```text
activo importante + amenaza + vulnerabilidad = riesgo
```

El tablero no calcula riesgo formal con probabilidad e impacto monetario. Lo que hace es mostrar señales de exposición: controles débiles, brechas ponderadas y capacidades poco maduras.

Esa lectura ayuda a decidir tratamientos.

## 12. Qué es tratamiento de riesgo

El **tratamiento** es qué hacemos frente a un riesgo o debilidad.

Opciones típicas:

- **Reducir:** implementar controles o mejorar procesos.
- **Transferir:** pasar parte del impacto a un tercero, por ejemplo seguro o contrato.
- **Aceptar:** asumir el riesgo si está dentro del apetito de la organización.
- **Evitar:** dejar de hacer la actividad que genera el riesgo.

En nuestro TP, el foco está en **reducir** brechas mediante proyectos de mejora.

## 13. Qué es Pareto de brechas

El **Pareto** ordena los controles que más explican la brecha ponderada.

Sirve para responder:

“Si no puedo mejorar todo al mismo tiempo, ¿por dónde empiezo?”

En el gráfico, las barras muestran brecha ponderada y la línea muestra acumulado. La idea es encontrar los controles que más aportan al problema total.

## 14. Qué es matriz impacto / esfuerzo

La matriz impacto / esfuerzo ayuda a priorizar proyectos.

- Alto impacto y bajo esfuerzo: **quick win**.
- Alto impacto y alto esfuerzo: proyecto estratégico.
- Bajo impacto y bajo esfuerzo: mejora táctica.
- Bajo impacto y alto esfuerzo: diferir o revisar.

Esto evita que el plan sea una lista arbitraria. Ordena acciones según valor esperado y capacidad de ejecución.

## 15. Qué es un quick win

Un **quick win** no es una acción menor ni cosmética. Es una acción con buen retorno inicial: aporta mucho frente al esfuerzo relativo que requiere.

TecnoHogar tiene **{resumen['quick_wins']} quick wins**.

Cómo explicarlo:

“Elegimos quick wins para mostrar avance temprano y reducir brechas visibles, pero el plan también incluye proyectos más estructurales”.

## 16. Qué es trazabilidad

La **trazabilidad** es poder seguir el camino completo de una decisión.

En el tablero, la cadena es:

```text
control ISO -> evidencia/hallazgo -> madurez -> brecha -> proyecto
```

Esto es clave para defender el trabajo. Si el profesor pregunta “¿por qué existe este proyecto?”, la respuesta no debería ser “porque nos pareció”. Debería ser: “porque cubre estos controles, que tienen estas brechas, con estos hallazgos”.

## 17. Qué es SGSI

**SGSI** significa Sistema de Gestión de Seguridad de la Información.

Es una forma organizada de gestionar seguridad: definir alcance, políticas, responsables, controles, medición, revisión y mejora.

El tablero no implementa un SGSI completo, pero sí ayuda a operar una lógica de SGSI:

1. medir estado actual;
2. detectar brechas;
3. priorizar acciones;
4. ejecutar mejoras;
5. volver a medir.

## 18. Cómo contar todo junto en la defensa

Una forma simple de explicarlo:

“Tomamos el contexto de TecnoHogar y usamos ISO/IEC 27002:2022 como catálogo de controles. A cada control le asignamos una madurez CMMI. Con eso calculamos brechas y brechas ponderadas. Luego vinculamos esas brechas con proyectos de mejora. El tablero permite ver el resumen ejecutivo, bajar al detalle por control y justificar el plan con trazabilidad”.

## 19. Frases cortas para responder preguntas

- **ISO 27002 no certifica:** nos da un catálogo de controles.
- **CMMI no es la ISO:** es la escala que usamos para medir madurez.
- **Brecha no significa ausencia total:** significa distancia al objetivo.
- **Brecha ponderada prioriza mejor:** combina distancia y peso del control.
- **Quick win no es algo menor:** es alto impacto con esfuerzo relativo bajo.
- **El tablero no es sólo visual:** sirve para gobernar, priorizar y seguir mejoras.
- **La trazabilidad defiende el plan:** cada proyecto se conecta con controles y hallazgos.
"""


def render_demo(result: MetricResult) -> str:
    resumen = result.resumen
    effort = int(resumen["esfuerzo_total"])
    return f"""# Demo en vivo

## Objetivo

Mostrar que el tablero permite ir desde una lectura ejecutiva hasta controles y proyectos trazables. La demo tiene que ser corta, guiada y conectada con la narrativa de la PPTX.

## Recorrido recomendado

1. Abrir `https://tp2seg.streamlit.app/` y verificar que el caso seleccionado sea `tecnohogar`.
2. Tab **Ejecutivo**: mostrar madurez global **{resumen['madurez_global_pct']}%**, brecha **{resumen['brecha_global_pct']}%**, **{resumen['controles_evaluados']} controles**, **{resumen['quick_wins']} quick wins** y radar de capacidades.
3. Tab **Mapa ISO**: mostrar que están los capítulos 5, 6, 7 y 8 y que los cuadrados representan controles evaluados.
4. Tab **Brechas**: mostrar el Pareto y explicar que la priorización usa brecha ponderada.
5. Tab **Plan**: mostrar las **{resumen['proyectos']} iniciativas**, la matriz impacto/esfuerzo y el roadmap de **{effort} jornadas**.
6. Tab **Trazabilidad**: cerrar con el Sankey y la tabla control-proyecto para demostrar que cada decisión se puede defender.

## Qué no conviene hacer

- No navegar sin rumbo por todas las tablas.
- No intentar explicar cada control uno por uno.
- No presentar el porcentaje global como única verdad.
- No decir que "todo está mal"; la lectura correcta es base operativa con brecha de formalización, medición y seguimiento.

## Plan B si Streamlit falla

1. Usar la PPTX generada.
2. Abrir `docs/notas/guia-graficos.md`.
3. Mostrar los screenshots de `docs/notas/assets/graficos/`.
4. Explicar que esos PNG fueron generados desde las mismas funciones Plotly que usa el tablero, con datos de TecnoHogar.

## Cierre sugerido

El tablero transforma el diagnóstico en gobierno: permite medir, priorizar, justificar proyectos y seguir la mejora de seguridad en el tiempo.
"""


def main() -> int:
    dataset = load_dataset(CASE_ID, ROOT)
    result = compute_metrics(dataset)
    guides = chart_guides()

    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    export_graphics(result, guides)
    write_file(NOTES_DIR / "README.md", render_readme(result, guides))
    write_file(NOTES_DIR / "glosario-abreviaturas.md", render_glossary())
    write_file(NOTES_DIR / "narrativa-presentacion.md", narrativa_markdown(result))
    write_file(NOTES_DIR / "guia-graficos.md", render_graph_guide(result, guides))
    write_file(NOTES_DIR / "conceptos-clave.md", render_concepts(result))
    write_file(NOTES_DIR / "iso-27002-guia.md", render_iso_guide(result))
    write_file(NOTES_DIR / "demo-en-vivo.md", render_demo(result))

    print(f"Generadas notas de defensa en {NOTES_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
