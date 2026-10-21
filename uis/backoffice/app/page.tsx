"use client";

import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";

type Product = {
  id: string;
  name: string;
  sku: string;
  category?: string;
  stock_minimo: number;
  unit: string;
};

type Location = {
  id: string;
  name: string;
  country: string;
  city: string;
};

type StockInfo = {
  product_id: string;
  location_id: string;
  current_stock: number;
  alert: boolean;
};

type Movement = {
  id: string;
  product_id: string;
  location_id: string;
  movement_type: "ENTRADA" | "SALIDA" | "MERMA";
  quantity: number;
  unit_price?: number | null;
  reference?: string | null;
  notes?: string | null;
  created_at: string;
};

type MovementType = Movement["movement_type"];

async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api/inventory${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });

  if (!response.ok) {
    let message = `Error ${response.status} al comunicarse con la API`;
    try {
      const body = (await response.json()) as { detail?: string };
      if (body.detail) message = body.detail;
    } catch {
      // Keep the HTTP status message when the API does not return JSON.
    }
    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

function messageFrom(error: unknown): string {
  return error instanceof Error ? error.message : "Error inesperado al comunicarse con la API.";
}

function formatDate(value: string): string {
  return new Intl.DateTimeFormat("es-CO", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function formatQuantity(value: number): string {
  return new Intl.NumberFormat("es-CO", { maximumFractionDigits: 2 }).format(value);
}

export default function InventoryPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [locations, setLocations] = useState<Location[]>([]);
  const [stocks, setStocks] = useState<StockInfo[]>([]);
  const [movements, setMovements] = useState<Movement[]>([]);
  const [selectedLocation, setSelectedLocation] = useState("");
  const [selectedProduct, setSelectedProduct] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("TODAS");
  const [loading, setLoading] = useState(true);
  const [refreshKey, setRefreshKey] = useState(0);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [formOpen, setFormOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [movementType, setMovementType] = useState<MovementType>("ENTRADA");
  const [quantity, setQuantity] = useState("");
  const [reference, setReference] = useState("");
  const [notes, setNotes] = useState("");

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");

    Promise.all([
      apiRequest<Product[]>(
        categoryFilter === "TODAS"
          ? "/products"
          : `/products?category=${encodeURIComponent(categoryFilter)}`,
      ),
      apiRequest<Location[]>("/locations"),
    ])
      .then(([productData, locationData]) => {
        if (!active) return;
        setProducts(productData);
        setLocations(locationData);
        setSelectedLocation((current) => current || locationData[0]?.id || "");
        setSelectedProduct((current) =>
          productData.some((product) => product.id === current)
            ? current
            : productData[0]?.id || "",
        );
      })
      .catch((loadError: unknown) => {
        if (active) setError(messageFrom(loadError));
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, [categoryFilter, refreshKey]);

  useEffect(() => {
    if (!selectedLocation || products.length === 0) {
      setStocks([]);
      return;
    }
    let active = true;

    Promise.all(
      products.map((product) =>
        apiRequest<StockInfo>(
          `/stock?product_id=${encodeURIComponent(product.id)}&location_id=${encodeURIComponent(selectedLocation)}`,
        ),
      ),
    )
      .then((stockData) => {
        if (active) setStocks(stockData);
      })
      .catch((loadError: unknown) => {
        if (active) setError(messageFrom(loadError));
      });

    return () => {
      active = false;
    };
  }, [products, selectedLocation, refreshKey]);

  useEffect(() => {
    if (!selectedLocation || !selectedProduct) {
      setMovements([]);
      return;
    }
    let active = true;

    apiRequest<Movement[]>(
      `/movements?product_id=${encodeURIComponent(selectedProduct)}&location_id=${encodeURIComponent(selectedLocation)}`,
    )
      .then((data) => {
        if (active) setMovements(data);
      })
      .catch((loadError: unknown) => {
        if (active) setError(messageFrom(loadError));
      });

    return () => {
      active = false;
    };
  }, [selectedLocation, selectedProduct, refreshKey]);

  const selectedLocationData = locations.find((location) => location.id === selectedLocation);
  const selectedProductData = products.find((product) => product.id === selectedProduct);
  const alertCount = useMemo(() => stocks.filter((stock) => stock.alert).length, [stocks]);

  const submitMovement = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    setNotice("");
    setSubmitting(true);

    try {
      await apiRequest<Movement>("/movements", {
        method: "POST",
        body: JSON.stringify({
          product_id: selectedProduct,
          location_id: selectedLocation,
          movement_type: movementType,
          quantity: Number(quantity),
          reference: reference.trim() || null,
          notes: notes.trim() || null,
        }),
      });
      setNotice("Movimiento registrado. El stock se actualizará a partir del historial.");
      setFormOpen(false);
      setQuantity("");
      setReference("");
      setNotes("");
      setRefreshKey((key) => key + 1);
    } catch (submitError: unknown) {
      setError(messageFrom(submitError));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <a className="sidebar-brand" href="#" aria-label="Brasaland">
          <span className="brand-symbol">B</span>
          <span>BRASALAND<small>OPERACIONES</small></span>
        </a>
        <div className="sidebar-label">MENÚ PRINCIPAL</div>
        <a className="side-link active" href="#inventario"><span className="side-icon">▦</span> Inventario</a>
        <a className="side-link" href="#movimientos"><span className="side-icon">↔</span> Movimientos</a>
        <div className="sidebar-bottom">
          <div className="user-avatar">BD</div>
          <div className="user-copy"><strong>Brasaland Digital</strong><span>Equipo de operaciones</span></div>
          <span className="user-menu">···</span>
        </div>
      </aside>

      <section className="main-area">
        <header className="topbar">
          <div className="breadcrumb">Operaciones <span>/</span> Inventario</div>
          <div className="topbar-right">
            <span className="secure-badge"><span /> Sistema interno</span>
            <span className="topbar-divider" />
            <span className="topbar-date">{new Intl.DateTimeFormat("es-CO", { dateStyle: "full", timeZone: "America/Bogota" }).format(new Date())}</span>
          </div>
        </header>

        <div className="content">
          <div className="page-heading">
            <div>
              <p className="eyebrow">BRASALAND · CONTROL OPERATIVO</p>
              <h1>Inventario</h1>
              <p className="page-subtitle">Existencias calculadas desde los movimientos registrados.</p>
            </div>
            <button className="primary-button" onClick={() => { setError(""); setNotice(""); setFormOpen(true); }} disabled={!products.length || !selectedLocation}>
              <span>＋</span> Registrar movimiento
            </button>
          </div>

          {error && <div className="feedback error-feedback" role="alert"><strong>No se pudo completar la operación</strong><span>{error}</span></div>}
          {notice && <div className="feedback success-feedback" role="status">{notice}</div>}

          <div className="location-toolbar">
            <label htmlFor="location-select">LOCAL ACTIVO</label>
            <select
              id="location-select"
              value={selectedLocation}
              onChange={(event) => setSelectedLocation(event.target.value)}
              disabled={loading || locations.length === 0}
            >
              {locations.length === 0 && <option value="">Sin locales disponibles</option>}
              {locations.map((location) => (
                <option key={location.id} value={location.id}>{location.name} · {location.city}</option>
              ))}
            </select>
            {selectedLocationData && <span className="location-country">{selectedLocationData.country}</span>}
          </div>

          <section className="stats-grid" aria-label="Resumen de inventario">
            <article className="stat-card">
              <div className="stat-top"><span>Productos registrados</span><span className="stat-icon icon-orange">▤</span></div>
              <strong>{loading ? "—" : products.length.toString().padStart(2, "0")}</strong>
              <small>En este catálogo</small>
            </article>
            <article className="stat-card">
              <div className="stat-top"><span>Alertas de mínimo</span><span className="stat-icon icon-red">!</span></div>
              <strong>{loading ? "—" : alertCount.toString().padStart(2, "0")}</strong>
              <small>{alertCount ? "Requieren atención" : "Todo dentro del mínimo"}</small>
            </article>
            <article className="stat-card">
              <div className="stat-top"><span>Locales disponibles</span><span className="stat-icon icon-green">⌖</span></div>
              <strong>{loading ? "—" : locations.length.toString().padStart(2, "0")}</strong>
              <small>Colombia · Estados Unidos</small>
            </article>
          </section>

          <section className="panel inventory-panel" id="inventario">
            <div className="panel-heading">
              <div><h2>Existencias por producto</h2><p>Stock actual calculado para el local seleccionado.</p></div>
              <div className="inventory-tools">
                <label className="category-filter-label" htmlFor="category-filter">CATEGORÍA</label>
                <select
                  className="category-filter"
                  id="category-filter"
                  value={categoryFilter}
                  onChange={(event) => setCategoryFilter(event.target.value)}
                >
                  <option value="TODAS">Todas</option>
                  <option value="CARNE">Carne</option>
                  <option value="BEBIDA">Bebida</option>
                  <option value="LACTEO">Lácteo</option>
                  <option value="VEGETAL">Vegetal</option>
                  <option value="OTRO">Otro</option>
                </select>
                <span className="live-chip"><span /> ACTUALIZADO EN VIVO</span>
              </div>
            </div>
            <div className="table-scroll">
              <table>
                <thead><tr><th>PRODUCTO</th><th>CATEGORÍA</th><th>STOCK ACTUAL</th><th>MÍNIMO</th><th>ESTADO</th></tr></thead>
                <tbody>
                  {loading && <tr><td className="empty-cell" colSpan={5}>Conectando con el servicio de inventario…</td></tr>}
                  {!loading && products.length === 0 && !error && <tr><td className="empty-cell" colSpan={5}>No hay productos registrados.</td></tr>}
                  {!loading && products.map((product) => {
                    const stock = stocks.find((item) => item.product_id === product.id);
                    return (
                      <tr key={product.id} className={selectedProduct === product.id ? "selected-row" : ""} onClick={() => setSelectedProduct(product.id)}>
                        <td><button className="product-cell" onClick={() => setSelectedProduct(product.id)}><span className="product-avatar">{product.name.slice(0, 1).toUpperCase()}</span><span><strong>{product.name}</strong><small>{product.sku}</small></span></button></td>
                        <td><span className="category-label">{product.category ?? "Sin categoría"}</span></td>
                        <td className="stock-value">{stock ? formatQuantity(stock.current_stock) : "—"} <span>{product.unit}</span></td>
                        <td>{formatQuantity(product.stock_minimo)} <span className="unit-muted">{product.unit}</span></td>
                        <td>{stock?.alert ? <span className="status status-alert"><span /> Bajo mínimo</span> : stock ? <span className="status status-ok"><span /> Saludable</span> : <span className="status status-loading">Consultando</span>}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
            <div className="panel-footnote"><span className="info-dot">i</span> El stock no se edita directamente. Se calcula como entradas menos salidas y mermas.</div>
          </section>

          <section className="panel movements-panel" id="movimientos">
            <div className="panel-heading">
              <div><h2>Últimos movimientos</h2><p>{selectedProductData ? `${selectedProductData.name} · ${selectedLocationData?.name ?? "Local"}` : "Selecciona un producto para ver su historial."}</p></div>
              {selectedProductData && <span className="history-count">{movements.length} registros</span>}
            </div>
            {!selectedProductData ? (
              <div className="empty-history">Selecciona un producto en la tabla para consultar sus movimientos.</div>
            ) : movements.length === 0 ? (
              <div className="empty-history">No hay movimientos para este producto en el local seleccionado.</div>
            ) : (
              <div className="movement-list">
                {movements.slice(0, 5).map((movement) => (
                  <article className="movement-row" key={movement.id}>
                    <span className={`movement-icon movement-${movement.movement_type.toLowerCase()}`}>{movement.movement_type === "ENTRADA" ? "↓" : movement.movement_type === "SALIDA" ? "↑" : "!"}</span>
                    <div className="movement-main"><strong>{movement.movement_type}</strong><span>{movement.reference || movement.notes || "Sin referencia"}</span></div>
                    <time>{formatDate(movement.created_at)}</time>
                    <strong className={`movement-quantity movement-quantity-${movement.movement_type.toLowerCase()}`}>{movement.movement_type === "ENTRADA" ? "+" : "−"}{formatQuantity(movement.quantity)} {selectedProductData.unit}</strong>
                  </article>
                ))}
              </div>
            )}
          </section>
          <footer className="page-footer"><span>BRASALAND DIGITAL</span><span>Inventario · Control de movimientos</span></footer>
        </div>
      </section>

      {formOpen && (
        <div className="modal-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) setFormOpen(false); }}>
          <section className="movement-modal" role="dialog" aria-modal="true" aria-labelledby="movement-title">
            <div className="modal-heading"><div><p className="eyebrow">INVENTARIO · NUEVO REGISTRO</p><h2 id="movement-title">Registrar movimiento</h2></div><button className="close-button" onClick={() => setFormOpen(false)} aria-label="Cerrar">×</button></div>
            <p className="modal-intro">Registra una entrada, salida o merma. La existencia se recalculará desde el historial.</p>
            <form onSubmit={submitMovement}>
              <label>Producto<select required value={selectedProduct} onChange={(event) => setSelectedProduct(event.target.value)}>{products.map((product) => <option value={product.id} key={product.id}>{product.name} · {product.sku}</option>)}</select></label>
              <label>Local<select required value={selectedLocation} onChange={(event) => setSelectedLocation(event.target.value)}>{locations.map((location) => <option value={location.id} key={location.id}>{location.name}</option>)}</select></label>
              <div className="form-row">
                <label>Tipo de movimiento<select value={movementType} onChange={(event) => setMovementType(event.target.value as MovementType)}><option value="ENTRADA">Entrada</option><option value="SALIDA">Salida</option><option value="MERMA">Merma</option></select></label>
                <label>Cantidad ({selectedProductData?.unit ?? "unidades"})<input required type="number" min="0.01" step="any" value={quantity} onChange={(event) => setQuantity(event.target.value)} placeholder="0" /></label>
              </div>
              <label>Referencia <span className="optional">(opcional)</span><input value={reference} onChange={(event) => setReference(event.target.value)} placeholder="Factura, venta u orden" /></label>
              <label>Notas <span className="optional">(opcional)</span><textarea value={notes} onChange={(event) => setNotes(event.target.value)} rows={3} placeholder="Añade un detalle para trazabilidad" /></label>
              <div className="modal-note"><span>i</span> Fecha y hora se asignan automáticamente al registrar.</div>
              <div className="modal-actions"><button type="button" className="secondary-button" onClick={() => setFormOpen(false)}>Cancelar</button><button type="submit" className="primary-button" disabled={submitting || !products.length || !locations.length}>{submitting ? "Registrando…" : "Confirmar movimiento"}</button></div>
            </form>
          </section>
        </div>
      )}
    </main>
  );
}
