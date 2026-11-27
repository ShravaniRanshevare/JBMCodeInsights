import { useState, useEffect } from "react";
import { NavLink , Navigate,useNavigate } from "react-router-dom";
import axios from "axios"
import "../css/login.css";

const colours = {
	pageBg: "#FFCB30",
	heading: "#FFDC73",
};

function SignIn(){

const [username,setUsername]= useState("");
const [email,setEmail]= useState("");
const [password,setPassword]= useState("");
const navigate = useNavigate();

const handleSignin= async() =>{
	try{
	const formData = new URLSearchParams();
	formData.append("username",username);
	formData.append("email",email);
	formData.append("password",password);
	const res_sign = await axios.post(
	"http://127.0.0.1:8000/auth/create_account",
	formData,
	{
	headers: {
		"Content-Type": "application/x-www-form-urlencoded"
	}
	}
	);

	const loginData = new URLSearchParams();
	loginData.append("email",email);
	loginData.append("password", password);
	const res_login = await axios.post(
	"http://127.0.0.1:8000/auth/login",
	loginData,
	{
	headers: {
		"Content-Type": "application/x-www-form-urlencoded"
	}
	}
	);

	const token = res_login.data.token;
	if (token){
		localStorage.setItem("token",token);
	}
	navigate("/Home");
	} catch(err){
	alert("Sign In Failed, try again later !");
	console.log(err);
	}
};

return (
<div className="min-h-screen" style={{backgroundColor : colours.heading}}>
	<div className="eye eye1">👁️</div>
	<div className="eye eye2">👁️</div>
	<div className="eye eye3">👁️</div>
	<div className="eye eye4">👁️</div>
	<div className="eye eye5">👁️</div>
	<div className="eye eye6">👁️</div>
	<div className="absolute top-6 right-6" style = {{ color: colours.pageBg, opacity:0.9, fontSize:"1.5rem",
		fontWeight: "bold", fontFamily: "Georgia,Serif" }}> JBMCodeInsights </div>
	<div className="min-h-screen flex flex-col justify-center items-center gap-2 shadow-lg">
		<form className="bg-[#FFF5DB] p-12 rounded-3xl w-[380px] h-[370px] shadow-lg flex flex-col gap-2">
			<h1 className="text-center font-semibold text-xl text-black p-15">Sign In </h1>
			<input type="text" name="username" value={username} placeholder="Enter Username"
				onChange={ (e)=> setUsername(e.target.value)} className= "h-30 text-xl rounded-2xl text-black p-6" style={{ backgroundColor: colours.pageBg}}/>
			<input type="text" name="email" value={email} placeholder="Enter Email"
				onChange={ (e)=> setEmail(e.target.value)} className= "h-30 text-xl rounded-2xl text-black p-6" style={{ backgroundColor: colours.pageBg}} />
			<input type="password" name="password" value={password} placeholder="Enter Password"
				onChange={ (e)=> setPassword(e.target.value)} className= "h-30 text-xl rounded-2xl text-black p-6" style={{ backgroundColor: colours.pageBg}} />
			<button type="submit" onClick={handleSignin} className="rounded-full h-10 px-10 py-3 font-semibold text-lg self-center w-40 transition-all hover:scale-105 " style={{ backgroundColor: colours.pageBg}}> Sign In </button>
		</form>
		<NavLink to="/login" className="text-sml text-black p-5 hover:text-gray-700">Already have an account? Login </NavLink>
	</div>
</div>

);


}
export default SignIn;