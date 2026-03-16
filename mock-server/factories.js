/**
 * Factory para generar respuestas con datos aleatorios
 * en formato legacy y taxeable
 */

const randomId = () => `ID-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
const randomInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
const randomDate = (daysOffset = 30) => {
  const d = new Date();
  d.setDate(d.getDate() + randomInt(-daysOffset, daysOffset));
  return d.toISOString().split('T')[0];
};

const CURRENCIES = ['COP', 'CLP', 'USD'];
const ACCOUNTS = ['VISTA', 'CORRIENTE', 'AHORRO', 'INVERSION'];

/**
 * Genera respuesta en formato legacy
 */
function buildLegacyResponse(incomingBody = {}) {
  const itemCount = incomingBody.lines?.length || incomingBody.items?.length || randomInt(1, 4);
  const lines = [];

  for (let i = 0; i < itemCount; i++) {
    const unitPrice = randomInt(10000, 100000);
    const qty = randomInt(1, 5);
    const lineTotal = unitPrice * qty;
    lines.push({
      id: randomId(),
      desc: incomingBody.lines?.[i]?.desc || `Item ${i + 1} - Descripción generada`,
      unit_price: unitPrice,
      line_total: lineTotal,
      acct: ACCOUNTS[randomInt(0, ACCOUNTS.length - 1)],
    });
  }

  const grossTotal = lines.reduce((sum, l) => sum + l.line_total, 0);

  return {
    invoice_number: incomingBody.invoice_number || `INV-${randomInt(1000, 9999)}`,
    recv_date: incomingBody.recv_date || randomDate(),
    expiry_date: incomingBody.expiry_date || randomDate(60),
    curr: incomingBody.curr || CURRENCIES[randomInt(0, 2)],
    gross_total: grossTotal,
    lines,
    processed_at: new Date().toISOString(),
  };
}

/**
 * Genera respuesta en formato taxeable
 */
function buildTaxeableResponse(incomingBody = {}) {
  const doc = incomingBody.document || incomingBody;
  const items = doc.items || [];
  const itemCount = items.length || randomInt(1, 4);
  const responseItems = [];

  for (let i = 0; i < itemCount; i++) {
    const unitPrice = randomInt(10000, 100000);
    const amount = unitPrice * randomInt(1, 5);
    responseItems.push({
      id: randomId(),
      description: items[i]?.description || `Item ${i + 1} - Descripción generada`,
      unitPrice,
      amount,
      account: items[i]?.account || ACCOUNTS[randomInt(0, ACCOUNTS.length - 1)],
    });
  }

  const total = responseItems.reduce((sum, i) => sum + i.amount, 0);

  return {
    document: {
      reference: doc.reference || `REF-${randomInt(1000, 9999)}`,
      dates: {
        reception: doc.dates?.reception || randomDate(),
        due: doc.dates?.due || randomDate(60),
      },
      currency: doc.currency || CURRENCIES[randomInt(0, 2)],
      total,
      items: responseItems,
      processedAt: new Date().toISOString(),
    },
  };
}

module.exports = {
  buildLegacyResponse,
  buildTaxeableResponse,
};
