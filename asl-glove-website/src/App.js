import React, { useEffect, useState } from 'react';
import './App.css';
import {Routes, Route, useLocation}
    from 'react-router-dom';
import Home from './pages/Home';
import Registration from './pages/Registration'
import Game from './pages/Game'
import Calibration from './pages/Calibration'
import SignName from './pages/SignName'
  

function App() {    

return (
    <Routes>
        <Route exact path='/' element={<Home />} />
        <Route path='/registration' element={<Registration/>} />
        <Route path='/calibration' element={<Calibration/>} />
        <Route path='/game' element={<Game/>} />
        <Route path='/signyourname' element={<SignName/>} />
    </Routes>
);
}

export default App;
