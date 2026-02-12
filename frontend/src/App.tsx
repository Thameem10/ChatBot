import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import ChatPage from "./pages/ChatPage";
import FilePage from "./pages/FilePage";
import Layout from "./pages/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import { AuthProvider } from "./contexts/AuthContext";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* PUBLIC LOGIN ROUTE - no layout */}
          <Route path="/login" element={<LoginPage />} />

          {/* PROTECTED ROUTES WITH LAYOUT */}
          <Route
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route path="/" element={<FilePage />} />
            <Route path="/chatbox" element={<ChatPage />} />
            {/* <Route path="/" element={<ContactForm />} /> */}
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
