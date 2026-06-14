export default function CognitiveLoadIndicator({ load }) {
  const color = load < 0.4 ? "green" : load < 0.7 ? "orange" : "red";

  return (
    <div style={{ padding: 10 }}>
      <h4>Carga cognitiva</h4>
      <div style={{ width: 200, height: 20, background: "#eee" }}>
        <div style={{ width: `${load * 100}%`, height: "100%", background: color }} />
      </div>
    </div>
  );
}
