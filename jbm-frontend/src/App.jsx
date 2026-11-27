
import './App.css'
import Navbar from "./components/Navbar.jsx";
import Home from "./pages/Home.jsx";
import Landing from "./pages/landing.jsx";
import Login from "./pages/Login.jsx";
import SignIn from "./pages/SignIn.jsx";
import { Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";





function DashboardLayout ({children}) {
  return (
    <div className= "flex min-h-screen">
      <Navbar />
      <main className="flex-1 px-12 py-8">
        {children}
      </main>
    </div>
  );
}

function App() {

  return (
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signin" element={<SignIn />} />


          <Route path="/Home" element={
            <ProtectedRoute>
              <DashboardLayout>
                <Home />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        </Routes>
    
  );
}

export default App;
