import React, { useMemo, useState } from 'react';
import { CATEGORY_COLLECTIONS } from '../lib/catalog';
import { VariationCarousel } from '../components/VariationCarousel';
import { MeasurementForm } from '../components/MeasurementForm';

export function App() {
  const [category, setCategory] = useState('women');
  const [dress, setDress] = useState('Saree');
  const [color, setColor] = useState('red');
  const [fabric, setFabric] = useState('georgette');

  const variations = useMemo(() => {
    const styles = ['temple', 'zari-heavy', 'embroidered', 'contrast-piping'];
    return styles.map((border, idx) => ({
      id: `${dress}-${idx}`,
      dress,
      color,
      fabric,
      border,
      pattern: ['floral', 'paisley', 'geometric', 'thread-art'][idx],
      sleeve: ['cap', 'elbow', 'full', 'ruffled'][idx],
    }));
  }, [dress, color, fabric]);

  return (
    <main className="p-6 font-sans">
      <h1 className="text-2xl font-bold">SmartStitch 3D Customizer</h1>

      <section className="mt-4 grid gap-3 md:grid-cols-4">
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          {Object.keys(CATEGORY_COLLECTIONS).map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>

        <select value={dress} onChange={(e) => setDress(e.target.value)}>
          {CATEGORY_COLLECTIONS[category].map((item) => (
            <option key={item} value={item}>{item}</option>
          ))}
        </select>

        <input value={color} onChange={(e) => setColor(e.target.value)} placeholder="Color" />
        <input value={fabric} onChange={(e) => setFabric(e.target.value)} placeholder="Fabric" />
      </section>

      <MeasurementForm />
      <VariationCarousel variations={variations} />
    </main>
  );
}
