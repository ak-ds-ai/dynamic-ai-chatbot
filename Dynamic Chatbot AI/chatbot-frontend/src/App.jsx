import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import DynamicAIChatbot from "./components/DynamicAIChatbot";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Landing from "./pages/Landing";
import Docs from "./pages/Docs";

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        {/* Public */}
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected */}
        <Route
          path="/chat"
          element={
            <ProtectedRoute>
              <DynamicAIChatbot />
            </ProtectedRoute>
          }
        />

        <Route
          path="/docs"
          element={
            <ProtectedRoute>
              <Docs />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
