import MasteryDashboard from "../components/MasteryDashboard";
import CognitiveLoadIndicator from "../components/CognitiveLoadIndicator";

export default function StudentView({ studentId }) {
  return (
    <div>
      <h2>Panel del Estudiante</h2>
      <MasteryDashboard studentId={studentId} />
      <CognitiveLoadIndicator load={0.42} />
    </div>
  );
}
