import { useState, useEffect } from "react";
import { NavLink , Navigate } from "react-router-dom";
import axios from "axios"

const colours {
	pageBg: "#FFF8D6",
	heading: "#FFCB30",
};


function SignIn(){

const [username,setUsername]= useState("");
const [email,setEmail]= useState("");
const [password,setPassword]= useState("");
const [loggedIn, setLoggedIn] = useState(false);

const handleSignin= async() =>{
	try{
	const formData = new URLSearchParams();
	formData.append("username",username);
	formData.append("email",email);
	formData.append("password",password);
	const res = await axios.post(
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
	const res = await axios.post(
	"http://127.0.0.1:8000/auth/login",
	loginData,
	{
	headers: {
		"Content-Type": "application/x-www-form-urlencoded"
	}
	}
	);

	const token = res.data.token;
	if (token){
		localStorage.setItem("token",token);
	}
	setLoggedIn(true);
	} catch(err){
	alert("Sign In Failed, try again later !");
	console.log(err);
	}
};

if !(loggedIn){
return (
<div className="min-h-screen" style={{color : colours.pageBg}}>
	<div className="absolute top-6 right-6" style = {{ color: colours.heading, opacity:0.3, fontSize:"1.3rem",
		fontWeight: "bold", fontFamily: "Georgia,Serif" }}> JBMCodeInsights </div>
	<div className="min-h-screen p-10 justify-center items-center ">
		<form className="bg-white p-8 rounded-xl  shadow-lg w-94">
			<input type="text" name="username" value={username} placeholder="Enter Username"
				onChange={ (e)=> setUsername(e.target.value)} className= "rounded-lg text-black p-5" style={{ backgroundColor: colours.pageBg}}/>
			<input type="text" name="email" value={email} placeholder="Enter Email"
				onChange={ (e)=> setEmail(e.target.value)} className= "rounded-lg text-black p-5" style={{ backgroundColor: colours.pageBg}} />
			<input type="password" name="password" value={password} placeholder="Enter Password"
				onChange={ (e)=> setPassword(e.target.value)} className= "rounded-lg text-black p-5" style={{ backgroundColor: colours.pageBg}} />
			<button type="submit" onClick={handleSignin} className="rounded-lg text-black p-5" style={{ backgroundColor: colours.pageBg}}> Sign In </button>
		</form>
		<NavLink to="/login" className="text-sml text-black p-5 hover:text-gray-700">Already have an account? Login </NavLink>
	</div>
</div>

);
}
else{
	return <Navigate to ="/Home" />;
}

}
export default function SignIn;