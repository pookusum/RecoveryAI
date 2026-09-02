import { useEffect, useState } from "react";
import {
  LayoutDashboard,
  Activity,
  Brain,
  ArrowUpRight,
  RefreshCw,
  AlertCircle,
} from "lucide-react";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchStats = async () => {
    try {
      setLoading(true);

      const response = await fetch(`${API_URL}/stats`);

      if (!response.ok) {
        throw new Error("Failed to fetch statistics");
      }

      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error("Error fetching stats:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">
          <div className="logo-icon">
            <Brain size={22} />
          </div>

          <div>
            <h2>RecoverAI</h2>
            <span>Revenue Intelligence</span>
          </div>
        </div>

        <nav>
          <div className="nav-item active">
            <LayoutDashboard size={19} />
            Dashboard
          </div>

          <div className="nav-item">
            <Activity size={19} />
            Transactions
          </div>

          <div className="nav-item">
            <Brain size={19} />
            AI Analysis
          </div>
        </nav>

        <div className="sidebar-bottom">
          <div className="system-status">
            <span className="status-dot"></span>
            System Operational
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main">
        <header className="topbar">
          <div>
            <p className="eyebrow">AI REVENUE RECOVERY</p>
            <h1>Recovery Dashboard</h1>
            <p className="subtitle">
              Monitor failed payments and optimize recovery decisions.
            </p>
          </div>

          <button className="refresh-btn" onClick={fetchStats}>
            <RefreshCw size={17} />
            Refresh
          </button>
        </header>

        {/* Stats */}
        <section className="stats-grid">
          <StatCard
            title="Total Transactions"
            value={stats?.total_transactions ?? 0}
            icon={<Activity size={20} />}
            loading={loading}
          />

          <StatCard
            title="Transaction Value"
            value={`₹${(stats?.total_transaction_value ?? 0).toLocaleString()}`}
            icon={<ArrowUpRight size={20} />}
            loading={loading}
          />

          <StatCard
            title="Avg. Recovery Probability"
            value={`${((stats?.average_recovery_probability ?? 0) * 100).toFixed(1)}%`}
            icon={<Brain size={20} />}
            loading={loading}
          />

          <StatCard
            title="Recommended Actions"
            value={stats?.recommended_actions ?? 0}
            icon={<AlertCircle size={20} />}
            loading={loading}
          />
        </section>

        {/* Main Panels */}
        <section className="dashboard-grid">
          <div className="panel large-panel">
            <div className="panel-header">
              <div>
                <h3>Recovery Overview</h3>
                <p>Current recovery opportunities</p>
              </div>
            </div>

            <div className="overview-content">
              <div className="recovery-circle">
                <div>
                  <strong>
                    {(
                      (stats?.average_recovery_probability ?? 0) * 100
                    ).toFixed(0)}
                    %
                  </strong>
                  <span>Avg. Recovery</span>
                </div>
              </div>

              <div className="overview-details">
                <div className="metric-row">
                  <span>High Recovery Opportunities</span>
                  <strong>
                    {stats?.high_recovery_opportunities ?? 0}
                  </strong>
                </div>

                <div className="metric-row">
                  <span>Recommended Actions</span>
                  <strong>{stats?.recommended_actions ?? 0}</strong>
                </div>

                <div className="metric-row">
                  <span>Amount Recovered</span>
                  <strong>
                    ₹{(stats?.total_amount_recovered ?? 0).toLocaleString()}
                  </strong>
                </div>
              </div>
            </div>
          </div>

          <div className="panel">
            <div className="panel-header">
              <div>
                <h3>AI Engine</h3>
                <p>Decision engine status</p>
              </div>
            </div>

            <div className="ai-status">
              <div className="ai-icon">
                <Brain size={28} />
              </div>

              <h2>Operational</h2>

              <p>
                RecoveryAI is analyzing failed transactions and generating
                recovery recommendations.
              </p>

              <div className="ai-badge">
                <span></span>
                ML Model Active
              </div>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer>
          RecoverAI • AI-powered revenue recovery system
        </footer>
      </main>
    </div>
  );
}

function StatCard({ title, value, icon, loading }) {
  return (
    <div className="stat-card">
      <div className="stat-top">
        <span>{title}</span>

        <div className="stat-icon">
          {icon}
        </div>
      </div>

      <div className="stat-value">
        {loading ? "..." : value}
      </div>
    </div>
  );
}

export default App;