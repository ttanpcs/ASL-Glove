import React from "react";
import "./gamestyles.sass";
import Button from "../Button/button";
import { left_glove_state, right_glove_state } from "../../App";
import {useRecoilValue, useSetRecoilState} from 'recoil'

export default function Game() {
  const left_id = useRecoilValue(left_glove_state)
  const setLeftId = useSetRecoilState(left_glove_state)
  const rightId = useRecoilValue(right_glove_state)
  const setRightId = useSetRecoilState(right_glove_state)
    return (    
          <div className = "background">
          <div className = "content">
          <div className = "title-box">
            <div className = "title">SignAlong</div>
            <div className = "menu"><Button className = "dropdown-button"></Button></div>
          </div>

          </div>      
  
      </div>
    )
  
}