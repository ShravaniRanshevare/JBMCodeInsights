import { NavLink } from "react-router-dom";
import "../css/Navbar.css";

const colours = {
	sidebarBg: "#FFDC73",
	text : "#000000",
	selectedText : "#FFFFFF",
	TextBorder : "2px solid #000000",
};

function Navbar() {
	return (
		<aside className= "flex flex-col gap-15 w-50 min-h-screen p-6 shadow-lg" 
			style = {{ backgroundColor: colours.sidebarBg}}>
			<h1 className="text-center text-xl font-bold " style={{opacity:0.5, fontFamily: "Georgia,Serif"}}>
				JBMCodeInsights
			</h1>
				<div className="flex flex-col justify-between align-items items-center">
				<NavLink to="/profile" className = "text-center bg-[#FFF8D6] w-20 h-20 p-3 rounded-full shadow hover:bg-gray-100">
					View Profile
				</NavLink>
			</div>
			
			<div className= "border-t border-gray-400 my-2 mb-20"></div>
			
			<nav>
					<ul className= "flex flex-col gap-15">
					<li>
						<NavLink to = "/projects" 
							className = {({ isActive }) => isActive ? "nav-link active": "nav-link"}>
							Previous Projects
						</NavLink>
					</li>
					<li>
						<NavLink to = "/create-project" className = {({ isActive }) => isActive ? "nav-link active": "nav-link"}>
							Create Project
						</NavLink>
					</li>
					<li>
						<NavLink to = "/analysis" className = {({ isActive }) => isActive ? "nav-link active": "nav-link"}>
							New Analysis
						</NavLink>
					</li>
					<li>
						<NavLink to ="/Home" className = {({ isActive }) => isActive ? "nav-link active": "nav-link"}>
							Home
						</NavLink>
					</li>
					</ul>
			</nav>	
			
		</aside>

	);


}

export default Navbar;