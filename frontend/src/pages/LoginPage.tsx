import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { LogIn } from "lucide-react";
import { useAuth } from "../contexts/AuthContext";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loginError, setLoginError] = useState("");
  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const { signIn } = useAuth();

  const validateForm = () => {
    let valid = true;

    // Email validation
    if (!email.trim()) {
      setEmailError("Email is required");
      valid = false;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setEmailError("Enter a valid email address");
      valid = false;
    } else {
      setEmailError("");
    }

    // Password validation
    if (!password.trim()) {
      setPasswordError("Password is required");
      valid = false;
    } else if (password.length < 6) {
      setPasswordError("Password must be at least 6 characters");
      valid = false;
    } else {
      setPasswordError("");
    }

    return valid;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    setLoginError(""); // clear old error

    if (!validateForm()) return;

    setLoading(true);

    try {
      await signIn(email, password);
      navigate("/");
    } catch (err: any) {
      setLoginError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-gray-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md p-8">
        <div className="text-center mb-8">
          <div
            className="inline-flex items-center justify-center w-16 h-16 rounded-full mb-4"
            style={{ backgroundColor: "#ca8a04" }}
          >
            <LogIn className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">LOGIN IN</h1>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* EMAIL FIELD */}
          {loginError && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded text-center">
              {loginError}
            </div>
          )}
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Email Address
            </label>

            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                setEmailError("");
              }}
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 outline-none transition
                ${
                  emailError
                    ? "border-red-500 focus:ring-red-400"
                    : "border-gray-300 focus:ring-amber-600"
                }
              `}
            />

            {emailError && (
              <p className="text-red-600 text-sm mt-1">{emailError}</p>
            )}
          </div>

          {/* PASSWORD FIELD */}
          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Password
            </label>

            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                setPasswordError("");
              }}
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 outline-none transition
                ${
                  passwordError
                    ? "border-red-500 focus:ring-red-400"
                    : "border-gray-300 focus:ring-amber-600"
                }
              `}
            />

            {passwordError && (
              <p className="text-red-600 text-sm mt-1">{passwordError}</p>
            )}
          </div>

          {/* SUBMIT BUTTON */}
          <button
            type="submit"
            disabled={loading}
            className="w-full text-white font-medium py-3 px-4 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
            style={{ backgroundColor: loading ? "#ca8a04" : "#ca8a04" }}
            onMouseOver={(e) =>
              !loading && (e.currentTarget.style.backgroundColor = "#b07a04")
            }
            onMouseOut={(e) =>
              !loading && (e.currentTarget.style.backgroundColor = "#ca8a04")
            }
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>
      </div>
    </div>
  );
}
