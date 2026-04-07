import React from 'react';

export function MeasurementForm() {
  const fields = [
    'height_cm','neck_cm','shoulder_cm','chest_cm','waist_cm','hip_cm',
    'arm_length_cm','wrist_cm','leg_length_cm','thigh_cm','ankle_cm'
  ];

  return (
    <section className="mt-6">
      <h2 className="font-semibold">Manual Measurements</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-2">
        {fields.map((f) => (
          <input key={f} name={f} placeholder={f} className="border p-2 rounded" />
        ))}
      </div>
      <button className="mt-3 rounded bg-black px-4 py-2 text-white">Generate 3D Model</button>
    </section>
  );
}
