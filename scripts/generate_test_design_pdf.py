"""Genera el documento breve de decisiones de diseño de pruebas."""
from fpdf import FPDF


REPO = "https://github.com/GayatriM916/task-manager"
OUT = "docs/decisiones-diseno-pruebas.pdf"


class Doc(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, f"Pagina {self.page_no()}/{{nb}}", align="C")


def clean(text: str) -> str:
    """Normaliza caracteres no soportados por Helvetica core fonts."""
    replacements = {
        "\u2014": "-",
        "\u2013": "-",
        "\u201c": '"',
        "\u201d": '"',
        "\u2018": "'",
        "\u2019": "'",
        "\u2026": "...",
        "\u00a0": " ",
        "\u2192": "->",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text.encode("latin-1", "replace").decode("latin-1")


def heading(pdf: FPDF, text: str, size: int = 12):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", size)
    pdf.set_text_color(20, 40, 70)
    pdf.multi_cell(0, 6, clean(text))
    pdf.set_x(pdf.l_margin)
    pdf.ln(1)


def body(pdf: FPDF, text: str):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(30, 30, 30)
    pdf.multi_cell(0, 4.6, clean(text))
    pdf.set_x(pdf.l_margin)
    pdf.ln(1.5)


def bullet(pdf: FPDF, text: str):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(30, 30, 30)
    pdf.multi_cell(0, 4.6, clean(f"  - {text}"))
    pdf.set_x(pdf.l_margin)


def main():
    pdf = Doc(format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.set_margins(16, 14, 16)
    pdf.add_page()

    # Titulo
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(15, 35, 65)
    pdf.multi_cell(0, 7, clean("Decisiones de diseno de las pruebas"))
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(
        0,
        4.5,
        clean(
            "Task Manager Testing Lab  |  Suite Jest  |  Documento breve (max. 2 paginas)"
        ),
    )
    pdf.set_x(pdf.l_margin)
    pdf.ln(2)

    heading(pdf, "1. Acceso al repositorio")
    body(
        pdf,
        "Codigo fuente y pruebas: "
        + REPO
        + "  |  Carpeta de pruebas: __tests__/  |  Cobertura: npx jest --coverage",
    )

    heading(pdf, "2. Que se probo en esta iteracion")
    body(
        pdf,
        "Se reforzaron las pruebas unitarias de utilidades y se completo el aislamiento "
        "del hook que interactua con la capa de servicio. No se modifico la logica "
        "funcional de la aplicacion ni se eliminaron pruebas existentes.",
    )
    bullet(
        pdf,
        "Utils - filterTasksByStatus (src/utils/filterTasks.ts): filtrado por estado, "
        "lista vacia, estados invalidos/nulos y uso de matchers toEqual, toContain y toThrow.",
    )
    bullet(
        pdf,
        "Utils - validateTaskTitle (src/utils/validateTask.ts): limites null/undefined "
        "y comprobacion parcial del mensaje de error con toContain.",
    )
    bullet(
        pdf,
        "Hooks - useCreateTask (src/hooks/useCreateTask.ts): estado inicial idle, "
        "submit exitoso (success + lista), fallo del servicio (loading -> error) y removeTask.",
    )
    pdf.ln(1)

    heading(pdf, "3. Por que se eligieron esos casos")
    bullet(
        pdf,
        "Casos principales: validan el comportamiento esperado del dominio "
        "(filtrar pending/completed, titulo valido, crear tarea con exito).",
    )
    bullet(
        pdf,
        "Casos limite: listas vacias, estados inesperados ('' / null), titulos null/undefined "
        "y errores de servicio. Exponen reglas de validacion y manejo de fallos.",
    )
    bullet(
        pdf,
        "Hooks con renderHook + act: permiten verificar actualizaciones de estado "
        "y efectos secundarios (llamada a createTask) sin montar pantallas completas.",
    )
    bullet(
        pdf,
        "Criterio de suficiencia: al menos 6 pruebas en utils (sumando las nuevas) "
        "y al menos 4 pruebas nuevas para el hook sin cobertura previa.",
    )
    pdf.ln(1)

    heading(pdf, "4. Dependencias aisladas con mocking")
    body(
        pdf,
        "Solo se mockeo donde habia dependencia externa. Las utilidades son funciones "
        "puras: no requieren jest.mock ni jest.fn.",
    )
    bullet(
        pdf,
        "jest.mock('../../src/services/taskService') en __tests__/hooks/useCreateTask.test.ts: "
        "aisla createTask (capa de servicio). Motivo: controlar exito/fallo sin depender "
        "de la implementacion real (red o Date.now), observar loading/error/success y "
        "verificar que submit invoca el servicio con el titulo esperado.",
    )
    bullet(
        pdf,
        "mockResolvedValue / mockImplementation + jest.clearAllMocks: configuran respuestas "
        "por caso y evitan fugas de estado entre pruebas. No se anadieron mocks innecesarios "
        "en filterTasks ni validateTask.",
    )
    pdf.ln(1)

    heading(pdf, "5. Resultado de la suite")
    body(
        pdf,
        "Ejecucion verificada con npx jest --coverage: 13 suites / 53 pruebas en verde. "
        "Cobertura global aproximada: 90.9% statements. Hooks y utils al 100% en statements "
        "de los archivos cubiertos por estas pruebas.",
    )

    pdf.output(OUT)
    print(f"PDF generado: {OUT}")


if __name__ == "__main__":
    main()
