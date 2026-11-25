
import './App.css'
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Landing from "./pages/landing";
import Login from "./pages/Login";
import SignIn from "./pages/SignIn";
import { Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";





function DashboardLayout ({children}) {
  return (
    <div className= "flex">
      <Navbar />
      <main className="flex-1 p-8">
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
            </ProtectedRoute>/>
          } 
        />

          <Route path="/profile" element={
            <ProtectedRoute>
              <DashboardLayout>
                <Profile />
              </DashboardLayout>
            </ProtectedRoute>
          } />
          <Route path="/projects" element={
            <ProtectedRoute>
              <DashboardLayout>
                <Projects />
              </DashboardLayout>
            </ProtectedRoute>
          } />
          <Route path="/create-project" element={
            <ProtectedRoute>
              <DashboardLayout>
                <CreateProject />
              </DashboardLayout>
            </ProtectedRoute>
          } />
          <Route path="/analysis" element={
            <ProtectedRoute>
              <DashboardLayout>
                <Analysis />
              </DashboardLayout>
            </ProtectedRoute>
          } />
        </Routes>
    
  );
}

export default App;
