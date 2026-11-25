import { NavLink , Navigate } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";

const colours = {
	pageBg: "#FFF8D6",
	heading: "#FFCB30",
};


function Login(){
const [username,setUsername]= useState("");
const [password, setPassword] = useState("");
const [loggedIn, setLoggedIn] = useState(false);

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
		setLoggedIn(true);
	} catch(err){
		alert("login failed, account does not exist");
		console.log(err);
	}
};

if !(loggedIn){
return (
<div className="min-h-screen" style={{colours.pageBg}}>
	<div className="absolute top-6 right-6" style={{color: colours.heading, opacity: 0.3, fontSize: "1.5rem",
		fontWeight: "bold", fontFamily: "Georgia,serif"}}> JBMCodeInsights </div>
	<div className="min-h-screen p-10 flex justify-center items-center">
		<form className="bg-white p-8 rounded-xl shadow-lg w-96">
			<input placeholder= "Enter Username" type="text" name="username" 
				value={username} onChange= {(e)=> setUsername(e.target.value)} className= "rounded-lg text-black p-5" style={{ backgroundColor: colours.pageBg}}/>
			<input placeholder= "Enter Password" type="password" 
				name="password" value={password} onChange={(e)=> setPassword(e.target.value)} className= "rounded-lg text-black p-5" style={{ backgroundColor: colours.pageBg}}/>
			<button type="submit" onClick={handleLogin()} className= "rounded-lg text-black p-5" style={{ backgroundColor: colours.pageBg}}> Login </button>
		</form>
		<NavLink to="/signin" className="text-sml text-black p-5 hover:text-gray-700"> Don't have an account? Sign Up Instead </NavLink>
	</div>
</div>

);
}
else{
	return <Navigate to = "/Home" />;
}

}

export default function Login;