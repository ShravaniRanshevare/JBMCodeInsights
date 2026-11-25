import { NavLink } from "react-router-dom";
import "./Navbar.css";

const colours = {
	sidebarBg: "#FFCB30",
	text : "#000000",
	selectedText : "#FFFFFF",
	TextBorder : "2px solid #000000",
};

function Navbar() {
	return (
		<aside className= "w-64 h-screen flex flex-col justify-between p-6" style = {{ backgroundColor: colours.sidebarBg}}>
			<h1 className="text-2xl font-bold mb-10">
				JBMCodeInsights
			</h1>

			<div>
				<NavLink to="/profile" className = "bg-white p-3 rounded-lg shadow hover:bg-gray-100 mb-4">
					👤 Profile
				</NavLink>
			</div>
			<div className= "border-t border-gray-400 my-6"></div>
			<div>
				<nav>
					<ul className= "space-y-4">
					<li>
						<NavLink to = "/projects" 
							className = {({ isActive }) => isActive ? "nav-link active": "nav-link"}>
							View Previous Projects
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
			</div>
		</aside>

	);


}

export default Navbar;