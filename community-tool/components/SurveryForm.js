import { useForm } from 'react-hook-form'
export default function SurveyForm({ onSubmit }) {
  const { register, handleSubmit } = useForm()
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label className="block font-medium">How safe do you feel in your area?</label>
        <select {...register('safety')} className="mt-1 w-full border rounded p-2">
          <option value="very_safe">Very safe</option>
          <option value="safe">Safe</option>
          <option value="neutral">Neutral</option>
          <option value="unsafe">Unsafe</option>
          <option value="very_unsafe">Very unsafe</option>
        </select>
      </div>
      <div>
        <label className="block font-medium">What concerns you most?</label>
        <textarea {...register('concerns')} className="mt-1 w-full border rounded p-2" rows={3} />
      </div>
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">Submit</button>
    </form>
  )
}