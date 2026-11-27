import { ResponsiveContainer, LineChart, Line, CartesianGrid,
			XAxis, YAxis, Tooltip, Legend } from "recharts";
import { useState, useEffect } from "react";
import axios from "axios";

const colours = {
	pageBg: "#FFF8D6",
	heading: "#FFCB30",
};

function TrendGraph(){

	const [projects,setProjects]  = useState(0);
	const [analyses,setAnalyses]  = useState(0);
	const [avg_complexity,setAvg_Complexity]  = useState(0);
	const [avg_maintainability,setAvg_Maintainability]  = useState(0);
	const [data, setData] = useState([]);
	const token = localStorage.getItem("token");

	const fetchOverview = async()=>{
		try{
				const res = await axios.get(
					"http://127.0.0.1:8000/analyse/dashboard/overview",
					{
						headers: {Authorization: `Bearer ${token}`,},
					}
				);

				setProjects(res.data.total_projects);
				setAnalyses(res.data.total_analyses);
				setAvg_Complexity(res.data.avg_complexity);
				setAvg_Maintainability(res.data.avg_maintainability);

		} catch(err){
			console.log(err);
		}
	};


	const fetchGraph = async() =>{
		try{
			const details = await axios.get(
				"http://127.0.0.1:8000/analyse/dashboard/graph",
				{
					headers: {Authorization: `Bearer ${token}`,},
				}
			);

			setData(details.data)
			} catch(err){
				console.log(err);
			}

	};

	useEffect(()=> {
		fetchOverview();
		fetchGraph();
	}, []);

	return (
		<div className="flex flex-col justify-between gap-10">
			{/* Graph */}
			<div className="bg-white px-12 py-11 rounded-xl shadow-lg w-250">
				<ResponsiveContainer width="90%" height={500}>
					<LineChart data={data}>
						<CartesianGrid stroke="#D9D9D9" />
						<XAxis dataKey= "analysis_number" />
						<YAxis />
						<Tooltip />
						<Legend />
						<Line type="monotone"
							dataKey = "complexity"
							stroke="#FF0000"
              				strokeWidth={3}
            				/>

            			<Line
              				type="monotone"
              				dataKey="maintainability"
              				stroke="#FFCB30"
              				strokeWidth={3}
           					 />
           					</LineChart>
           				</ResponsiveContainer>
           	</div>
           	{/* KPI Cards */}
           	<div className="grid grid-cols-2 gap-8" style={{backgroundColor: colours.pageBg}}>
           		<div className="w-80 bg-white p-6 rounded-2xl shadow-md">
           			<h3 className="text-gray-500">
           				Total Projects
           			</h3>
           			<p className= "text-3xl font-bold">
           				{projects}
           			</p>
           		</div>
           		<div className="w-80 bg-white p-6 rounded-2xl shadow-md">
           			<h4 className= "text-gray-500">
           				Total Analyses
           			</h4>
           			<p className="text-3xl font-bold">
           				{analyses}
           			</p>
           		</div>
           		<div className="w-80 bg-white p-6 rounded-2xl shadow-md">
           			<h5 className= "text-gray-500">
           				Average Complexity
           			</h5>
           			<p className="text-3xl font-bold">
           				{avg_complexity}
           			</p>
           		</div>
           		<div className="w-80 bg-white p-6 rounded-2xl shadow-md">
           			<h6 className= "text-gray-500">
           				Average Maintainability
           			</h6>
           			<p className="text-3xl font-bold">
           				{avg_maintainability}
           			</p>
           		</div>
           	</div>
           </div>

	);

};
export default TrendGraph;