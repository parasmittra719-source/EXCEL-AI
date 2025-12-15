import { useState, useEffect } from "react";
import * as XLSX from "xlsx";
import axios from "axios";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend);

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";
const WS_BASE_URL = API_BASE_URL.replace(/^http/, "ws");

console.log("Current API Config:", { API_BASE_URL, WS_BASE_URL });

function App() {
  const [rows, setRows] = useState<any[]>([]);
  const [cols, setCols] = useState<string[]>([]);
  const [targets, setTargets] = useState<string[]>([]);
  const [forecasts, setForecasts] = useState<Record<string, number[]>>({});
  const [token, setToken] = useState("");
  const [insight, setInsight] = useState("");
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("admin");
  const [org, setOrg] = useState("");
  const [role, setRole] = useState("");

  // Auto-Analyze when forecast updates
  useEffect(() => {
    if (Object.keys(forecasts).length > 0) {
      askAI();
    }
  }, [forecasts]);

  const askAI = async () => {
    // Fix: Send 'forecasts' instead of raw 'rows' for better context
    const payload = {
      data: Object.keys(forecasts).map(k => ({ metric: k, values: forecasts[k] }))
    };
    try {
      const res = await axios.post(`${API_BASE_URL}/insight`, payload);
      setInsight(res.data.insight);
    } catch (e) {
      console.error("AI Analysis failed", e);
    }
  };

  // Calculate Live Stats
  const calculateStats = () => {
    if (!Object.keys(forecasts).length) return null;

    // Aggregate across all metrics
    const stats = Object.entries(forecasts).map(([key, values]) => {
      const start = values[0];
      const end = values[values.length - 1];
      const growth = ((end - start) / start) * 100;
      const avg = values.reduce((a, b) => a + b, 0) / values.length;
      return { key, growth: growth.toFixed(1), avg: avg.toFixed(1), end: end.toFixed(0) };
    });
    return stats;
  };

  const liveStats = calculateStats();

  const doLogin = async () => {
    try {
      const res = await axios.post(`${API_BASE_URL}/login`, {
        username: username,
        password: password
      });
      setToken(res.data.token);
      axios.defaults.headers.common["Authorization"] = `Bearer ${res.data.token}`;

      const payload = JSON.parse(atob(res.data.token.split('.')[1]));
      setOrg(payload.org_name);
      setRole(payload.role);
    } catch (e) {
      alert("Login failed! Check credentials or server.");
    }
  };

  const sendEmail = async () => {
    try {
      await axios.post(`${API_BASE_URL}/email-report`, {
        email: "test@example.com",
        content: insight || "No insight generated yet."
      });
      alert("Email sent!");
    } catch (e) {
      alert("Error sending email");
    }
  };

  // Real-time Refresh via Websocket
  useEffect(() => {
    // Only connect if we have data to refresh
    if (!rows.length || !targets.length) return;

    console.log("Connecting to WebSocket...");
    const ws = new WebSocket(`${WS_BASE_URL}/ws`);

    ws.onmessage = (event) => {
      if (event.data === "refresh") {
        console.log("Received refresh signal via WS");
        runForecast();
      }
    };

    ws.onerror = (e) => console.error("WS Error:", e);

    return () => {
      console.log("Closing WebSocket...");
      ws.close();
    };
  }, [rows, targets]); // Re-connect if data changes (simple approach)

  const upload = (e: any) => {
    const reader = new FileReader();
    reader.onload = evt => {
      const wb = XLSX.read(evt.target?.result, { type: "binary" });
      const sheet = wb.Sheets[wb.SheetNames[0]];
      const data = XLSX.utils.sheet_to_json(sheet) as any[];
      setRows(data);
      if (data.length > 0) {
        // Only show numeric columns for forecasting
        const numericKeys = Object.keys(data[0]).filter(key => {
          const val = data[0][key];
          return typeof val === 'number';
        });
        setCols(numericKeys);
        setTargets(numericKeys); // Auto-select all numeric columns for intelligent default
      }
    };
    reader.readAsBinaryString(e.target.files[0]);
  };

  const runForecast = async () => {
    if (!targets.length) {
      alert("Please select at least one numeric metric.");
      return;
    }

    if (!rows.length) {
      alert("No data uploaded.");
      return;
    }

    try {
      const res = await axios.post(`${API_BASE_URL}/forecast`, {
        rows,
        targets
      });
      setForecasts(res.data.forecasts);
    } catch (e: any) {
      console.error(e);
      const msg = e.response?.data?.detail || e.message || "Unknown error";
      alert(`Forecast failed: ${msg}`);
    }
  };

  const toggleTarget = (col: string) => {
    if (targets.includes(col)) {
      setTargets(targets.filter(t => t !== col));
    } else {
      setTargets([...targets, col]);
    }
  };

  const colors = ["#4f46e5", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899"];


  if (!token) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
        <div className="w-full max-w-md p-8 space-y-8 bg-white rounded-lg shadow-lg">
          <div className="text-center">
            <h1 className="text-3xl font-extrabold text-gray-900">AI Analytics</h1>
            <p className="mt-2 text-sm text-gray-600">Enterprise Dashboard Login</p>
          </div>
          <div className="mt-8 space-y-6">
            <input
              type="text"
              placeholder="Username"
              className="w-full px-3 py-2 border border-gray-300 rounded-md bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              onChange={e => setUsername(e.target.value)}
            />
            <input
              type="password"
              placeholder="Password"
              className="w-full px-3 py-2 border border-gray-300 rounded-md bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              onChange={e => setPassword(e.target.value)}
            />
            <button
              onClick={doLogin}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Sign In (Demo)
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-100 font-sans">
      {/* Sidebar */}
      <div className="w-64 bg-indigo-900 text-white flex flex-col">
        <div className="h-16 flex items-center justify-center text-2xl font-bold bg-indigo-800">
          Nexus AI
        </div>
        <nav className="flex-1 px-2 py-4 space-y-2">
          <div className="flex items-center px-4 py-2 bg-indigo-800 rounded-md text-gray-100 cursor-pointer">
            Analytics
          </div>
          <div
            onClick={() => alert("Reports module coming soon!")}
            className="flex items-center px-4 py-2 hover:bg-indigo-700 rounded-md text-gray-300 cursor-pointer"
          >
            Reports
          </div>
          <div
            onClick={() => alert("Settings module coming soon!")}
            className="flex items-center px-4 py-2 hover:bg-indigo-700 rounded-md text-gray-300 cursor-pointer"
          >
            Settings
          </div>
        </nav>
        <div className="p-4 bg-indigo-800">
          <div className="text-sm font-medium">{org}</div>
          <div className="text-xs text-indigo-300">{role}</div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Header */}
        <header className="h-16 bg-white shadow flex items-center justify-between px-6 z-10">
          <h2 className="text-xl font-semibold text-gray-800">Dashboard Overview</h2>
          <div className="flex items-center space-x-4">
            <span className={`text-sm px-3 py-1 rounded-full ${rows.length > 0 ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"}`}>
              {rows.length > 0 ? "Dataset Active" : "Waiting for Data"}
            </span>
          </div>
        </header>

        {/* Dashboard Grid */}
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

            {/* Control Panel */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 lg:col-span-2">
              <h3 className="text-lg font-medium text-gray-900 mb-6 flex items-center">
                <span className="w-2 h-8 bg-indigo-500 rounded mr-3"></span>
                Data Controls
              </h3>

              {/* Live Stats Board */}
              {liveStats && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  {liveStats.map(s => (
                    <div key={s.key} className="bg-indigo-50 p-3 rounded-lg border border-indigo-100">
                      <div className="text-xs text-indigo-500 uppercase font-bold">{s.key} Growth</div>
                      <div className={`text-xl font-bold ${Number(s.growth) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {Number(s.growth) >= 0 ? '+' : ''}{s.growth}%
                      </div>
                      <div className="text-xs text-gray-500 mt-1">
                        Avg: {s.avg} | Final: {s.end}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-end">
                <div className="w-full">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Upload Dataset (CSV)</label>
                  <input
                    type="file"
                    onChange={upload}
                    className="block w-full text-sm text-gray-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Metrics to Analyze</label>
                  <div className="flex flex-wrap gap-2 max-h-24 overflow-y-auto">
                    {cols.length > 0 ? cols.map(c => (
                      <button
                        key={c}
                        onClick={() => toggleTarget(c)}
                        className={`text-xs px-2 py-1 rounded-full border ${targets.includes(c) ? 'bg-indigo-100 border-indigo-500 text-indigo-700 font-semibold' : 'bg-gray-50 border-gray-200 text-gray-500 hover:bg-gray-100'}`}
                      >
                        {c}
                      </button>
                    )) : <span className="text-sm text-gray-400">Upload data first</span>}
                  </div>
                </div>
                <div>
                  <button
                    onClick={runForecast}
                    disabled={!rows.length || !targets.length}
                    className={`w-full py-2.5 px-6 rounded-lg text-white font-medium transition-all shadow-md ${(!rows.length || !targets.length) ? 'bg-gray-300 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700 hover:shadow-lg'}`}
                  >
                    Generate Forecast
                  </button>
                </div>
              </div>
            </div>

            {/* Chart Section */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-[500px] flex flex-col">
              <h3 className="text-lg font-medium text-gray-900 mb-6 flex items-center">
                <span className="w-2 h-8 bg-blue-500 rounded mr-3"></span>
                Forecast Visualization
              </h3>
              <div className="flex-1 relative">
                {Object.keys(forecasts).length > 0 ? (
                  <Line
                    data={{
                      labels: Object.values(forecasts)[0].map((_, i) => `Month ${i + 1}`),
                      datasets: Object.keys(forecasts).map((key, idx) => ({
                        label: key,
                        data: forecasts[key],
                        borderColor: colors[idx % colors.length],
                        backgroundColor: `${colors[idx % colors.length]}20`, // 20% opacity
                        borderWidth: 2,
                        pointBackgroundColor: "#ffffff",
                        pointBorderColor: colors[idx % colors.length],
                        pointRadius: 4,
                        tension: 0.4,
                      }))
                    }}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: { legend: { display: true, position: 'top' } },
                      scales: {
                        y: { grid: { color: "#f3f4f6" }, border: { display: false } },
                        x: { grid: { display: false }, border: { display: false } }
                      }
                    }}
                  />
                ) : (
                  <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-400 border-2 border-dashed border-gray-200 rounded-lg">
                    <svg className="w-16 h-16 mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
                    <span>No forecast generated. Upload data and click Generate.</span>
                  </div>
                )}
              </div>
            </div>

            {/* Insights Panel */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-[500px] flex flex-col">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-medium text-gray-900 flex items-center">
                  <span className="w-2 h-8 bg-purple-500 rounded mr-3"></span>
                  AI Business Insights
                </h3>
                <div className="flex space-x-3">
                  <button
                    onClick={askAI}
                    disabled={!rows.length}
                    className="flex items-center bg-purple-50 text-purple-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-purple-100 transition-colors"
                  >
                    Analyze
                  </button>
                  <button
                    onClick={sendEmail}
                    disabled={!insight}
                    className="flex items-center bg-green-50 text-green-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-100 transition-colors"
                  >
                    Email Report
                  </button>
                </div>
              </div>
              <div className="flex-1 bg-gray-900 text-gray-300 p-6 rounded-lg overflow-y-auto font-mono text-sm leading-relaxed whitespace-pre-wrap shadow-inner">
                {insight || "// AI Analysis will appear here...\n// 1. Upload Data\n// 2. Click Analyze"}
              </div>
            </div>

          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
