import SurveyForm from 'components/SurveyForm'
import BurglaryMap from 'components/BurglaryMap'
import wardGeo from '../police-dashboard/data/ward_choro.json'
export default function Home() {
  const handleSurvey = data => console.log('survey', data)
  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-blue-800 text-white p-4 text-xl">Community Safety Feedback</header>
      <main className="flex-1 p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
        <section>
          <h2 className="text-lg font-semibold mb-4">Your Feedback</h2>
          <SurveyForm onSubmit={handleSurvey} />
        </section>
        <section>
          <h2 className="text-lg font-semibold mb-4">Burglaries in Your Ward</h2>
          <BurglaryMap
            geojson={wardGeo}
            center={[51.5074, -0.1278]}
            zoom={10}
          />
        </section>
      </main>
      <footer className="bg-gray-200 text-center p-2">© Met Police Data Demo</footer>
    </div>
  )
}