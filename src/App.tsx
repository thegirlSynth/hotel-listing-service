import { BrowserRouter, Routes, Route } from 'react-router-dom';
import "./App.css";
import Home from "./pages/home/Home";
import About from "./pages/about/About";

const App = () => {
	return (
		<div className="App">
			<BrowserRouter>
				<Routes>
					<Route path="/" element={<Home/>} />
					<Route path="about" element={<About/>} />
				</Routes>
			</BrowserRouter>
		</div>
	)
}

export default App;
