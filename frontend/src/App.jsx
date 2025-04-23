import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthProvider";
import Login from "./components/Login";
import Register from "./components/Register"
import PrivateRoute from "./routes/PrivateRoute";
import Dashboard from "./components/Dashboard";
import TestEl from "./components/TestEl";
import SetAwsCred from "./components/SetAwsCred/SetAwsCred";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route element={<PrivateRoute />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/tester" element={<TestEl />} />
            <Route path="/aws_cred/setup" element={<SetAwsCred />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
