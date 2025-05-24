import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet'
export default function BurglaryMap({ geojson, center, zoom }) {
  return (
    <MapContainer center={center} zoom={zoom} className="h-96 w-full">
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <GeoJSON data={geojson} style={() => ({ fillColor: '#f03', weight: 1, fillOpacity: 0.6 })} />
    </MapContainer>
  )
}