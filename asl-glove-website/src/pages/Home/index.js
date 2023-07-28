import React from "react";
import "./homestyles.sass";
import { left_glove_state, right_glove_state } from "../../App";
import {useRecoilValue, useSetRecoilState} from 'recoil'
import Button from "../Button/button"

function goto(s) {
  window.location.replace(s)
}
export default function Home() {
  const left_id = useRecoilValue(left_glove_state)
  const setLeftId = useSetRecoilState(left_glove_state)
  const rightId = useRecoilValue(right_glove_state)
  const setRightId = useSetRecoilState(right_glove_state)
    return (    
          <div className = "background-home">
          <div className = "content">
          <div className = "title-box">
            <div className = "title">SignAlong</div>
            
            <div className = "menu"><Button className = "dropdown-button"></Button></div>
          </div>
          <div className="body">
          <button className="game1" onClick={()=>goto('/game')}>Play Now</button>
          <button className="game2" onClick={()=>goto('/signyourname')}>Play Now</button>
          </div>
          </div>      

      </div>
    )
}