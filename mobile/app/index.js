import React, { useState } from 'react';
import { ScrollView, Text, TextInput, View } from 'react-native';
import { VariationCards } from '../components/VariationCards';

export default function App() {
  const [color, setColor] = useState('red');

  return (
    <ScrollView contentContainerStyle={{ padding: 16, gap: 12 }}>
      <Text style={{ fontSize: 24, fontWeight: '700' }}>SmartStitch Mobile Try-On</Text>
      <TextInput
        value={color}
        onChangeText={setColor}
        placeholder="Selected color"
        style={{ borderWidth: 1, borderColor: '#ccc', borderRadius: 8, padding: 10 }}
      />
      <View>
        <Text>AR Target: ARCore / WebXR bridge ready.</Text>
      </View>
      <VariationCards color={color} />
    </ScrollView>
  );
}
