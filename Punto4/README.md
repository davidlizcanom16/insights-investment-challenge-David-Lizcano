# Sofia — ACH Funding Agent
### Insights Wealth Management · Punto 4

Sofia es un agente conversacional diseñado para guiar a clientes de
Insights Wealth Management a través del proceso completo de fondeo de
su cuenta de inversión vía transferencia ACH. El agente detecta el
idioma del cliente automáticamente y responde en español o inglés.

---

## Demo en vivo

No se requiere instalación. El agente está desplegado y disponible:

👉 **[Abrir Sofia en Streamlit Cloud](https://insights-investment-challenge-david-lizcano-123456789.streamlit.app/)**

El sidebar permite simular los tres escenarios del punto 4.5:

| Escenario | Configuración |
|-----------|---------------|
| Flujo exitoso | ✅ Success |
| Fondos insuficientes | ⚠️ R01 |
| Cuenta no encontrada | ❌ R03 |

---

## Stack tecnológico

| Componente | Herramienta |
|------------|-------------|
| LLM | Gemini 2.5 Flash (Google AI) |
| UI | Streamlit |
| Routing lookup | Tabla ABA estática + validación checksum |
| Memoria entre sesiones | JSON local (`memory.json`) |
| Deployment | Streamlit Community Cloud |

---

## Estructura de archivos
```
punto4/
├── app.py              # Interfaz Streamlit + lógica de UI
├── agent.py            # Integración Gemini API + system prompt
├── routing_table.py    # Tabla ABA routing numbers + validación checksum
├── memory.py           # Lectura y escritura de memoria entre sesiones
├── memory.json         # Persistencia local de datos del cliente
├── Logoprueba.png      # Logo de Insights WM
├── requirements.txt    # Dependencias Python
└── README.md           # Este archivo
```

---

## Correr localmente

**1. Clonar el repositorio:**
```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo/punto4
```

**2. Instalar dependencias:**
```bash
pip install -r requirements.txt
```

**3. Configurar API key:**

Crear archivo `.streamlit/secrets.toml` en la raíz del proyecto:
```toml
GEMINI_API_KEY = "tu-api-key-aqui"
```

La API key de Gemini se obtiene en: https://aistudio.google.com/app/apikey

**4. Correr el agente:**
```bash
streamlit run app.py
```

Se abre automáticamente en `http://localhost:8501`

---

## Flujo del agente
```
Cliente inicia conversación
        ↓
Sofia detecta idioma → español o inglés
        ↓
¿Hay memoria previa del cliente?
   SÍ → saluda con banco y estado guardados
   NO → recopila banco y estado desde cero
        ↓
Recopila número de cuenta, tipo y monto
        ↓
Lookup routing number → banco + estado
Valida checksum internamente
Confirma con el cliente
        ↓
Guía paso a paso la configuración ACH
        ↓
Resumen + confirmación explícita
        ↓
   ✅ Éxito → fondeo iniciado
   ⚠️ R01  → fondos insuficientes
   ❌ R03  → cuenta no encontrada
   ❓ Otro → escala a asesor humano
```

---

## Memoria entre sesiones

El agente guarda banco, estado y tipo de cuenta por cliente en
`memory.json`. En la siguiente sesión, Sofia reconoce al cliente
y omite las preguntas ya respondidas.

**Limitación conocida:** en Streamlit Community Cloud el filesystem
es efímero — la memoria no persiste entre reinicios del servidor.
En producción se reemplazaría `memory.json` por Supabase o Firebase
Firestore sin cambios en la lógica del agente.

---

## Investigación de trasfondo

La investigación completa que fundamenta el diseño del agente
está documentada en [`solutions.md`](../solutions.md):

- **4.1.1** Flujo ACH completo: Originator → ODFI → ACH Network → RDFI → Receiver
- **4.1.2** Requisitos de fondeo + códigos Nacha de rechazo
- **4.1.3** Routing numbers ABA: estructura, lógica y tabla de referencia
- **4.1.4** Comparativa ACH vs Wire vs Tarjeta de Débito
