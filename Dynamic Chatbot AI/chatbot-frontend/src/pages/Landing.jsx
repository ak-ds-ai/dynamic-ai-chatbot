import { Link, Navigate } from "react-router-dom";
import { motion } from "framer-motion";

const Landing = () => {
  const token = localStorage.getItem("token");

  if (token) {
    return <Navigate to="/chat" />;
  }

  return (
    <div style={styles.wrapper}>
      {/* Glow blobs */}
      <div style={styles.glowTop} />
      <div style={styles.glowBottom} />

      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        style={styles.card}
      >
        <motion.h1
          initial={{ scale: 0.95 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2 }}
          style={styles.title}
        >
          Dynamic AI Chatbot 🤖
        </motion.h1>

        <p style={styles.subtitle}>
          Secure • Intelligent • Local LLM powered
        </p>

        <div style={styles.buttons}>
          <Link to="/login" style={styles.loginBtn}>
            Login
          </Link>

          <Link to="/register" style={styles.registerBtn}>
            Get Started
          </Link>
        </div>
      </motion.div>
    </div>
  );
};

export default Landing;

/* ---------------- STYLES ---------------- */

const styles = {
  wrapper: {
    height: "100vh",
    background:
      "linear-gradient(135deg, #5B4BDB 0%, #8B3CF6 50%, #EC4899 100%)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    position: "relative",
    overflow: "hidden",
  },

  glowTop: {
    position: "absolute",
    width: "420px",
    height: "420px",
    background: "radial-gradient(circle, #A78BFA, transparent 70%)",
    top: "-120px",
    right: "-120px",
    filter: "blur(120px)",
  },

  glowBottom: {
    position: "absolute",
    width: "420px",
    height: "420px",
    background: "radial-gradient(circle, #F472B6, transparent 70%)",
    bottom: "-120px",
    left: "-120px",
    filter: "blur(120px)",
  },

  card: {
    background: "rgba(255,255,255,0.18)",
    backdropFilter: "blur(18px)",
    borderRadius: "22px",
    padding: "60px 70px",
    textAlign: "center",
    border: "1px solid rgba(255,255,255,0.25)",
    boxShadow: "0 25px 60px rgba(0,0,0,0.35)",
    zIndex: 2,
  },

  title: {
    fontSize: "3rem",
    fontWeight: "700",
    color: "#ffffff",
    marginBottom: "12px",
  },

  subtitle: {
    color: "#E9D5FF",
    fontSize: "1.05rem",
    marginBottom: "42px",
  },

  buttons: {
    display: "flex",
    gap: "20px",
    justifyContent: "center",
  },

  loginBtn: {
    padding: "12px 30px",
    borderRadius: "999px",
    background: "rgba(255,255,255,0.25)",
    color: "#ffffff",
    textDecoration: "none",
    fontWeight: "500",
    transition: "all 0.3s ease",
  },

  registerBtn: {
    padding: "12px 30px",
    borderRadius: "999px",
    background: "#6D28D9",
    color: "#ffffff",
    textDecoration: "none",
    fontWeight: "600",
    boxShadow: "0 10px 30px rgba(109,40,217,0.45)",
    transition: "all 0.3s ease",
  },
};
