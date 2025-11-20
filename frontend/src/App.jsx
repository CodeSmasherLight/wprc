import { useState } from "react";

export default function App() {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchReviews = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/reviews");
      if (!res.ok) throw new Error("Failed to fetch reviews");
      const data = await res.json();
      setReviews(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const clearReviews = () => setReviews([]);

  return (
    <div
      style={{
        minHeight: "100vh",
        padding: "24px",
        background: "#f4f6f8",
      }}
    >
      <header style={{ marginBottom: "20px" }}>
        <h1 style={{ margin: 0, fontSize: "28px" }}>WhatsApp Product Reviews</h1>
        <p style={{ marginTop: "6px", color: "#6b7280", fontSize: "14px" }}>
          View customer feedback collected via WhatsApp
        </p>
      </header>

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "12px",
          marginBottom: "16px",
        }}
      >
        <button
          onClick={fetchReviews}
          style={{
            background: "#2563eb",
            color: "#fff",
            padding: "10px 16px",
            borderRadius: "6px",
            border: "none",
            cursor: "pointer",
          }}
        >
          Fetch Reviews
        </button>
        <button
          onClick={clearReviews}
          style={{
            background: "#fff",
            color: "#374151",
            padding: "10px 16px",
            borderRadius: "6px",
            border: "1px solid #d1d5db",
            cursor: "pointer",
          }}
        >
          Clear
        </button>
      </div>

      <div
        style={{
          background: "#fff",
          borderRadius: "8px",
          padding: "16px",
          boxShadow: "0 1px 4px rgba(0,0,0,0.05)",
          maxWidth: "100%",
        }}
      >
        {loading && <p style={{ color: "#6b7280" }}>Loading reviews...</p>}
        {error && <p style={{ color: "#dc2626" }}>{error}</p>}

        {!loading && reviews.length === 0 && !error && (
          <p style={{ color: "#6b7280" }}>Click Fetch Reviews to display data.</p>
        )}

        {reviews.length > 0 && !loading && (
          <div style={{ overflowX: "auto" }}>
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
                fontSize: "14px",
              }}
            >
              <thead>
                <tr style={{ background: "#f9fafb" }}>
                  <th
                    style={{
                      padding: "12px",
                      textAlign: "left",
                      borderBottom: "1px solid #e5e7eb",
                    }}
                  >
                    User
                  </th>
                  <th
                    style={{
                      padding: "12px",
                      textAlign: "left",
                      borderBottom: "1px solid #e5e7eb",
                    }}
                  >
                    Product
                  </th>
                  <th
                    style={{
                      padding: "12px",
                      textAlign: "left",
                      borderBottom: "1px solid #e5e7eb",
                    }}
                  >
                    Review
                  </th>
                  <th
                    style={{
                      padding: "12px",
                      textAlign: "left",
                      borderBottom: "1px solid #e5e7eb",
                    }}
                  >
                    Date
                  </th>
                </tr>
              </thead>
              <tbody>
                {reviews.map((r) => (
                  <tr key={r.id}>
                    <td
                      style={{
                        padding: "12px",
                        borderBottom: "1px solid #f0f0f0",
                      }}
                    >
                      {r.user_name}
                    </td>
                    <td
                      style={{
                        padding: "12px",
                        borderBottom: "1px solid #f0f0f0",
                        fontWeight: 600,
                      }}
                    >
                      {r.product_name}
                    </td>
                    <td
                      style={{
                        padding: "12px",
                        borderBottom: "1px solid #f0f0f0",
                      }}
                    >
                      {r.product_review}
                    </td>
                    <td
                      style={{
                        padding: "12px",
                        borderBottom: "1px solid #f0f0f0",
                        color: "#6b7280",
                      }}
                    >
                      {new Date(r.created_at).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
