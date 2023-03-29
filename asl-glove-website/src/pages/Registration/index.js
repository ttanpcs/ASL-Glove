import React from "react";
import "./regstyles.sass";
import Button from "../Button/button"
import { left_glove_state, right_glove_state } from "../../App";
import {useRecoilValue, useSetRecoilState} from 'recoil'

const CreateNew = () => {

}

const PickExisting = ({existing, side}) => {
  const [open, setOpen] = React.useState(false);
  const handleOpen = function() {
    setOpen(!open);
  }
  return (
    <div>
      <button className = "half-button" onClick={handleOpen}>Pick a Registered {side} Glove</button>
      {open ? (
          <ul className="half-list">
            {existing.map((id, index)=>{
              return <li key={index} >
                <button className = "half-item">{id}</button>
                </li>
            })}
          </ul>
      ) : null}
    </div>
  )
}

//return (

  // }

export default function Registration() {
  
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
          <div className="left-right">
            <div className="half">
            <button onClick={CreateNew} className = "half-button">Register a New Left Glove</button>
            <PickExisting existing = {[1,2,3]} side = {"Left"}/>
            </div>
            <div className="half">
            <button onClick={CreateNew} className = "half-button">Register a New Right Glove</button>
            <PickExisting existing = {[1,2,3]} side = {"Right"}/>
            </div>
          </div>
          </div>      

          
      </div>
    )
  }

