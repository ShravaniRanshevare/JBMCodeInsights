import TrendGraph from "../components/TrendGraph";

const colours = {
	pageBg: "#FFF8D6",
	heading: "#FFCB30",
};


function Home(){
	


return (
	<div 
		className= "min-h-screen p-10"
		style = {{ backgroundColor: colours.pageBg }}>
		<h1 className= "text-5xl font-bold font-serif mb-4" style={{color: colours.heading}}>
			JBMCodeInsights <div className= "eye"> 👁️</div> </h1> 
	
		<p className= "text-lg text-gray-700 mb-10">
			Track how your code quality evolves over time !
		</p>

		<TrendGraph />
	</div>

);



}

export default Home;