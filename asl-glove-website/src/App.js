import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route}
    from 'react-router-dom';
import Home from './pages/Home';
import Registration from './pages/Registration'
  
function App() {
return (
    <Router>
    <Routes>
        <Route exact path='/' element={<Home />} />
        <Route path='/registration' element={<Registration/>} />
    </Routes>
    </Router>
);
}

export default App;
