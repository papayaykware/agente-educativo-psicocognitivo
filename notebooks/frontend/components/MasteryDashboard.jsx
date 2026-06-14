import { useEffect, useState } from "react";
import { apiGet } from "../api/client";
import { BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

export default function MasteryDashboard({ studentId }) {
  const [data, setData] = useState([]);

  useEffect(() => {
    async function load() {
      const res = await apiGet(`/dkt/mastery/${studentId}`);
      const formatted = Object.entries(res.mastery).map(([concept, value]) => ({
        concept,
        value
      }));
      setData(formatted);
    }
    load();
  }, [studentId]);

  return (
    <div>
      <h3>Mastery del estudiante</h3>
      <BarChart width={400} height={250} data={data}>
        <XAxis dataKey="concept" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="value" fill="#4f46e5" />
      </BarChart>
    </div>
  );
}
