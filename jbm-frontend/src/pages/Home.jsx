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
		<div className="flex items-center gap-4 mb-4">
			<h1 className= "align-center text-5xl font-bold font-serif mb-4 p-4" style={{color: colours.heading}}>
				JBMCodeInsights <span className= "eye"> 👁️ </span> 
			</h1> 
	
		</div>
		<div className="rounded-2xl shadow-lg p-8 mb-10" style={{backgroundColor: colours.pageBg}}>
			<p className= "text-lg text-gray-700 mb-10 p-4">
			Track how your code quality evolves over time !
			</p>
			<TrendGraph />
		</div>
	</div>

);



}

export default Home;