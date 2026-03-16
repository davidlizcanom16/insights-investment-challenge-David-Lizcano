## 4.1 Investigación previa

### 4.1.1 ¿Cómo funciona ACH en EE.UU.?

Cuando un cliente de Insights deposita dinero desde su cuenta bancaria mediante ACH, el proceso no ocurre de forma instantánea. Se trata de un sistema de pagos **por lotes** que involucra varias instituciones financieras y que normalmente tarda entre **1 y 3 días hábiles** en completarse.

El flujo completo del sistema ACH es el siguiente:

**1. Originator (Insights)**  
Insights inicia la instrucción de débito desde la cuenta bancaria del cliente. En otras palabras, solicita retirar una cantidad específica de dinero desde la cuenta del usuario.

**2. ODFI (Originating Depository Financial Institution)**  
La solicitud pasa primero por el banco de Insights. Este banco recopila múltiples instrucciones del día y las envía agrupadas en un archivo batch hacia la red ACH.

**3. ACH Network**  
La red ACH (operada por la Reserva Federal o por The Clearing House) actúa como intermediario. Su función es enrutar cada transacción hacia el banco correspondiente del cliente.

**4. RDFI (Receiving Depository Financial Institution)**  
El banco del cliente recibe la instrucción, verifica que la cuenta exista y que tenga fondos suficientes, y ejecuta el débito.

**5. Receiver (cliente)**  
El dinero se debita de la cuenta del cliente y finalmente se acredita en la cuenta de Insights.

#### Tiempos de liquidación

Existen dos modalidades principales:

**ACH estándar**
- Tiempo típico: **1–3 días hábiles**
- Es el método más común para transferencias regulares.

**Same-Day ACH**
- Liquidación el mismo día
- Debe enviarse antes de las ventanas de corte aproximadas:
  - 10:30 AM ET  
  - 1:00 PM ET  
  - 4:45 PM ET

Un punto importante es que, incluso cuando una transacción aparece como "exitosa", el banco del cliente todavía puede **rechazarla o devolverla posteriormente**. Por esta razón, muchas plataformas financieras mantienen un período de retención de **3 a 5 días hábiles** antes de permitir que esos fondos se utilicen para invertir.

#### Cuándo recomendar Same-Day ACH

El Same-Day ACH tiene sentido en situaciones como:

- Cuando el cliente quiere **invertir el mismo día** por una oportunidad de mercado.
- Cuando se necesita **corregir rápidamente un fondeo fallido**.
- Cuando se trata del **primer depósito de un cliente nuevo** y se quiere mejorar la experiencia inicial.

Para depósitos recurrentes o programados, el **ACH estándar suele ser suficiente y más económico**.

---

### 4.1.2 Requisitos para fondear una cuenta vía ACH

Para configurar un débito ACH desde la cuenta bancaria de un cliente, normalmente se requiere la siguiente información:

- Nombre del titular de la cuenta
- Routing number (ABA) del banco
- Número de cuenta bancaria
- Tipo de cuenta (corriente o ahorros)

Además, el cliente debe aceptar una **autorización ACH**, que es el consentimiento legal que permite a la plataforma iniciar débitos desde su cuenta.

#### Verificación de la cuenta bancaria

Antes de procesar el primer débito, la cuenta generalmente debe ser verificada. Existen dos métodos principales.

**Micro-depósitos**

Se envían dos pequeños montos (normalmente menores a $1) a la cuenta bancaria del cliente. El cliente debe confirmar esos montos uno o dos días después.

Ventajas:
- Funciona con prácticamente cualquier banco.

Desventajas:
- Introduce fricción y demora en el proceso de activación.

**Verificación instantánea**

Servicios como **Plaid o MX** permiten que el cliente se autentique en su banca en línea y verifique la cuenta en segundos.

Ventajas:
- Activación inmediata.
- Mejor experiencia de usuario.

#### Límites y disponibilidad de fondos

Las cuentas nuevas suelen tener límites iniciales de fondeo diario entre **$5,000 y $25,000**, que pueden aumentar conforme el cliente construye historial en la plataforma.

Después de procesarse el depósito, los fondos suelen permanecer en espera durante **3 a 5 días hábiles** antes de poder utilizarse para invertir.

#### Códigos comunes de rechazo (Nacha)

**R01 — Fondos insuficientes**

La cuenta no tenía saldo suficiente en el momento del débito.

Mensaje al cliente:  
> No pudimos completar el depósito porque la cuenta no tenía fondos suficientes. Te recomendamos verificar tu saldo e intentar nuevamente.

**R02 — Cuenta cerrada**

La cuenta bancaria ya no está activa.

Mensaje al cliente:  
> Parece que la cuenta bancaria vinculada está cerrada. Por favor conecta una cuenta diferente para continuar.

**R03 — No existe cuenta**

El routing number o el número de cuenta no coinciden con registros válidos del banco.

Mensaje al cliente:  
> No pudimos verificar los datos bancarios. Te recomendamos revisar el routing number y el número de cuenta en tu app bancaria o en un cheque.

---

### 4.1.3 Routing numbers (ABA): lógica y lookup por banco y estado

El **ABA routing number** es un código de **9 dígitos** que identifica a una institución financiera dentro del sistema de pagos de Estados Unidos.

Es el número que aparece en la parte inferior izquierda de los cheques y es esencial para procesar transferencias ACH.

#### Estructura del routing number

El número está compuesto por tres partes:

- Los primeros dígitos indican el **distrito de la Reserva Federal**.
- Los siguientes identifican a la **institución financiera**.
- El último es un **dígito de control** que permite validar matemáticamente el número.

#### Por qué un banco puede tener distintos routing numbers

Muchos bancos en Estados Unidos tienen routing numbers diferentes dependiendo del **estado donde se abrió la cuenta**.

Esto ocurre debido a décadas de **fusiones y adquisiciones bancarias**. Cuando un banco grande absorbe otro, muchas veces conserva los routing numbers regionales.

Por ejemplo, **Bank of America puede tener un routing number distinto en Texas que en California**.

Incluso si un cliente se muda a otro estado, normalmente seguirá utilizando el routing asociado al estado donde abrió su cuenta originalmente.

#### Implicación para el agente

Para encontrar el routing correcto, el agente debe preguntar:

- el banco del cliente
- el estado donde abrió su cuenta

Con esta información se puede realizar el lookup correcto y pedir al cliente que confirme que el número coincide con el que aparece en su app bancaria o en su chequera.

Si el cliente proporciona un routing diferente, el sistema puede validar su estructura antes de utilizarlo.

---

### 4.1.4 Comparativa: ACH vs Wire vs tarjeta de débito

Cuando un cliente quiere fondear su cuenta de inversión, existen tres métodos principales:

**ACH**

- Tiempo: 1–3 días hábiles
- Costo: muy bajo
- Ideal para depósitos recurrentes

Es el método preferido por la mayoría de plataformas porque permite automatizar depósitos y mantener costos operativos bajos.

**Wire transfer**

- Tiempo: mismo día o menos de 24 horas
- Costo: alto

Se utiliza principalmente cuando el cliente necesita que los fondos estén disponibles de inmediato o cuando el monto transferido es muy alto.

**Tarjeta de débito**

- Tiempo: casi instantáneo
- Costo: más alto que ACH

Se utiliza frecuentemente para **primeros depósitos pequeños**, ya que permite que el cliente vea el dinero reflejado inmediatamente, lo que mejora la experiencia inicial.

En la práctica, el **ACH suele ser la opción principal** para depósitos recurrentes debido a su bajo costo y facilidad de uso.

## 4.2 Diseño del agente — Arquitectura y flujo conversacional

**Propósito:** guiar a clientes de Insights a través del proceso
completo de fondeo vía ACH, desde la recopilación de datos bancarios
hasta la confirmación de la instrucción, manejando errores y
escalamientos de forma autónoma.

### Estados del agente

| # | Estado | Responsabilidad | Transición |
|---|--------|-----------------|------------|
| 1 | GREETING | Identificar intención del cliente | Si menciona fondeo → COLLECT_BANK_STATE |
| 2 | COLLECT_BANK_STATE | Preguntar banco y estado antes que cualquier otra cosa | Datos recibidos → COLLECT_ACCOUNT_INFO |
| 3 | COLLECT_ACCOUNT_INFO | Recopilar número de cuenta, tipo y monto | Datos completos → ROUTING_LOOKUP |
| 4 | ROUTING_LOOKUP | Inferir routing, aplicar checksum, confirmar | Cliente confirma → INSTRUCTIONS |
| 5 | INSTRUCTIONS | Guiar paso a paso la autorización ACH | Cliente autoriza → CONFIRMATION |
| 6 | CONFIRMATION | Resumen completo antes de ejecutar | Cliente confirma → éxito / error |
| 7 | ERROR_HANDLING | Comunicar fallo con código Nacha y siguiente paso | Reintento o escalar → humano |

### Diagrama de flujo
```
Cliente inicia conversación
        ↓
[GREETING] — ¿En qué puedo ayudarte?
        ↓
¿Intención = fondeo ACH?
   NO → redirigir o escalar
   SÍ ↓
[COLLECT_BANK_STATE]
"¿Con qué banco y en qué estado tienes tu cuenta?"
        ↓
¿Hay memoria previa del cliente?
   SÍ → "Veo que usas {banco} en {estado}, ¿seguimos?"
   NO → recopilar desde cero
        ↓
[COLLECT_ACCOUNT_INFO]
— Número de cuenta
— Tipo: cheques o ahorros
— Monto a fondear
        ↓
[ROUTING_LOOKUP]
— Lookup banco + estado → routing number
— Validar checksum internamente
— Confirmar con cliente
        ↓
[INSTRUCTIONS] → paso a paso
        ↓
[CONFIRMATION] → resumen + confirmación explícita
        ↓
   ✅ Éxito → fondeo iniciado → guardar memoria
   ⚠️ R01  → fondos insuficientes → reintentar
   ❌ R03  → cuenta no encontrada → revisar datos
   ❓ Otro → escalar a asesor humano con historial
```

### Reglas de diseño

1. **Banco + estado siempre primero.** Sin excepción.
2. **Memoria entre sesiones.** Si el cliente ya fondeo, el agente
   recupera banco y estado y pregunta si desea usar la misma cuenta.
3. **Confirmación explícita antes de ejecutar.** El agente muestra
   un resumen completo y pide confirmación antes de procesar.
4. **Escalamiento con contexto.** Si el agente no puede resolver el
   fallo, escala a un asesor humano enviando el historial completo.
5. **Tono consistente.** Profesional y cercano. Los códigos Nacha
   son internos — el cliente recibe mensajes en lenguaje natural.

---

## 4.3 System prompt — El cerebro del agente

El system prompt completo está implementado en `agent.py` dentro de
la función `build_system_prompt()`. A continuación se documenta cada
sección y la razón de su inclusión.

### Secciones y justificación

| Sección | Contenido | Por qué está ahí |
|---------|-----------|-----------------|
| **Rol y nombre** | Sofia, asistente ACH de Insights WM | Define identidad consistente. Sin esto el LLM improvisa nombre y rol entre turnos |
| **Regla de idioma** | Detecta español/inglés y responde en el mismo | Los clientes de Insights son latinos en EE.UU. — la barrera de idioma no puede ser un obstáculo |
| **Tono** | Profesional, cercano, sin jerga técnica | Un cliente que recibe "ODFI" o "Nacha" en una respuesta pierde confianza |
| **Regla banco+estado primero** | Obligatoria antes de cualquier información | Previene dar routing incorrecto. Es también la regla más importante del enunciado |
| **Flujo ordenado** | 7 pasos secuenciales explícitos | Un LLM sin flujo explícito salta pasos. El orden es la columna vertebral del agente |
| **Routing table interna** | Tabla banco+estado → routing, nunca expuesta al cliente | El agente resuelve sin preguntar al cliente. Experiencia fluida |
| **Checksum interno** | Fórmula de validación ABA aplicada en silencio | Capa de protección que el cliente nunca ve pero que previene errores de tipeo |
| **Error handling por código** | Mensajes humanos para R01, R02, R03 y error desconocido | El cliente nunca ve códigos técnicos. Empatía primero, solución después |
| **Disclaimer** | Una vez por sesión antes de la confirmación final | Protección legal mínima. Estándar en cualquier producto fintech |
| **Memoria** | Instrucciones para usar y guardar datos del cliente | Reduce fricción en sesiones futuras |

### Extracto del system prompt
```
You are Sofia, a specialized ACH funding assistant for
Insights Wealth Management. Your sole purpose is to guide
clients through funding their investment account via ACH
bank transfer.

LANGUAGE RULE — CRITICAL:
Detect the language of the client's first message and respond
in that language throughout the session. Never mix languages.

MANDATORY RULE — BANK AND STATE ALWAYS FIRST:
Before providing any routing number or instructions, collect:
  1. Client's bank name
  2. US state where the account was opened
Never skip this step under any circumstance.
```

El system prompt completo está disponible en `agent.py`.

---

## 4.4 Implementación

Ver código completo en:
- `app.py` — Interfaz Streamlit
- `agent.py` — Integración Gemini API + system prompt
- `routing_table.py` — Tabla ABA + validación checksum
- `memory.py` — Persistencia entre sesiones

### Decisiones de implementación

**¿Por qué Gemini 2.5 Flash?**
El enunciado otorga puntos bonus por usar la API de Gemini.
Gemini 2.5 Flash ofrece el mejor balance entre velocidad, costo
y capacidad para tareas conversacionales estructuradas. Su tier
gratuito es suficiente para un prototipo de demostración.

**¿Por qué Streamlit y no CLI?**
El enunciado dice "interfaz libre". Una app web desplegada es
superior a un script de consola porque el evaluador puede
interactuar sin instalar nada, los tres escenarios se prueban
en segundos con el selector del sidebar, y el diseño visual
refuerza la identidad de marca de Insights.

**¿Por qué routing table estática?**
Para un prototipo, una tabla estática es suficiente y evita
dependencias externas que pueden fallar en demo. En producción
se reemplazaría por una consulta en tiempo real a la Federal
Reserve o a Plaid.

---

## 4.5 Demo y Reflexión

Ver archivo principal: [`punto4/README.md`](README.md)
