import React from "react";
import "./regstyles.sass";
import Button from "../Button/button"
import { left_glove_state, right_glove_state } from "../../App";
import {useRecoilValue, useSetRecoilState} from 'recoil'

// const asy = async () => {
//    const response = await fetch('http://localhost:5000/opencals', {
//       method: 'POST',
//       headers: {
//         Accept: 'application/json',
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({glove_id : 1})
//     });
//   const result = await response.json()
//   return result
// }

const asy = async (side) => {
  var endpoint = "http://localhost:5000/rightgloves"
  if (side == "Left") {
    endpoint = "http://localhost:5000/leftgloves"
  }
   const response = await fetch(endpoint, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      }
    });
  const result = await response.json()
  return result
}

const PickExisting = ({side, setID, currID}) => {
  const [open, setOpen] = React.useState(false);
  const [existing, setExisting] = React.useState([]);
  const handleOpen = async () => {
    setOpen(!open);
    setExisting(await asy(side))
  }
  return (
    <div>
      <button className = "half-button" onClick={handleOpen}>Pick a Registered {side} Glove</button>
      {open ? (
          <ul className="half-list">
            {existing.map((id, index)=>{
              return <li key={index} >
                <button className = "half-item" onClick={() => setID({id: id, open_id: currID.open_id, close_id: currID.close_id})}>{id}</button>
                </li>
            })}
          </ul>
      ) : null}
    </div>
  )
}

const asy2 = async (side, port_input) => {
  const response = await fetch('http://localhost:5000/register', {
     method: 'POST',
     headers: {
       Accept: 'application/json',
       'Content-Type': 'application/json',
     },
     body: JSON.stringify({is_primary: side, port: port_input})
   });
 const result = await response.json()
 return result
}

function RegForm({side, setID, currID}) {
  
  const [port, setPort] = React.useState("")
  var val = "Register a New Left Glove"
  var alert_str = "You registered a new left glove."
  if (side) {
    val = "Register a New Right Glove"
    alert_str = "You registered a new right glove."
  }
  const handleSubmit = async (event) => {
    event.preventDefault()
    alert(alert_str)
    const ret = (await asy2(side, port)).id
    console.log(ret)
    setID({id: ret, open_id: currID.open_id, close_id: currID.close_id})
  }
  return (
    <form className="half-form" onSubmit={handleSubmit}>
    <label>Enter your port:&nbsp; &nbsp; &nbsp;
      <input type="text" className="text-input" value = {port} onChange={(e) => setPort(e.target.value)}/>
    </label>
    <input type = "submit" className = "half-button" value = {val}></input>
    </form>
  )
}


export default function Registration() {
  
  const leftid = useRecoilValue(left_glove_state)
  const setLeftId = useSetRecoilState(left_glove_state)
  const rightid = useRecoilValue(right_glove_state)
  const setRightId = useSetRecoilState(right_glove_state)
    return (    
          <div className = "background-reg">
          <div className = "content">
          <div className = "title-box">
            <div className = "title">SignAlong</div>
            <div className = "menu"><Button className = "dropdown-button"></Button></div>
          </div>
          <div className="left-right">
            <div className="half">
            <RegForm side = {false} setID = {setLeftId} currID = {leftid}/>
            <PickExisting side = {"Left"} setID = {setLeftId} currID = {leftid}/>
            </div>
            <div className="half">
            <RegForm side = {true} setID = {setRightId} currID = {rightid}/>
            <PickExisting side = {"Right"} setID = {setRightId} currID = {rightid}/>
            </div>
          </div>
          </div>      

          
      </div>
    )
  }

