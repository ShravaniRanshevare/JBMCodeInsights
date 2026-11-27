import { NavLink , Navigate, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import "../css/login.css";

const colours = {
	pageBg: "#FFCB30",
	heading: "#FFDC73",
};


function Login(){
const [username,setUsername]= useState("");
const [password, setPassword] = useState("");
const navigate = useNavigate();

const handleLogin= async() =>{
	try{

		const formData = new URLSearchParams();
		formData.append("username",username);
		formData.append("password",password);
		const res = await axios.post(
		"http://127.0.0.1:8000/auth/login",
		formData,
		{
			headers: {"Content-Type":  "application/x-www-form-urlencoded"}
		}
		);
		const token = res.data.access_token
		if (token){
			localStorage.setItem("token",token);
		}
		navigate("/Home");
	} catch(err){
		alert("login failed, account does not exist");
		console.log(err);
	}
};

return (
<div className="min-h-screen" style = {{ backgroundColor: colours.heading }} >
	<div className="eye eye1">👁️</div>
	<div className="eye eye2">👁️</div>
	<div className="eye eye3">👁️</div>
	<div className="eye eye4">👁️</div>
	<div className="eye eye5">👁️</div>
	<div className="eye eye6">👁️</div>
	<div className="absolute top-6 right-6" style={{color: colours.pageBg, opacity: 0.9, fontSize: "1.5rem",
		fontWeight: "bold", fontFamily: "Georgia,serif"}}> JBMCodeInsights </div>
	<div className="min-h-screen flex flex-col justify-center items-center gap-2 shadow-lg">
			<form className="bg-[#FFF5DB] p-12 rounded-3xl shadow-lg w-[380px] min-h-[370px] flex flex-col gap-6 ">
					<h1 className="text-center font-semibold text-xl text-black p-15">Login</h1>
				<input placeholder= "Enter Username" type="text" name="username" 
				value={username} onChange= {(e)=> setUsername(e.target.value)} className= "mt-10 h-30 text-xl rounded-2xl text-black p-6" style={{ backgroundColor: colours.pageBg, opacity: 0.8}}/>

				<input placeholder= "Enter Password" type="password" 
				name="password" value={password} onChange={(e)=> setPassword(e.target.value)} className= "h-30 text-xl rounded-2xl text-black p-6" 
				style={{ backgroundColor: colours.pageBg, opacity: 0.8}}/>

				<button type="button" onClick={handleLogin} className= "h-10 px-10 py-3 rounded-full font-semibold text-lg self-center w-40 transition-all hover:scale-105" 
					style={{ backgroundColor: colours.pageBg, opacity: 0.8}}> Login </button>
			</form>
		<NavLink to="/signin" className="mt-6 text-xl text-black hover:text-gray-700" style={{opacity: 0.5, fontSize: "1rem", fontFamily: "Georgia,serif"}}> Don't have an account? Sign Up Instead </NavLink>
	</div>
</div>

);


}

export default Login;