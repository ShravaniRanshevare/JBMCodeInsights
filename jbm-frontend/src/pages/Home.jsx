import TrendGraph from "../components/TrendGraph";
import "../css/Home.css"

const colours = {
	pageBg: "#FFF8D6",
	heading: "#FFCB30",
};


function Home(){
	


return (
	<div 
		className= "min-h-screen justify-center align-center p-5"
		style = {{ backgroundColor: colours.pageBg }}>
		<div className="flex flex-col align-center items-center mb-15">
			<h1 className= "text-center text-5xl font-bold font-serif p-4" style={{color: colours.heading}}>
				JBMCodeInsights <span className= "eye"> 👁️ </span> 
			</h1> 
	
		</div>
		<div className="mt-10 rounded-2xl shadow-lg p-8 flex flex-col justify-between gap-4" style={{backgroundColor: colours.pageBg}}>
			<p className= "text-center text-lg text-gray-700 mb-10 p-4" style={{fontSize: "1rem"}}>
			Track how your code quality evolves over time !
			</p>
			<TrendGraph />
		</div>
	</div>

);



}

export default Home;