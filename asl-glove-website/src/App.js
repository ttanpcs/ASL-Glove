import React, {useState } from 'react';
import {
    RecoilRoot,
    atom,
    selector,
    useRecoilState,
    useRecoilValue,
  } from 'recoil';
import './App.css';
import {Routes, Route, BrowserRouter as Router}
    from 'react-router-dom';
import Home from './pages/Home';
import Registration from './pages/Registration'
import Game from './pages/Game'
import Calibration from './pages/Calibration'
import SignName from './pages/SignName'
import { recoilPersist } from 'recoil-persist'

const { persistAtom } = recoilPersist()


export const left_glove_state = atom({
    key: 'left_ids',
    default: {
        id: -1,
        open_id: -2,
        close_id: -3,
    },
    effects_UNSTABLE: [persistAtom],
})  
export const right_glove_state = atom({
    key: 'right_ids',
    default: {
        id: -1,
        open_id: -2,
        close_id: -3,
    },
    effects_UNSTABLE: [persistAtom],
})  

function App() {  
return (
    <RecoilRoot>
        <Router>
        <Routes>
            <Route exact path='/' element={<Home />} />
            <Route path='/registration' element={<Registration/>} />
            <Route path='/calibration' element={<Calibration/>} />
            <Route path='/game' element={<Game/>} />
            <Route path='/signyourname' element={<SignName/>} />
        </Routes>
        </Router>
    </RecoilRoot>
);
}

export default App;
