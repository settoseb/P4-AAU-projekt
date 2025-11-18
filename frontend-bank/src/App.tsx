import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Routes, Route } from "react-router-dom";
import { ProtectedRoute } from "./components/protected-route";

import Home from "./pages/Home";
import Login from "./pages/Login";
import About from "./pages/About";
import Signup from "./pages/Signup";
import Transaction from "./pages/Transaction";

function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        }
      />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route
        path="/about"
        element={
          <ProtectedRoute>
            <About />
          </ProtectedRoute>
        }
      />
      <Route
        path="/transaction"
        element={
          <ProtectedRoute>
            <Transaction />
          </ProtectedRoute>
        }
      />
    </Routes>
  )
}

export default App
