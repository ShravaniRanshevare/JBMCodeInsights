import { NavLink, useNavigate } from "react-router-dom";
import {useState} from "react";
import "../css/Navbar.css";

const colours = {
	sidebarBg: "#FFDC73",
	text : "#6E3000",
	selectedText : "#FFFFFF",
	TextBorder : "2px solid #000000",
};

function Navbar() {

	const navigate = useNavigate();
	const [showLogoutModal,setShowLogoutModal]= useState(false);


	const handleLogout= ()=>{
		localStorage.removeItem("token");
		navigate("/login")

	}
	return (
		<aside className= "flex flex-col gap-15 w-50 min-h-screen p-6 shadow-lg" 
			style = {{ backgroundColor: colours.sidebarBg}}>
			<h1 className="text-[#6E3000] text-center text-xl font-bold " style={{opacity:0.5, fontFamily: "Georgia,Serif"}}>
				JBMCodeInsights
			</h1>
				<div className="flex flex-col justify-between align-items items-center">
				<NavLink to="/profile" className = "text-[#6E3000] flex justify-center items-center bg-[#FFF8D6] w-20 h-20 p-3 rounded-full 
					shadow hover:text-white" style={{opacity:0.9, fontFamily: "Georgia,Serif"}}>
					Profile
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

					<li>
						<p onClick={()=> setShowLogoutModal(true)} className="nav-link cursor-pointer">
							Logout
						</p>
					</li>
					</ul>
			</nav>	
			{

				showLogoutModal && (
					<div className="
            					fixed
            					inset-0
					            bg-black/40
					            flex
					            justify-center
					            items-center
					            z-50
					        ">

					            <div className="
					                bg-[#FAF5E9]
					                rounded-3xl
					                p-8
					                w-[400px]
					                h-[100px]
					                shadow-xl
					                flex flex-col gap-5
					            ">
						<h2 className="text-center text-[#6E3000] text-xl font-semibold font-serif mb-10">
							Log Out?
						</h2>
						<div className="flex justify-center gap-5 p-10">
							<button className="w-25 text-white font-serif font-semibold rounded-lg" style={{backgroundColor: colours.sidebarBg}}
								onClick={()=> setShowLogoutModal(false)}>
								Cancel
							</button>
							<button className="w-25 bg-[#FF0000] text-white font-serif font-semibold rounded-lg" 
								onClick={handleLogout}>
								Logout
							</button>
						</div>
					</div>
				</div>


				)
			}
			
		</aside>

	);


}

export default Navbar;