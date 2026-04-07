import React from 'react';
import { Text, View } from 'react-native';

export function VariationCards({ color }) {
  const variations = [
    { border: 'gold-heavy', pattern: 'floral', sleeve: 'elbow' },
    { border: 'temple', pattern: 'paisley', sleeve: 'cap' },
    { border: 'minimal', pattern: 'thread-art', sleeve: 'full' },
  ];

  return (
    <View style={{ gap: 10 }}>
      {variations.map((v, idx) => (
        <View key={idx} style={{ borderWidth: 1, borderColor: '#ddd', borderRadius: 10, padding: 10 }}>
          <Text>{color} saree variation #{idx + 1}</Text>
          <Text>Border: {v.border}</Text>
          <Text>Pattern: {v.pattern}</Text>
          <Text>Sleeve: {v.sleeve}</Text>
        </View>
      ))}
    </View>
  );
}
