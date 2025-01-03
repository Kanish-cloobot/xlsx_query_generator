import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import "./AuthPage.css";

const AuthPage = () => {
  const [isLogin, setIsLogin] = useState(true);

  // Form state and validation errors
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });
  const [errors, setErrors] = useState({});
  const navigate = useNavigate(); // Initialize navigate function

  const toggleForm = () => {
    setIsLogin((prev) => !prev);
    setFormData({ username: "", email: "", password: "" }); // Reset form
    setErrors({}); // Clear errors
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.username.trim()) {
      newErrors.username = "Username is required";
    }

    if (!isLogin && !formData.email.trim()) {
      newErrors.email = "Email is required";
    } else if (
      !isLogin &&
      !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(formData.email)
    ) {
      newErrors.email = "Invalid email address";
    }

    if (!formData.password.trim()) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 6) {
      newErrors.password = "Password must be at least 6 characters long";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0; // Return true if no errors
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      // On successful login, redirect to home page
      if (isLogin) {
        alert("Login Successful");
        navigate("/home"); // Redirect to home page
      } else {
        alert("Account Created Successfully");
        setFormData({ username: "", email: "", password: "" });
        setErrors({});
      }
    }
  };

  return (
    <section>
      <div className="colour"></div>
      <div className="colour"></div>
      <div className="colour"></div>
      <div className="box">
        <div className="square" style={{ "--i": 0 }}></div>
        <div className="square" style={{ "--i": 1 }}></div>
        <div className="square" style={{ "--i": 2 }}></div>
        <div className="square" style={{ "--i": 3 }}></div>
        <div className="square" style={{ "--i": 4 }}></div>
        <div className={`container ${isLogin ? "show-login" : "show-signup"}`}>
          {/* Login Form */}
          {isLogin && (
            <div className="form">
              <h2>Login</h2>
              <form onSubmit={handleSubmit}>
                <div className="input__box">
                  <input
                    type="text"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    placeholder="Username"
                  />
                  {errors.username && (
                    <span className="error">{errors.username}</span>
                  )}
                </div>
                <div className="input__box">
                  <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Password"
                  />
                  {errors.password && (
                    <span className="error">{errors.password}</span>
                  )}
                </div>
                <div className="input__box">
                  <button type="submit">Login</button>
                </div>
                <p className="switch-form">
                  Don't have an account?{" "}
                  <span onClick={toggleForm}>Create Account</span>
                </p>
              </form>
            </div>
          )}

          {/* Sign Up Form */}
          {!isLogin && (
            <div className="form">
              <h2>Create Account</h2>
              <form onSubmit={handleSubmit}>
                <div className="input__box">
                  <input
                    type="text"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    placeholder="Username"
                  />
                  {errors.username && (
                    <span className="error">{errors.username}</span>
                  )}
                </div>
                <div className="input__box">
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="Email"
                  />
                  {errors.email && <span className="error">{errors.email}</span>}
                </div>
                <div className="input__box">
                  <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Password"
                  />
                  {errors.password && (
                    <span className="error">{errors.password}</span>
                  )}
                </div>
                <div className="input__box">
                  <button type="submit">Sign Up</button>
                </div>
                <p className="switch-form">
                  Already have an account?{" "}
                  <span onClick={toggleForm}>Login</span>
                </p>
              </form>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

export default AuthPage;
