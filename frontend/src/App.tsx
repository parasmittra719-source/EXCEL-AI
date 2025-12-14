import { useState, useEffect } from "react";
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

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";
const WS_BASE_URL = API_BASE_URL.replace(/^http/, "ws");

console.log("Current API Config:", { API_BASE_URL, WS_BASE_URL });

function App() {
  const [rows, setRows] = useState<any[]>([]);
  const [cols, setCols] = useState<string[]>([]);
  const [target, setTarget] = useState("");
  const [forecast, setForecast] = useState<number[]>([]);
  const [token, setToken] = useState("");
  const [insight, setInsight] = useState("");
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("admin");
  const [org, setOrg] = useState("");
  const [role, setRole] = useState("");

  const askAI = async () => {
    const res = await axios.post(`${API_BASE_URL}/insight`, { data: rows });
    setInsight(res.data.insight);
  };

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
    if (!rows.length || !target) return;

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
  }, [rows, target]); // Re-connect if data changes (simple approach)

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
    if (!target || target === "Select Metric") {
      alert("Please select a valid Target Metric column.");
      return;
    }

    if (!rows.length) {
      alert("No data uploaded.");
      return;
    }

    try {
      const res = await axios.post(`${API_BASE_URL}/forecast`, {
        rows,
        target
      });
      setForecast(res.data.forecast);
    } catch (e: any) {
      console.error(e);
      const msg = e.response?.data?.detail || e.message || "Unknown error";
      alert(`Forecast failed: ${msg}`);
    }
  };


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
          <div className="flex items-center px-4 py-2 hover:bg-indigo-700 rounded-md text-gray-300 cursor-pointer">
            Reports
          </div>
          <div className="flex items-center px-4 py-2 hover:bg-indigo-700 rounded-md text-gray-300 cursor-pointer">
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
                  <label className="block text-sm font-medium text-gray-700 mb-2">Target Metric</label>
                  <select
                    onChange={e => setTarget(e.target.value)}
                    className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white"
                  >
                    <option>Select Metric</option>
                    {cols.map(c => <option key={c}>{c}</option>)}
                  </select>
                </div>
                <div>
                  <button
                    onClick={runForecast}
                    disabled={!rows.length || !target}
                    className={`w-full py-2.5 px-6 rounded-lg text-white font-medium transition-all shadow-md ${(!rows.length || !target) ? 'bg-gray-300 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700 hover:shadow-lg'}`}
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
                {forecast.length > 0 ? (
                  <Line
                    data={{
                      labels: forecast.map((_, i) => `Month ${i + 1}`),
                      datasets: [
                        {
                          label: "Predicted Growth",
                          data: forecast,
                          borderColor: "#4f46e5",
                          backgroundColor: "rgba(79, 70, 229, 0.1)",
                          borderWidth: 3,
                          pointBackgroundColor: "#ffffff",
                          pointBorderColor: "#4f46e5",
                          pointRadius: 4,
                          tension: 0.4,
                          fill: true
                        },
                      ],
                    }}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: { legend: { display: false } },
                      scales: {
                        y: { grid: { color: "#f3f4f6" }, border: { display: false } },
                        x: { grid: { display: false }, border: { display: false } }
                      }
                    }}
                  />
                ) : (
                  <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-400 border-2 border-dashed border-gray-200 rounded-lg">
                    <svg className="w-16 h-16 mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
                    <span>No data available. Run a forecast to compare.</span>
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
