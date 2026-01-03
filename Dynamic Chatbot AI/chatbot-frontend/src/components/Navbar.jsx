import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

const Navbar = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  const [dark, setDark] = useState(true);

  // 🔁 Load saved theme
  useEffect(() => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "light") {
      document.documentElement.classList.remove("dark");
      setDark(false);
    } else {
      document.documentElement.classList.add("dark");
      setDark(true);
    }
  }, []);

  const toggleTheme = () => {
  document.documentElement.classList.toggle("dark");

  // optional: persist theme
  const isDark = document.documentElement.classList.contains("dark");
  localStorage.setItem("theme", isDark ? "dark" : "light");
};


  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav style={styles.nav}>
      <Link to="/" style={styles.logo}>AI Chatbot</Link>

      <div style={styles.links}>
        {/* 🌙 Theme Toggle */}
        <button onClick={toggleTheme} style={styles.themeBtn}>
          {dark ? "☀️" : "🌙"}
        </button>

        {token ? (
          <>
            <Link to="/chat">Chat</Link>
            <Link to="/docs">Docs</Link>
            <button onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
};

const styles = {
  nav: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "15px 30px",
    background: "rgba(0,0,0,0.35)",
    backdropFilter: "blur(12px)",
    borderBottom: "1px solid rgba(255,255,255,0.1)",
  },
  logo: {
    fontWeight: "bold",
    fontSize: "20px",
    textDecoration: "none",
  },
  links: {
    display: "flex",
    gap: "20px",
    alignItems: "center",
  },
  themeBtn: {
    background: "rgba(255,255,255,0.15)",
    border: "none",
    borderRadius: "20px",
    padding: "6px 12px",
    cursor: "pointer",
  },
};

export default Navbar;
