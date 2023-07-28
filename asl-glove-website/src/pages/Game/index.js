import React from "react";
import "./gamestyles.sass";
import Button from "../Button/button";
import { left_glove_state, right_glove_state } from "../../App";
import {useRecoilValue, useSetRecoilState} from 'recoil'
import {useEffect, useRef} from 'react';



const GameBox = (rightid) => {
  const [active, setActive] = React.useState(false);
  const [startTime, setStartTime] = React.useState(0);
  const [runTime, setRunTime] = React.useState(0);
  const alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",];
  const [letter, setLetter] = React.useState("A")
  const [timeOut, setTimeOut] = React.useState(false)
  const [showChart, setShowChart] = React.useState(false)

  const Start = async () => {
    console.log(rightid)
    const response = await fetch('http://localhost:5000/reset', {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
        });
    await response.text()
    const response2 = await fetch('http://localhost:5000/start', {
     method: 'POST',
     headers: {
       Accept: 'application/json',
       'Content-Type': 'application/json',
     },
     body: JSON.stringify({glove_id: rightid.rightid.id, ocid: rightid.rightid.open_id, ccid: rightid.rightid.close_id})
   });
    await response2.text()
  }
  
  const Querying = async (num) => {
    var done = false
    if (!done) {
      const response = await fetch('http://localhost:5000/query', {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({label: letter, primary: rightid.rightid.id})
        });
      done = (await response.json()).found
    }
    if (!done && num < 3) {
      await Querying(num + 1)
    } else {
      setActive(false)
    }
  }
  
  const Stop = async () => {
    const response = await fetch('http://localhost:5000/stop', {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({glove_id: rightid.rightid.id})
        });
    await response.text()
  }
  
  const runTimer = async () => {
    const d = new Date()
    if (active) {
      console.log(active)
      const newTime = d.getTime()-startTime
      setRunTime(newTime)
      console.log(startTime)
      await new Promise(resolve => setTimeout(resolve, 990));
      runTimer()
    }
  }

  const handleStart = async () => {
    setShowChart(false)
    setActive(true)
    const d = new Date()
    setStartTime(d.getTime())
    let random = Math.floor(Math.random() * 26)
    setLetter(alphabet[random])
  }

  useEffect(() => {
    const gameStart = async () => {
      if (active) {
        console.log(active)
        // runTimer()
        await Start(rightid)
        await Querying(0)
        await Stop(rightid.glove_id)
      }
    }
    gameStart()
  }, [active, startTime, letter])

  return (
    <div className = "gamebox">
    {active ? (
      <button onClick={() => {setShowChart(!showChart)}} className = "chartbutton">
        {showChart ? (
          <div className="chart">

          </div>
        ): 
        (<div className="flashcard">
          <h1 className="extra">Try to sign the letter:</h1>
          <h1 className="lettershow">{letter}</h1>
          {/* <h1 className="extra">Seconds elapsed: {Math.floor(runTime/1000.0)}</h1>  */}
        </div>)}
      
      </button>
    ) :
     <button onClick={() => {handleStart()}} className = "startbutton">Play Our Game!</button>
    } 
    </div>
  )
 
}

export default function Game() {
  const leftid = useRecoilValue(left_glove_state)
  const setLeftId = useSetRecoilState(left_glove_state)
  const rightid = useRecoilValue(right_glove_state)
  const setRightId = useSetRecoilState(right_glove_state)
    return (    
          <div className = "background-game">
          <div className = "content-game">
          <div className = "title-box">
            <div className = "title">SignAlong</div>
            <div className = "menu"><Button className = "dropdown-button"></Button></div>
          </div>
          <div className="body">
          <GameBox rightid = {rightid}/>
          </div>
          </div>      
  
      </div>
    )
  
}