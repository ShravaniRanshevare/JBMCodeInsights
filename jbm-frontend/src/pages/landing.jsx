import { NavLink } from "react-router-dom";
import { Navigate } from "react-router-dom";
import "../css/landing.css";

const colours = {
	pageBG: "#FFF8D6",
	text: "#FFCB30",
	buttonDark: "#000000",
	buttonLight: "#FFFFFF",
};




function Landing(){
	const token = localStorage.getItem("token");
	if (token){
		return <Navigate to = "/Home" />;
	}

	return (
	<div className="min-h-screen flex justify-center align-center items-center text-align-center p-10" style = {{ backgroundColor: colours.pageBG}}>
		{/* Floating Eyes */}
		<div className= "eye eye1"> 👁️</div>
		<div className= "eye eye2"> 👁️</div>
		<div className= "eye eye3"> 👁️</div>
		<div className= "eye eye4"> 👁️</div>
		<div className= "eye eye5"> 👁️</div>
		<div className= "eye eye6"> 👁️</div>
	<div className="content">
		<h1 className="mt-20 text-center text-5xl font-bold mb-10 font-serif" style={{ color: colours.text}}>
			Welcome to JBMCodeInsights </h1>
			<p className="text-center subtitle" style = {{color: colours.text, fontWeight: "semi-bold", fontFamily: "Georgia,serif"}}> Where We Have All Insights</p>

		<div className="mt-10 button-group">
			<NavLink to = "/login" className="w-[220px] h-[110px] rounded-2xl flex justify-center items-center text-black hover:text-white" 
				style={{ backgroundColor: colours.text, fontFamily: "Georgia,serif",opacity:0.7}}>
				Login
			</NavLink>

			<NavLink to = "/signin" className="w-[220px] h-[110px] rounded-2xl flex justify-center items-center text-black hover:text-white" 
				style={{ backgroundColor: colours.text, fontFamily: "Georgia,serif",opacity:0.7}}>
				Sign In
			</NavLink>
		</div>
	</div>
</div>

	);


}

export default Landing;