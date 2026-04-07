import React from 'react';

export function VariationCarousel({ variations }) {
  return (
    <section className="mt-8">
      <h2 className="font-semibold">Design Variations</h2>
      <div className="mt-2 flex gap-3 overflow-auto pb-2">
        {variations.map((v) => (
          <article key={v.id} className="min-w-[220px] rounded border p-3">
            <p className="font-medium">{v.dress}</p>
            <p>{v.color} / {v.fabric}</p>
            <p>Border: {v.border}</p>
            <p>Pattern: {v.pattern}</p>
            <p>Sleeve: {v.sleeve}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
