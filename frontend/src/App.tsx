import { useState } from "react";
import * as XLSX from "xlsx";
import axios from "axios";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

function App() {
  const [rows, setRows] = useState<any[]>([]);
  const [cols, setCols] = useState<string[]>([]);
  const [target, setTarget] = useState("");
  const [forecast, setForecast] = useState<number[]>([]);
  const [token, setToken] = useState("");
  const [insight, setInsight] = useState("");

  const askAI = async () => {
    const res = await axios.post("http://127.0.0.1:8000/insight", { data: rows });
    setInsight(res.data.insight);
  };

  const doLogin = async () => {
    const res = await axios.post("http://127.0.0.1:8000/login", {
      username: "admin",
      password: "admin"
    });
    setToken(res.data.token);
    axios.defaults.headers.common["Authorization"] = `Bearer ${res.data.token}`;
  };

  const upload = (e: any) => {
    const reader = new FileReader();
    reader.onload = evt => {
      const wb = XLSX.read(evt.target?.result, { type: "binary" });
      const sheet = wb.Sheets[wb.SheetNames[0]];
      const data = XLSX.utils.sheet_to_json(sheet) as any[];
      setRows(data);
      setCols(Object.keys(data[0]));
    };
    reader.readAsBinaryString(e.target.files[0]);
  };

  const runForecast = async () => {
    const res = await axios.post("http://127.0.0.1:8000/forecast", {
      rows,
      target
    });
    setForecast(res.data.forecast);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>AI Analytics Dashboard</h2>
      {!token && <button onClick={doLogin}>Login</button>}
      <br /><br />
      <input type="file" onChange={upload} />
      <br /><br />
      {rows.length > 0 && (
        <>
          <button onClick={askAI}>Get AI Insight</button>
          <pre>{insight}</pre>
          <br /><br />
        </>
      )}
      <select onChange={e => setTarget(e.target.value)}>
        <option>Select Metric</option>
        {cols.map(c => <option key={c}>{c}</option>)}
      </select>
      <br /><br />
      <button onClick={runForecast}>Run Forecast</button>
      <h3>Forecast:</h3>
      {forecast.length > 0 && (
        <Line
          data={{
            labels: forecast.map((_, i) => `F${i + 1}`),
            datasets: [
              {
                label: "Forecast",
                data: forecast,
                borderColor: "blue",
              },
            ],
          }}
        />
      )}
      <pre>{JSON.stringify(forecast, null, 2)}</pre>
    </div>
  );
}

export default App;
