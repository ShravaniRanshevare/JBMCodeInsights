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
	<div className="min-h-screen flex justify-center align-center text-align-center p-10" style = {{ backgroundColor: colours.pageBG}}>
		{/* Floating Eyes */}
		<div className= "eye eye1"> 👁️</div>
		<div className= "eye eye2"> 👁️</div>
		<div className= "eye eye3"> 👁️</div>
		<div className= "eye eye4"> 👁️</div>
		<div className= "eye eye5"> 👁️</div>
		<div className= "eye eye6"> 👁️</div>
	<div className="content">
		<h1 className="text-5xl font-bold mb-10 font-serif" style={{ color: colours.text}}>
			Welcome to JBMCodeInsights </h1>
			<p className="subtitle" style = {{color: colours.text}}> Where we have all Insights</p>

		<div className="button-group">
			<NavLink to = "/login" className="p-3 rounded-lg text-white" style={{ backgroundColor: colours.text, WebkitTextStroke: "1px black" }}>
				Login
			</NavLink>

			<NavLink to = "/signin" className="p-3 rounded-lg text-white" style={{ backgroundColor: colours.text, WebkitTextStroke: "1px black" }}>
				Sign In
			</NavLink>
		</div>
	</div>
</div>

	);


}

export default Landing;