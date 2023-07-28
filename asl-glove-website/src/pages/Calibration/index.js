import React from "react";
import "./calstyles.sass";
import Button from "../Button/button"
import { left_glove_state, right_glove_state } from "../../App";
import {useRecoilValue, useSetRecoilState} from 'recoil'

const asy = async (g_id, open) => {
  var endpoint = 'http://localhost:5000/closedcals'
  if (open) {
    endpoint = 'http://localhost:5000/opencals'
  }
//   const response = await fetch('http://localhost:5000/closedcals', {
//      method: 'GET',
//      headers: {
//        Accept: 'application/json',
//        'Content-Type': 'application/json',
//      },
//      body: JSON.stringify({glove_id: g_id})
//    });
//   const result = await response.json()
//   return result
// }
   const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({glove_id : g_id})
    });
  const result = await response.json()
  return result
}

const PickExisting = ({side, g_id, g_open, setID, currID}) => {
 const [open, setOpen] = React.useState(false);
 const [existing, setExisting] = React.useState([]);
 const handleOpen = async () => {
   setOpen(!open);
   setExisting(await asy(g_id, g_open))
 }
 var open_str = "an Open"
 if (!g_open) {
  open_str = "a Closed"
 }
 if (g_open) {
 return (
    <div>
      <button className = "qu-button2" onClick={handleOpen}>Pick {open_str} Calibration for Your {side} Glove</button>
      {open ? (
          <ul className="qu-list">
            {existing.map((id, index)=>{
              return <li key={index} >
                <button className = "qu-item" onClick={() => setID({open_id: id, id: currID.id, close_id: currID.close_id})}>{id}</button>
                </li>
            })}
          </ul>
      ) : null}
    </div>
 )
} else {
  return (
    <div>
      <button className = "qu-button2" onClick={handleOpen}>Pick {open_str} Calibration for Your {side} Glove</button>
      {open ? (
          <ul className="qu-list">
            {existing.map((id, index)=>{
              return <li key={index} >
                <button className = "qu-item" onClick={() => setID({close_id: id, id: currID.id, open_id: currID.open_id})}>{id}</button>
                </li>
            })}
          </ul>
      ) : null}
    </div>
  )
}
}

const asy2 = async (g_id, open) => {
  const response = await fetch('http://localhost:5000/snapshot', {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({glove_id: g_id, type: open})
  });
const result = await response.json()
return result.id
}

const regCal = async (right, open, g_id, setID, currID) => {
  var alert_str = ""
  var open_str = "closed"
  if (right) {
    if (open) {
      alert_str = "You calibrated an open right glove."
    } else {
      alert_str = "You calibrated a closed right glove."
    }
  } else {
    if (open) {
      alert_str = "You calibrated an open left glove."
    } else {
      alert_str = "You calibrated a closed left glove."
    }
  }
  alert(alert_str)

  if (open) {
    open_str = "open"
  }
  const cal_id = await asy2(g_id, open_str)
  console.log(cal_id)
  console.log(currID)
  if (!open) {
    setID({close_id: cal_id, open_id: currID.open_id, id: currID.id})
  } else {
    setID({open_id: cal_id, close_id: currID.close_id, id: currID.id})
  }
}

export default function Calibration() {

  const leftid = useRecoilValue(left_glove_state)
  const setLeftId = useSetRecoilState(left_glove_state)
  const rightid = useRecoilValue(right_glove_state)
  const setRightId = useSetRecoilState(right_glove_state)
    
    return (
          
          <div className = "background-cal">
          <div className = "content">
          <div className = "title-box-cal">
            <div className = "title">SignAlong</div>
            <div className = "menu"><Button className = "dropdown-button"></Button></div>
          </div>
          <div className="four-col">
            <div className="quarter">
              <button className="qu-button" onClick={() => regCal(false, true, leftid.id, setLeftId, leftid)}>Make a New Open Calibration of Your Left Glove</button>
              <PickExisting side = "Left" g_id = {leftid.id} g_open = {true} setID = {setLeftId} currID = {leftid}/>
            </div>
            <div className="quarter">
              <button className="qu-button" onClick={() => regCal(false, false, leftid.id, setLeftId, leftid)}>Make a New Closed Calibration of Your Left Glove</button>
              <PickExisting side = "Left" g_id = {leftid.id} g_open = {false} setID = {setLeftId} currID = {leftid}/>
            </div>
            <div className="quarter">
              <button className="qu-button" onClick={() => regCal(true, true, rightid.id, setRightId, rightid)}>Make a New Open Calibration of Your Right Glove</button>
              <PickExisting side = "Right" g_id = {rightid.id} g_open = {true} setID = {setRightId} currID = {rightid}/>
            </div>
            <div className="quarter">
              <button className="qu-button" onClick={() => regCal(true, false, rightid.id, setRightId, rightid)}>Make a New Closed Calibration of Your Right Glove</button>
              <PickExisting side = "Right" g_id = {rightid.id} g_open = {false} setID = {setRightId} currID = {rightid}/>
            </div>
          </div>
          </div>      

          
            </div>
    )
  
}