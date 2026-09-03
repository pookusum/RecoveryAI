import { useEffect, useState } from "react";
import {
  LayoutDashboard,
  Activity,
  Brain,
  ArrowUpRight,
  RefreshCw,
  AlertCircle,
  Search,
  CheckCircle,
  Clock,
  XCircle,
  ChevronRight,
  BarChart3,
} from "lucide-react";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [activePage, setActivePage] = useState("dashboard");

  return (
    <div className="app">

      {/* ================= SIDEBAR ================= */}

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

          <div
            className={`nav-item ${
              activePage === "dashboard" ? "active" : ""
            }`}
            onClick={() => setActivePage("dashboard")}
          >
            <LayoutDashboard size={19} />
            Dashboard
          </div>

          <div
            className={`nav-item ${
              activePage === "transactions" ? "active" : ""
            }`}
            onClick={() => setActivePage("transactions")}
          >
            <Activity size={19} />
            Transactions
          </div>

          <div
            className={`nav-item ${
              activePage === "analysis" ? "active" : ""
            }`}
            onClick={() => setActivePage("analysis")}
          >
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

      {/* ================= MAIN ================= */}

      <main className="main">

        {activePage === "dashboard" && (
          <Dashboard />
        )}

        {activePage === "transactions" && (
          <Transactions />
        )}

        {activePage === "analysis" && (
          <AIAnalysis />
        )}

      </main>

    </div>
  );
}


/* =========================================================
   DASHBOARD
========================================================= */

function Dashboard() {

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

    <>
      {/* Header */}

      <header className="topbar">

        <div>

          <p className="eyebrow">
            AI REVENUE RECOVERY
          </p>

          <h1>
            Recovery Dashboard
          </h1>

          <p className="subtitle">
            Monitor failed payments and optimize recovery decisions.
          </p>

        </div>

        <button
          className="refresh-btn"
          onClick={fetchStats}
        >
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
          value={`₹${(
            stats?.total_transaction_value ?? 0
          ).toLocaleString()}`}
          icon={<ArrowUpRight size={20} />}
          loading={loading}
        />

        <StatCard
          title="Avg. Recovery Probability"
          value={`${(
            (stats?.average_recovery_probability ?? 0) * 100
          ).toFixed(1)}%`}
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

              <h3>
                Recovery Overview
              </h3>

              <p>
                Current recovery opportunities
              </p>

            </div>

          </div>


          <div className="overview-content">

            <div className="recovery-circle">

              <div>

                <strong>
                  {(
                    (stats?.average_recovery_probability ?? 0) *
                    100
                  ).toFixed(0)}
                  %
                </strong>

                <span>
                  Avg. Recovery
                </span>

              </div>

            </div>


            <div className="overview-details">

              <div className="metric-row">

                <span>
                  High Recovery Opportunities
                </span>

                <strong>
                  {stats?.high_recovery_opportunities ?? 0}
                </strong>

              </div>


              <div className="metric-row">

                <span>
                  Recommended Actions
                </span>

                <strong>
                  {stats?.recommended_actions ?? 0}
                </strong>

              </div>


              <div className="metric-row">

                <span>
                  Amount Recovered
                </span>

                <strong>
                  ₹{(
                    stats?.total_amount_recovered ?? 0
                  ).toLocaleString()}
                </strong>

              </div>

            </div>

          </div>

        </div>


        {/* AI Engine */}

        <div className="panel">

          <div className="panel-header">

            <div>

              <h3>
                AI Engine
              </h3>

              <p>
                Decision engine status
              </p>

            </div>

          </div>


          <div className="ai-status">

            <div className="ai-icon">
              <Brain size={28} />
            </div>

            <h2>
              Operational
            </h2>

            <p>
              RecoverAI is analyzing failed transactions
              and generating recovery recommendations.
            </p>

            <div className="ai-badge">

              <span></span>

              ML Model Active

            </div>

          </div>

        </div>

      </section>


      <footer>
        RecoverAI • AI-powered revenue recovery system
      </footer>

    </>

  );
}


/* =========================================================
   TRANSACTIONS
========================================================= */

function Transactions() {

  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [selectedTransaction, setSelectedTransaction] =
    useState(null);


  const fetchTransactions = async () => {

    try {

      setLoading(true);

      const response =
        await fetch(`${API_URL}/transactions`);

      if (!response.ok) {
        throw new Error("Failed to fetch transactions");
      }

      const data = await response.json();

      setTransactions(data.transactions || []);

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);

    }

  };


  useEffect(() => {
    fetchTransactions();
  }, []);


  const filteredTransactions =
    transactions.filter((transaction) =>
      transaction.case_id
        .toLowerCase()
        .includes(search.toLowerCase()) ||
      transaction.customer_id
        .toLowerCase()
        .includes(search.toLowerCase()) ||
      transaction.failure_reason
        .toLowerCase()
        .includes(search.toLowerCase())
    );


  return (

    <>

      <header className="topbar">

        <div>

          <p className="eyebrow">
            TRANSACTION MANAGEMENT
          </p>

          <h1>
            Transactions
          </h1>

          <p className="subtitle">
            Monitor failed payments and recovery opportunities.
          </p>

        </div>

        <button
          className="refresh-btn"
          onClick={fetchTransactions}
        >
          <RefreshCw size={17} />
          Refresh
        </button>

      </header>


      <div className="panel transaction-panel">

        <div className="transaction-toolbar">

          <div className="search-box">

            <Search size={18} />

            <input
              type="text"
              placeholder="Search transaction..."
              value={search}
              onChange={(e) =>
                setSearch(e.target.value)
              }
            />

          </div>

          <div className="transaction-count">
            {transactions.length} transactions
          </div>

        </div>


        {loading ? (

          <div className="empty-state">
            Loading transactions...
          </div>

        ) : filteredTransactions.length === 0 ? (

          <div className="empty-state">
            No transactions found.
          </div>

        ) : (

          <div className="transaction-table">

            <div className="table-header">

              <span>Transaction</span>
              <span>Customer</span>
              <span>Amount</span>
              <span>Recovery</span>
              <span>Action</span>
              <span>Status</span>
              <span></span>

            </div>


            {filteredTransactions.map(
              (transaction) => (

                <div
                  className="table-row"
                  key={transaction.case_id}
                >

                  <span className="transaction-id">
                    {transaction.case_id}
                  </span>

                  <span>
                    {transaction.customer_id}
                  </span>

                  <span>
                    ₹{Number(
                      transaction.amount
                    ).toLocaleString()}
                  </span>

                  <span>

                    <strong
                      className={
                        transaction.recovery_probability >= 0.7
                          ? "probability-high"
                          : "probability-low"
                      }
                    >
                      {(
                        transaction.recovery_probability * 100
                      ).toFixed(1)}%
                    </strong>

                  </span>

                  <span>
                    {transaction.recommended_action}
                  </span>

                  <span>

                    <StatusBadge
                      status={
                        transaction.action_status
                      }
                    />

                  </span>

                  <button
                    className="view-btn"
                    onClick={() =>
                      setSelectedTransaction(
                        transaction.case_id
                      )
                    }
                  >
                    <ChevronRight size={17} />
                  </button>

                </div>

              )
            )}

          </div>

        )}

      </div>


      {/* Transaction Details */}

      {selectedTransaction && (

        <TransactionDetails
          caseId={selectedTransaction}
          onClose={() =>
            setSelectedTransaction(null)
          }
        />

      )}

    </>

  );

}


/* =========================================================
   TRANSACTION DETAILS
========================================================= */

function TransactionDetails({
  caseId,
  onClose,
}) {

  const [transaction, setTransaction] =
    useState(null);


  useEffect(() => {

    const fetchTransaction = async () => {

      try {

        const response =
          await fetch(
            `${API_URL}/transactions/${caseId}`
          );

        const data = await response.json();

        setTransaction(data);

      } catch (error) {

        console.error(error);

      }

    };

    fetchTransaction();

  }, [caseId]);


  if (!transaction) {

    return (
      <div className="modal-overlay">
        <div className="modal">
          Loading transaction...
        </div>
      </div>
    );

  }


  return (

    <div className="modal-overlay">

      <div className="modal">

        <div className="modal-header">

          <div>

            <p className="eyebrow">
              TRANSACTION DETAILS
            </p>

            <h2>
              {transaction.case_id}
            </h2>

          </div>

          <button
            className="modal-close"
            onClick={onClose}
          >
            ×
          </button>

        </div>


        <div className="details-grid">

          <Detail
            label="Customer ID"
            value={transaction.customer_id}
          />

          <Detail
            label="Payment ID"
            value={transaction.payment_id}
          />

          <Detail
            label="Amount"
            value={`₹${Number(
              transaction.amount
            ).toLocaleString()}`}
          />

          <Detail
            label="Failure Reason"
            value={transaction.failure_reason}
          />

          <Detail
            label="Previous Successes"
            value={transaction.previous_successes}
          />

          <Detail
            label="Previous Failures"
            value={transaction.previous_failures}
          />

          <Detail
            label="Customer Lifetime Value"
            value={`₹${Number(
              transaction.customer_lifetime_value
            ).toLocaleString()}`}
          />

          <Detail
            label="Retry Count"
            value={transaction.retry_count}
          />

          <Detail
            label="Risk Score"
            value={transaction.risk_score}
          />

          <Detail
            label="Recovery Probability"
            value={`${(
              transaction.recovery_probability * 100
            ).toFixed(1)}%`}
          />

          <Detail
            label="Recommended Action"
            value={transaction.recommended_action}
          />

          <Detail
            label="Action Status"
            value={transaction.action_status}
          />

        </div>


        <div className="decision-box">

          <h3>
            AI Policy Decision
          </h3>

          <p>
            {transaction.policy_decision}
          </p>

        </div>


        <div className="modal-footer">

          <span>
            Amount Recovered:
          </span>

          <strong>
            ₹{Number(
              transaction.amount_recovered || 0
            ).toLocaleString()}
          </strong>

        </div>

      </div>

    </div>

  );

}


/* =========================================================
   AI ANALYSIS
========================================================= */

function AIAnalysis() {
  const [form, setForm] = useState({
    transaction_id: "TXN-TEST-004",
    customer_id: "CUST-1004",
    amount: 10000,
    failure_reason: "temporary_bank_decline",
    previous_successes: 8,
    previous_failures: 1,
    customer_lifetime_value: 75000,
    retry_count: 1,
    days_since_last_payment: 5,
    checkout_duration: 240,
    payment_method: "card",
    risk_score: 0.25,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;

    setForm((prev) => ({
      ...prev,
      [name]: [
        "amount",
        "previous_successes",
        "previous_failures",
        "customer_lifetime_value",
        "retry_count",
        "days_since_last_payment",
        "checkout_duration",
        "risk_score",
      ].includes(name)
        ? Number(value)
        : value,
    }));
  };

  const analyzeTransaction = async (e) => {
    e.preventDefault();

    setLoading(true);
    setResult(null);
    setError("");

    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Transaction analysis failed"
        );
      }

      setResult(data);
    } catch (error) {
      console.error(error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const probability = result
    ? result.recovery_probability * 100
    : 0;

  const action = result?.decision?.action || "manual_review";

  const shouldExecute =
    result?.decision?.should_execute || false;

  return (
    <>
      {/* ================= PAGE HEADER ================= */}

      <header className="topbar">
        <div>
          <p className="eyebrow">MACHINE LEARNING</p>

          <h1>AI Analysis</h1>

          <p className="subtitle">
            Analyze a failed transaction and generate
            an intelligent recovery decision.
          </p>
        </div>
      </header>

      {/* ================= ANALYSIS LAYOUT ================= */}

      <div className="analysis-layout">

        {/* ================= INPUT PANEL ================= */}

        <div className="panel analysis-form-panel">

          <div className="panel-header">
            <div>
              <h3>Transaction Input</h3>

              <p>
                Enter transaction details for AI-powered
                recovery analysis.
              </p>
            </div>

            <div className="analysis-panel-icon">
              <Brain size={21} />
            </div>
          </div>

          <form
            className="analysis-form"
            onSubmit={analyzeTransaction}
          >

            <div className="form-section-title">
              Transaction Information
            </div>

            <div className="form-grid">

              <Input
                label="Transaction ID"
                name="transaction_id"
                value={form.transaction_id}
                onChange={handleChange}
              />

              <Input
                label="Customer ID"
                name="customer_id"
                value={form.customer_id}
                onChange={handleChange}
              />

              <Input
                label="Amount (₹)"
                name="amount"
                type="number"
                value={form.amount}
                onChange={handleChange}
              />

              <Input
                label="Failure Reason"
                name="failure_reason"
                value={form.failure_reason}
                onChange={handleChange}
              />

            </div>

            <div className="form-section-title">
              Customer History
            </div>

            <div className="form-grid">

              <Input
                label="Previous Successes"
                name="previous_successes"
                type="number"
                value={form.previous_successes}
                onChange={handleChange}
              />

              <Input
                label="Previous Failures"
                name="previous_failures"
                type="number"
                value={form.previous_failures}
                onChange={handleChange}
              />

              <Input
                label="Customer Lifetime Value (₹)"
                name="customer_lifetime_value"
                type="number"
                value={form.customer_lifetime_value}
                onChange={handleChange}
              />

              <Input
                label="Days Since Last Payment"
                name="days_since_last_payment"
                type="number"
                value={form.days_since_last_payment}
                onChange={handleChange}
              />

            </div>

            <div className="form-section-title">
              Payment & Risk Signals
            </div>

            <div className="form-grid">

              <Input
                label="Retry Count"
                name="retry_count"
                type="number"
                value={form.retry_count}
                onChange={handleChange}
              />

              <Input
                label="Checkout Duration (seconds)"
                name="checkout_duration"
                type="number"
                value={form.checkout_duration}
                onChange={handleChange}
              />

              <Input
                label="Payment Method"
                name="payment_method"
                value={form.payment_method}
                onChange={handleChange}
              />

              <Input
                label="Risk Score (0 - 1)"
                name="risk_score"
                type="number"
                step="0.01"
                min="0"
                max="1"
                value={form.risk_score}
                onChange={handleChange}
              />

            </div>

            <button
              className="analyze-btn"
              type="submit"
              disabled={loading}
            >
              {loading ? (
                <>
                  <RefreshCw
                    size={18}
                    className="spin"
                  />
                  Analyzing Transaction...
                </>
              ) : (
                <>
                  <Brain size={18} />
                  Analyze Transaction
                </>
              )}
            </button>

          </form>

          {error && (
            <div className="error-message">
              <XCircle size={18} />
              <span>{error}</span>
            </div>
          )}

        </div>

        {/* ================= AI RESULT PANEL ================= */}

        <div className="panel result-panel">

          <div className="panel-header">
            <div>
              <h3>AI Decision</h3>

              <p>
                Recovery model output and recommended action.
              </p>
            </div>

            <div className="analysis-panel-icon">
              <BarChart3 size={21} />
            </div>
          </div>

          {!result ? (

            <div className="analysis-empty">

              <div className="analysis-empty-icon">
                <BarChart3 size={30} />
              </div>

              <h3>No analysis yet</h3>

              <p>
                Submit a transaction to see the ML
                prediction and recovery recommendation.
              </p>

              <div className="empty-hint">
                <Brain size={15} />
                AI model ready for analysis
              </div>

            </div>

          ) : (

            <div className="analysis-result">

              {/* ================= PROBABILITY ================= */}

              <div className="probability-card">

                <div className="probability-header">
                  <div>
                    <span>Recovery Probability</span>

                    <small>
                      ML model confidence
                    </small>
                  </div>

                  <div className="probability-value">
                    {probability.toFixed(1)}%
                  </div>
                </div>

                <div className="probability-track">
                  <div
                    className="probability-fill"
                    style={{
                      width: `${Math.min(
                        probability,
                        100
                      )}%`,
                    }}
                  ></div>
                </div>

                <div className="probability-labels">
                  <span>Low</span>
                  <span>Medium</span>
                  <span>High</span>
                </div>

              </div>

              {/* ================= ACTION ================= */}

              <div className="decision-highlight">

                <div className="decision-icon">
                  <Brain size={24} />
                </div>

                <div className="decision-content">

                  <span className="decision-label">
                    Recommended Action
                  </span>

                  <strong>
                    {action.replaceAll("_", " ")}
                  </strong>

                </div>

              </div>

              {/* ================= EXECUTION STATUS ================= */}

              <div
                className={
                  shouldExecute
                    ? "result-status success"
                    : "result-status pending"
                }
              >

                {shouldExecute ? (
                  <>
                    <CheckCircle size={20} />

                    <div>
                      <strong>
                        Action recommended for execution
                      </strong>

                      <span>
                        The decision engine considers this
                        transaction suitable for automated recovery.
                      </span>
                    </div>
                  </>
                ) : (
                  <>
                    <Clock size={20} />

                    <div>
                      <strong>
                        Manual review required
                      </strong>

                      <span>
                        The transaction should remain pending
                        until further review.
                      </span>
                    </div>
                  </>
                )}

              </div>

              {/* ================= DECISION REASON ================= */}

              <div className="reason-box">

                <div className="reason-title">
                  <AlertCircle size={18} />

                  <h4>Decision Reason</h4>
                </div>

                <p>
                  {result.decision?.reason}
                </p>

              </div>

              {/* ================= TRANSACTION SUMMARY ================= */}

              <div className="result-summary">

                <div className="summary-item">
                  <span>Transaction</span>
                  <strong>
                    {form.transaction_id}
                  </strong>
                </div>

                <div className="summary-item">
                  <span>Amount</span>
                  <strong>
                    ₹{Number(form.amount).toLocaleString()}
                  </strong>
                </div>

                <div className="summary-item">
                  <span>Risk Score</span>
                  <strong>
                    {Number(form.risk_score).toFixed(2)}
                  </strong>
                </div>

                <div className="summary-item">
                  <span>Retry Count</span>
                  <strong>
                    {form.retry_count}
                  </strong>
                </div>

              </div>

              {/* ================= AUDIT ================= */}

              <div className="audit-box">

                <div className="audit-header">
                  <div>
                    <h4>Audit Record</h4>

                    <span>
                      Decision trace generated by RecoverAI
                    </span>
                  </div>

                  <CheckCircle size={18} />
                </div>

                <pre>
                  {JSON.stringify(
                    result.audit,
                    null,
                    2
                  )}
                </pre>

              </div>

            </div>

          )}

        </div>

      </div>
    </>
  );
}

/* =========================================================
   REUSABLE COMPONENTS
========================================================= */

function StatCard({
  title,
  value,
  icon,
  loading,
}) {

  return (

    <div className="stat-card">

      <div className="stat-top">

        <span>
          {title}
        </span>

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


function Input({
  label,
  name,
  value,
  onChange,
  type = "text",
  step,
}) {

  return (

    <div className="form-group">

      <label>
        {label}
      </label>

      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        step={step}
        required
      />

    </div>

  );

}


function Detail({
  label,
  value,
}) {

  return (

    <div className="detail-item">

      <span>
        {label}
      </span>

      <strong>
        {value ?? "-"}
      </strong>

    </div>

  );

}


function StatusBadge({
  status,
}) {

  if (status === "RECOMMENDED") {

    return (
      <span className="status-badge recommended">
        <CheckCircle size={14} />
        Recommended
      </span>
    );

  }

  return (

    <span className="status-badge pending">
      <Clock size={14} />
      Pending
    </span>

  );

}


export default App;