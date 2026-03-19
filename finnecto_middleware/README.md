# Finnecto Middleware (Entrega)

Middleware de integración para reenviar facturas a 2 sistemas destino (mock): `legacy` y `taxeable`.

## Requisitos

- Python \(>= 3.14\)
- [Poetry]
- (Opcional) Docker + Docker Compose para levantar el mock

## Variables de entorno

Este servicio soporta `.env` (ver `.env.example`).

- **`MOCK_SERVER_URL`**: base URL del mock. Default: `http://localhost:3000`
- **`JWT_DECODE_SECRET`**: secret para validar/decodificar el JWT entrante. Default: `incoming-jwt-dev-secret`

## Cómo ejecutar

### Levantar el mock server

Con Docker:

```bash
cd ../mock-server
docker-compose up --build
```

Verificar:

```bash
curl http://localhost:3000/health
```

### Levantar el middleware

```bash
poetry install
poetry run uvicorn main:app --reload
```

Verificar:

```bash
curl http://localhost:8000/health
```

## Happy path (flujo completo)

### 1) Preparar JWT de entrada

El request entrante exige `Authorization: Bearer <token>`.

- **Legacy**: JWT con claims `connection_type=legacy`, `username`, `password`.
- **Taxeable**: además incluye `secret` (usado para generar el JWT de salida al mock).

En el `README.md` del challenge hay tokens de ejemplo ya firmados con `incoming-jwt-dev-secret`.

### 2) Enviar factura estándar al middleware

Body estándar (ejemplo):

```json
{
  "number": "FNCT0006",
  "reception_date": "2026-03-03",
  "due_date": "2026-03-20",
  "currency": "COP",
  "total": 780000,
  "items": [
    {
      "description": "Item 1",
      "unit_price": 30000,
      "total": 390000,
      "account": "VISTA"
    }
  ]
}
```

#### Caso legacy

```bash
curl -sS -X POST http://localhost:8000/invoice/forward \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <JWT_LEGACY>" \
  -d '{"number":"FNCT0006","reception_date":"2026-03-03","due_date":"2026-03-20","currency":"COP","total":780000,"items":[{"description":"Item 1","unit_price":30000,"total":390000,"account":"VISTA"}]}'
```

El middleware:

- Decodifica el JWT entrante
- Aplica IVA 19% a cada línea (solo sobre `total` de ítem) y recalcula total de cabecera
- Transforma el body a formato legacy
- Autentica contra el mock usando **Basic Auth** con `username/password` del JWT
- Envía a `POST ${MOCK_SERVER_URL}/legacy`
- Toma la respuesta y la transforma al formato estándar

#### Caso taxeable

```bash
curl -sS -X POST http://localhost:8000/invoice/forward \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <JWT_TAXEABLE>" \
  -d '{"number":"FNCT0006","reception_date":"2026-03-03","due_date":"2026-03-20","currency":"COP","total":780000,"items":[{"description":"Item 1","unit_price":30000,"total":390000,"account":"VISTA"}]}'
```

El middleware:

- Decodifica el JWT entrante y extrae `secret`
- Transforma el body a formato taxeable
- Genera un JWT de salida con:
  - `iss="middleware-mock"`
  - `aud="taxeable-api"`
  - `exp` a 1 hora
- Envía a `POST ${MOCK_SERVER_URL}/taxeable` con `Authorization: Bearer <token-generado>`
- Toma la respuesta y la transforma al formato estándar

## Manejo de errores (mínimo)

- **400**: payload inválido (validación FastAPI/Pydantic)
- **401**: header Authorization faltante o JWT inválido/expirado
- **502**: error al invocar el mock (status no-2xx, connect error, timeout)

## Supuestos

- **IVA legacy**: se aplica como \(total\_línea \* 1.19\) y se **redondea** con `round(...)` por línea; luego el total de cabecera es la suma de líneas.
- **Total de entrada**: se acepta como parte del contrato de entrada, pero para legacy el total efectivo enviado se recalcula desde las líneas (después de IVA).
- **Timeout a destino**: 10s por request al mock.

## Tests

```bash
poetry run pytest -v
```